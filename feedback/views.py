from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import JsonResponse
from .forms import FeedbackForm
from .models import Feedback, Showroom, UserProfile

# 1. Feedback form view
@login_required
def feedback_form(request):
    # Check if the current user has a profile. If not, create one.
    try:
        _ = request.user.profile
    except UserProfile.DoesNotExist:
        # Create a profile using the first available showroom as default.
        default_showroom = Showroom.objects.first()
        UserProfile.objects.create(user=request.user, showroom=default_showroom)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # Now we safely assign the showroom from the user's profile.
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

# 3. Dashboard view: Renders the dashboard template.
@login_required
def dashboard(request):
    return render(request, 'feedback/dashboard.html')

# 4. Dashboard data: Returns JSON with detailed aggregated feedback and product category data.
@login_required
def dashboard_data(request):
    if request.user.is_superuser:
        # --- For Superusers ---
        # Overall aggregated breakdown for "How Did You Hear About Us" (for pie chart)
        aggregated_feedback_data = list(
            Feedback.objects.values('how_did_you_hear').annotate(count=Count('id'))
        )
        
        # Overall aggregated data for Product Categories
        aggregated_category_data = list(
            Feedback.objects.values('category').annotate(count=Count('id'))
        )
        
        # Detailed breakdown by showroom for "How Did You Hear About Us"
        detailed_feedback_qs = Feedback.objects.values('showroom__name', 'how_did_you_hear') \
                                      .annotate(count=Count('id')).order_by('showroom__name')
        detailed_feedback_data = {}
        for entry in detailed_feedback_qs:
            showroom = entry['showroom__name']
            source = entry['how_did_you_hear']
            count = entry['count']
            if showroom not in detailed_feedback_data:
                detailed_feedback_data[showroom] = {}
            detailed_feedback_data[showroom][source] = count

        # Detailed breakdown by showroom for Product Categories
        detailed_category_qs = Feedback.objects.values('showroom__name', 'category') \
                                               .annotate(count=Count('id')) \
                                               .order_by('showroom__name', 'category')
        detailed_category_data = {}
        for entry in detailed_category_qs:
            showroom = entry['showroom__name']
            cat = entry['category']
            count = entry['count']
            if showroom not in detailed_category_data:
                detailed_category_data[showroom] = {}
            detailed_category_data[showroom][cat] = count

        data = {
            'is_superuser': True,
            'aggregated_feedback_data': aggregated_feedback_data,   # For overall pie chart ("How Did You Hear About Us")
            'aggregated_category_data': aggregated_category_data,   # For overall pie chart (Product Categories)
            'detailed_feedback_data': detailed_feedback_data,       # For grouped bar chart ("How Did You Hear About Us" per showroom)
            'detailed_category_data': detailed_category_data        # For grouped bar chart (Product Categories per showroom)
        }
    else:
        # --- For Operators (Non‑Superusers) ---
        aggregated_feedback_data = list(
            Feedback.objects.filter(showroom=request.user.profile.showroom)
            .values('how_did_you_hear')
            .annotate(count=Count('id'))
        )
        aggregated_category_data = list(
            Feedback.objects.filter(showroom=request.user.profile.showroom)
            .values('category')
            .annotate(count=Count('id'))
        )
        data = {
            'is_superuser': False,
            'feedback_count_data': aggregated_feedback_data,  # For the operator's overall "How Did You Hear About Us" pie chart
            'category_data': aggregated_category_data           # For the operator's Product Category pie chart
        }
    return JsonResponse(data)

# 5. Customer Lookup view:
@login_required
def customer_lookup(request):
    """
    Given a customer_name as a GET parameter, returns existing details 
    (if any) to auto-populate the feedback form fields.
    """
    customer_name = request.GET.get('customer_name', '').strip()
    if customer_name:
        # Search for an existing feedback with matching customer_name (case-insensitive)
        feedback = Feedback.objects.filter(customer_name__iexact=customer_name).first()
        if feedback:
            data = {
                'gender': feedback.gender,
                'company_name': feedback.company_name,
                'phone_number': feedback.phone_number,
                'email_address': feedback.email_address,
            }
            return JsonResponse(data)
    return JsonResponse({})

# 6. Custom login view to allow switching showrooms.
class SwitchShowroomLoginView(LoginView):
    template_name = 'feedback/login.html'

    def dispatch(self, request, *args, **kwargs):
        # If the user is already logged in, log them out to allow showroom switching.
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
