from django.contrib import admin

from .models import CalorieEntry, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'age', 'gender', 'height_cm', 'weight_kg', 'goal', 'updated_at')
    list_filter = ('gender', 'goal', 'activity_level')
    search_fields = ('user__username', 'user__email', 'name')


@admin.register(CalorieEntry)
class CalorieEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_name', 'calories', 'date', 'created_at')
    list_filter = ('date',)
    search_fields = ('user__username', 'item_name')
    date_hierarchy = 'date'
