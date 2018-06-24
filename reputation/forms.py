from django import forms


class AddReputationForm(forms.Form):
    POINTS_CHOICES = (
        (-1, 'Negative (-1)'),
        (1, 'Positive (+1)'),
    )

    points = forms.ChoiceField(required=True, choices=POINTS_CHOICES, label="Type:")
    description = forms.CharField(required=False, max_length=200)
