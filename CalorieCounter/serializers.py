from rest_framework import serializers

from .models import CalorieEntry, Profile


class ProfileSerializer(serializers.ModelSerializer):
    bmr = serializers.SerializerMethodField()
    tdee = serializers.SerializerMethodField()
    required_calories = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'age', 'gender', 'height_cm', 'weight_kg',
            'activity_level', 'goal', 'bmr', 'tdee', 'required_calories',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']

    def get_bmr(self, obj):
        return obj.calculate_bmr()

    def get_tdee(self, obj):
        return obj.calculate_tdee()

    def get_required_calories(self, obj):
        return obj.required_calories()


class CalorieEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalorieEntry
        fields = ['id', 'item_name', 'calories', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
