from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Profile(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    SEDENTARY = 'SED'
    LIGHT = 'LIG'
    MODERATE = 'MOD'
    ACTIVE = 'ACT'
    VERY_ACTIVE = 'VAC'
    ACTIVITY_CHOICES = [
        (SEDENTARY, 'Sedentary (little or no exercise)'),
        (LIGHT, 'Lightly active (1-3 days/week)'),
        (MODERATE, 'Moderately active (3-5 days/week)'),
        (ACTIVE, 'Active (6-7 days/week)'),
        (VERY_ACTIVE, 'Very active (hard exercise/physical job)'),
    ]

    ACTIVITY_MULTIPLIERS = {
        SEDENTARY: 1.2,
        LIGHT: 1.375,
        MODERATE: 1.55,
        ACTIVE: 1.725,
        VERY_ACTIVE: 1.9,
    }

    GOAL_LOSE = 'LOSE'
    GOAL_MAINTAIN = 'MAINTAIN'
    GOAL_GAIN = 'GAIN'
    GOAL_CHOICES = [
        (GOAL_LOSE, 'Lose weight'),
        (GOAL_MAINTAIN, 'Maintain weight'),
        (GOAL_GAIN, 'Gain weight'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    
    name = models.CharField(max_length=150)
    age = models.PositiveIntegerField(help_text='Age in years')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height_cm = models.FloatField(help_text='Height in centimeters', validators= [MinValueValidator(0.01)])
    weight_kg = models.FloatField(help_text='Weight in kilograms', validators= [MinValueValidator(0.01)])
    activity_level = models.CharField(
        max_length=3, choices=ACTIVITY_CHOICES, default=SEDENTARY
    )
    goal = models.CharField(max_length=8, choices=GOAL_CHOICES, default=GOAL_MAINTAIN)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def calculate_bmr(self):
      
        if self.gender == self.MALE:
            bmr = (66.47 + (13.75 * self.weight_kg) + (5.003 * self.height_cm) - (6.755 * self.age))
        else:
            bmr = (655.1 + (9.563 * self.weight_kg) + (1.850 * self.height_cm) - (4.676 * self.age))
        return round(bmr, 2)

    def calculate_tdee(self):
        
        multiplier = self.ACTIVITY_MULTIPLIERS.get(self.activity_level, 1.2)
        return round(self.calculate_bmr() * multiplier, 2)

    def required_calories(self):
        
        tdee = self.calculate_tdee()
        if self.goal == self.GOAL_LOSE:
            return round(tdee - 500, 2)
        if self.goal == self.GOAL_GAIN:
            return round(tdee + 500, 2)
        return tdee


class CalorieEntry(models.Model):
  

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calorie_entries',
    )
    item_name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(help_text='Calories consumed for this item')
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.item_name} ({self.calories} kcal) - {self.user.username}'
