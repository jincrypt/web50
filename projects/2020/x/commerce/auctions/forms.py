from django import forms
from .models import Categories

class CreateListingForm(forms.Form):
    
    title           = forms.CharField(label="Item Name", max_length=100)
    description     = forms.CharField(label="Item Description", max_length=500)
    starting_price  = forms.DecimalField(decimal_places=2)
    image           = forms.URLField(label="image URL (Optional)", required=False)
    category        = forms.ChoiceField(label="Choices", choices=Categories.CATEGORY_CHOICES, required=False)

class CreateBid(forms.Form):
    bid = forms.DecimalField(decimal_places=2)

class CreateComment(forms.Form):
    comment = forms.CharField(max_length=600, widget=forms.Textarea)

