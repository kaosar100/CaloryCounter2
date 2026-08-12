from django.urls import path

from . import api_views, views

app_name = 'CalorieCounter'

urlpatterns = [
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Daily calorie entries
    path('entry/add/', views.CalorieEntryCreateView.as_view(), name='entry_add'),
    path('entry/<int:pk>/edit/', views.CalorieEntryUpdateView.as_view(), name='entry_edit'),
    path('entry/<int:pk>/delete/', views.CalorieEntryDeleteView.as_view(), name='entry_delete'),

    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # --- DRF API (built with mixins, not ModelViewSet) ---
    path('api/profile/', api_views.ProfileListCreateAPIView.as_view(), name='api_profile_list'),
    path('api/profile/<int:pk>/', api_views.ProfileDetailAPIView.as_view(), name='api_profile_detail'),
    path('api/entries/', api_views.CalorieEntryListCreateAPIView.as_view(), name='api_entry_list'),
    path('api/entries/<int:pk>/', api_views.CalorieEntryDetailAPIView.as_view(), name='api_entry_detail'),
]
