from django.db import models
from django.contrib.auth.models import User

# 1. Showroom Model
class Showroom(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

# 2. UserProfile Model: Links a Django User to a Showroom
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"

# --- New Choice Fields for the updated Feedback Model ---
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

INTEREST_CHOICES = [
    ('home', 'Home'),
    ('office', 'Office'),
]

CATEGORY_CHOICES = [
    ('sofa_set', 'Sofa Set'),
    ('dining_sets', 'Dining Sets'),
    ('console_cabinet_coffee', 'Console/Cabinet/Coffee Table'),
    ('bedroom_sets', 'Bedroom Sets'),
    ('accessories', 'Accessories'),
    ('mattresses', 'Mattresses'),
    ('office_chairs', 'Office Chairs'),
    ('office_tables', 'Office Tables'),
    ('workstations', 'Workstations'),
    ('filing_cabinets', 'Filing Cabinets'),
    ('safes', 'Safes'),
    ('link_chairs', 'Link Chairs'),
    ('office_sofas', 'Office Sofas'),
    ('reception_desks', 'Reception Desks'),
    ('customization', 'Customization'),
]

HEAR_ABOUT_CHOICES = [
    ('social_media', 'Social Media'),
    ('influencers', 'Influencers'),
    ('outdoor_media', 'Outdoor Media'),
    ('newsletter', 'Newsletter/Email'),
    ('word_of_mouth', 'Word of Mouth'),
    ('sms', 'SMS'),
    ('repeat_customer', 'Repeat Customer'),
]

# 3. Feedback Model: Updated to include additional customer details
class Feedback(models.Model):
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    
    # Customer details
    customer_name = models.CharField(max_length=255, default="Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    
    # Interest and Product details
    interested_in = models.CharField(max_length=10, choices=INTEREST_CHOICES, default="home")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="sofa_set")
    specific_products = models.CharField(max_length=255, blank=True, null=True)
    # Sales details
    sale_closed = models.BooleanField(default=False)
    deal_worth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quotation_issued = models.BooleanField(default=False)
    
    # Follow-up and additional info
    follow_up_date = models.DateField(blank=True, null=True)
    how_did_you_hear = models.CharField(max_length=50, choices=HEAR_ABOUT_CHOICES, default="social_media")
    birthday = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.customer_name} - {self.showroom.name}"
