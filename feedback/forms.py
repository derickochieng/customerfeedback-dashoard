from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    # Override these fields to force an active choice.
    sale_closed = forms.TypedChoiceField(
        label='Sale Closed',
        choices=[('', 'Select an option'), ('True', 'Yes'), ('False', 'No')],
        coerce=lambda x: x == 'True',
        required=True,
        widget=forms.RadioSelect,
        error_messages={'required': 'Please indicate if the sale is closed.'}
    )
    quotation_issued = forms.TypedChoiceField(
        label='Quotation Issued',
        choices=[('', 'Select an option'), ('True', 'Yes'), ('False', 'No')],
        coerce=lambda x: x == 'True',
        required=True,
        widget=forms.RadioSelect,
        error_messages={'required': 'Please indicate if a quotation was issued.'}
    )

    class Meta:
        model = Feedback
        fields = [
            'customer_name',      
            'gender',             
            'company_name',        # Optional
            'phone_number',        # Optional
            'email_address',       # Optional
            'interested_in',       # Choice (e.g., Home / Office)
            'category',            # Required
            'deal_worth',          # Optional numeric value
            'follow_up_date',      # Optional date
            'how_did_you_hear',    # Field for the source – to be labeled below
            'specific_products',   # Added field (make sure your model has this field)
            'birthday',            # Optional date
        ]
        labels = {
            'how_did_you_hear': 'How Did You Hear About Us',
        }
        # We are handling sale_closed and quotation_issued as custom fields,
        # so they are not re-specified in Meta's widgets.
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark required fields for which the operator must input a value:
        self.fields['customer_name'].required = True
        self.fields['gender'].required = True
        self.fields['category'].required = True
        self.fields['how_did_you_hear'].required = True
        # Set custom error messages.
        self.fields['customer_name'].error_messages = {'required': 'Please enter the customer name.'}
        self.fields['gender'].error_messages = {'required': 'Please select a gender.'}
        self.fields['category'].error_messages = {'required': 'Please select a product category.'}
        self.fields['how_did_you_hear'].error_messages = {'required': 'Please indicate how the customer heard about us.'}
