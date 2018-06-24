from django import forms
from .models import Event
from taggit.models import Tag
from django.core.exceptions import ValidationError


class EventForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple(), to_field_name='name')
    place_location_lat = forms.FloatField(widget=forms.HiddenInput(), required=True)
    place_location_lng = forms.FloatField(widget=forms.HiddenInput(), required=True)
    start_date = forms.DateField(label='Start date', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End date', widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def clean(self):
        if (self.cleaned_data['start_date'] >
            self.cleaned_data['end_date']):
            raise ValidationError("Event's end date can't be before start date !")

        return self.cleaned_data

    class Meta:
        model = Event

        fields = ('name', 'description', 'start_date', 'end_date', 'tags', 'place_text', 'place_location_lat', 'place_location_lng',)
        labels = {"name": "Name",
                  "description": "Description",
                  "place_text": "Place",
                  }
