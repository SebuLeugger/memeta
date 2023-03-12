from django import forms
from .models import CardFront, CardBack, Card, Preferences, Rep, IllKnow
from bootstrap_datepicker_plus.widgets import DateTimePickerInput



class AddCardFrontForm(forms.ModelForm):
    class Meta:
        model = CardFront
        fields = ('course', 'body',)
        labels = {
            'course': 'Kurs',
            'body': 'Vorderseite',
        }
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Frage, Problem,...'}),
        }

class AddCardBackForm(forms.ModelForm):
    class Meta:
        model = CardBack
        fields = ('body',)
        labels = {
            'body': 'Rückseite',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Antwort, Lösung,...'}),
        }


class AddFrontForm(forms.ModelForm):
    class Meta:
        model = CardFront
        fields = ('course', 'body',)
        labels = {
            'course': 'Kurs',
            'body': 'Vorderseite',
        }
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Frage, Problem,...'}),
        }


class SetPreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('courses',)
        labels = {
            'courses': '',
        }
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }

class ChangePreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('courses',)
        labels = {
            'courses': '',
        }
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }

class RepFrontForm(forms.ModelForm):
    i_know = forms.CharField(  
        label = '',
        widget = forms.RadioSelect(choices=[
            (1, 'Ich weiss, was auf der Rückseite steht'), 
            (0, 'Ich weiss nicht, was auf der Rückseite steht')]),
    )

    class Meta: #diese Meta-Klasse ist obsolet, wenn ich das einzige formfield explizit definiere wie oben. Aber ich lasse es mal so, falls ich es mal noch ändere
        model = Rep
        fields = ('i_know',)
        labels = {
            'i_know': '',
        }
        widgets = {
            'i_know': forms.RadioSelect(choices=[
            (True, 'Ich weiss, was auf der Rückseite steht'), 
            (False, 'Ich weiss nicht, was auf der Rückseite steht')]),
        }


class RepBackForm(forms.ModelForm):
    i_knew = forms.CharField(  
        label = '',
        widget = forms.RadioSelect(choices=[
            (1, 'Ich wusste, was hier steht'), 
            (0, 'Ich wusste nicht, was hier steht')]),
    )

    class Meta: #diese Meta-Klasse ist obsolet, wenn ich das einzige formfield explizit definiere wie oben. Aber ich lasse es mal so, falls ich es mal noch ändere
        model = Rep
        fields = ('i_knew',)
        labels = {
            'i_knew': '',
        }
        widgets = {
            'i_knew': forms.RadioSelect(choices=[
                (True, 'Ich wusste, was hier steht'), 
                (False, 'Ich wusste nicht, was hier steht')
            ]),
        }


class AddIllKnowForm(forms.ModelForm):
    class Meta:
        model = IllKnow
        fields = ('when',)
        labels = {
            'when': '"Was hier steht, kann ich mir merken bis am..."',
        }
        widgets = {
            'when': DateTimePickerInput(options={"format": "DD.MM.YYYY", "useCurrent": True}, attrs={'placeholder': 'Datum auswählen...'}),
        }
        # I'm using dateTIMEpicker but don't let the user choose a time (by not including the time in the "format")
        # Instead I set the time to useCurrent = True. 
        # This way, choosing only the date doesn't automatically set the time to 00:00:00 local time of that chosen date
        # We would still have to round the datetime object UP to the nearest day to get the required amount of days as an integer (23h59min is 0 days...)
        # but since I plan to display the exact timespans of bets in a graph I will not implement this rounding-up properly
        # I'm just hacking it with a timedalta of 10 minutes added to each time difference for frontend display, such that all normal submit delays after timeinput widget uses should be fine