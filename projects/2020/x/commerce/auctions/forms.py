from django import forms
from .models import Categories

class CreateListingForm(forms.Form):
    
    title           = forms.CharField(label="Item Name", max_length=100, widget=forms.TextInput(attrs={
        'class' : 'form-control col-md-4 mb-3',
        'type' : 'text'
        }))
    description     = forms.CharField(label="Item Description", max_length=500, widget=forms.Textarea(attrs={
        'class' : 'form-control col-md-6',
        'rows' : 5
        }))
    starting_price  = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={
        'class' : 'form-control col-md-2 mb-3',
        'type' : 'text'
        }))
    image           = forms.URLField(label="Image URL (Optional)", required=False, widget=forms.URLInput(attrs={
        'class' : 'form-control col-md-4 mb-3',
        # 'type' : 'text'
        }))
    category        = forms.ChoiceField(label="Choices", choices=Categories.CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class' : 'form-control col-md-2 mb-3'}))

class CreateBid(forms.Form):
    bid = forms.DecimalField(decimal_places=2)

class CreateComment(forms.Form):
    comment = forms.CharField(max_length=600, widget=forms.Textarea)

