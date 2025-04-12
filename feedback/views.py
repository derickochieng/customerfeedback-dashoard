from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import JsonResponse
from .forms import FeedbackForm
from .models import Feedback

# 1. Feedback form view
@login_required
def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # Automatically assign the showroom based on the logged-in user's profile
            feedback.showroom = request.user.profile.showroom
            feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})

# 2. Thank You view
@login_required
def thank_you(request):
    return render(request, 'feedback/thank_you.html')

# 3. Dashboard view: Displays a page with a chart
@login_required
def dashboard(request):
    return render(request, 'feedback/dashboard.html')

# 4. Dashboard data: Returns JSON for AJAX polling on the dashboard
@login_required
def dashboard_data(request):
    is_superuser = request.user.is_superuser
    if is_superuser:
        source_data = list(Feedback.objects.values('showroom__name', 'source').annotate(count=Count('id')))
        showroom_totals = list(Feedback.objects.values('showroom__name').annotate(total=Count('id')))
        data = {
            'source_data': source_data,
            'showroom_totals': showroom_totals,
            'is_superuser': True,
        }
    else:
        source_data = list(
            Feedback.objects.filter(showroom=request.user.profile.showroom)
            .values('source').annotate(count=Count('id'))
        )
        total_count = Feedback.objects.filter(showroom=request.user.profile.showroom).count()
        data = {
            'source_data': source_data,
            'total_count': total_count,
            'is_superuser': False,
        }
    return JsonResponse(data)

# 5. Custom login view to allow switching showrooms
class SwitchShowroomLoginView(LoginView):
    template_name = 'feedback/login.html'

    def dispatch(self, request, *args, **kwargs):
        # If user is already logged in, log them out to allow showroom switching
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
