from django.contrib import admin
from .models import Showroom, UserProfile, Feedback

class FeedbackAdmin(admin.ModelAdmin):
    # Define the order of fields to appear in the admin form
    fields = [
        'customer_name',      # first field
        'gender',             # second field
        'company_name',
        'phone_number',
        'email_address',
        'interested_in',
        'category',
        'specific_products',
        'sale_closed',
        'deal_worth',
        'quotation_issued',
        'follow_up_date',
        'how_did_you_hear',
        'birthday',
        'showroom',  # Auto-assigned; include if needed for context
    ]
    
    # Customize the list view for quick scanning of feedback entries
    list_display = ('customer_name', 'gender', 'created_at', 'showroom')
    readonly_fields = ('created_at',)  # Prevent editing of auto-generated timestamp

admin.site.register(Showroom)
admin.site.register(UserProfile)
admin.site.register(Feedback, FeedbackAdmin)

admin.site.site_header = "Fairdeals furniture"
admin.site.site_title = "Fairdeals furniture Admin"
admin.site.index_title = "Welcome to fairdeal"
