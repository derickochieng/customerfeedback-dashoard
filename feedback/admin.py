from django.contrib import admin
from .models import Showroom, UserProfile, Feedback

admin.site.register(Showroom)
admin.site.register(UserProfile)
admin.site.register(Feedback)
from django.contrib import admin

admin.site.site_header = "Fairdeals furniture"
admin.site.site_title = "Fairdeals furniture Admin"
admin.site.index_title = "Welcome to fairdeal" 
