from django import forms

class CreateListingForm(forms.Form):
    title           = forms.CharField(label="Item Name", max_length=100)
    description     = forms.CharField(label="Item Description", max_length=500)
    starting_price  = forms.DecimalField(decimal_places=2)
    image           = forms.URLField(label="image URL (Optional)", required=False)

class CreateBid(forms.Form):
    bid = forms.DecimalField(decimal_places=2)