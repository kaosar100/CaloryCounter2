from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404, render

from .forms import CalorieEntryForm, EmailOrUsernameAuthenticationForm, ProfileForm, RegistrationForm
from .models import CalorieEntry, Profile



# Authentication views


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = 'CalorieCounter/register.html'
    success_url = reverse_lazy('CalorieCounter:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. Please log in.')
        return response


class LoginView(DjangoLoginView):
    
    template_name = 'CalorieCounter/login.html'
    authentication_form = EmailOrUsernameAuthenticationForm
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('CalorieCounter:login')



# Profile (Name, Age, Gender, Height, Weight, ...)


class ProfileView(LoginRequiredMixin, View):

    template_name = 'CalorieCounter/profile_form.html'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        form = ProfileForm(instance=profile)
        return self._render(request, form)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your profile has been saved.')
            return redirect('CalorieCounter:dashboard')
        return self._render(request, form)

    def _render(self, request, form):
      
        return render(request, self.template_name, {'form': form})


# Daily calorie intake entries (Item name, Calorie consumed)


class CalorieEntryCreateView(LoginRequiredMixin, CreateView):
    
    model = CalorieEntry
    form_class = CalorieEntryForm
    template_name = 'CalorieCounter/entry_form.html'
    success_url = reverse_lazy('CalorieCounter:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Entry added.')
        return super().form_valid(form)
    

class CalorieEntryUpdateView(LoginRequiredMixin, UpdateView):
    
    model = CalorieEntry
    form_class = CalorieEntryForm
    template_name = 'CalorieCounter/entry_form.html'
    success_url = reverse_lazy('CalorieCounter:dashboard')

    def get_queryset(self):
        # A user can only edit their own entries
        return CalorieEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Entry updated.')
        return super().form_valid(form)


class CalorieEntryDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        entry = get_object_or_404(CalorieEntry, pk=pk, user=request.user)
        entry.delete()
        messages.success(request, 'Entry removed.')
        return redirect('CalorieCounter:dashboard')



# Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
  
    template_name = 'CalorieCounter/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        today = timezone.localdate()
        todays_entries = CalorieEntry.objects.filter(user=user, date=today)
        consumed_today = sum(e.calories for e in todays_entries)

        required = profile.required_calories() if profile else None
        remaining = (required - consumed_today) if required is not None else None

        context.update({
            'profile': profile,
            'todays_entries': todays_entries,
            'consumed_today': consumed_today,
            'required_calories': required,
            'remaining_calories': remaining,
            'bmr': profile.calculate_bmr() if profile else None,
            'tdee': profile.calculate_tdee() if profile else None,
            'recent_entries': CalorieEntry.objects.filter(user=user)[:10],
            'today': today,
        })
        
        return context
