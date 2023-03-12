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
        # if we subtract not the datetime objects themselves from each other but instead the dates of the datetime objects only, we get the intuitively right amount of days in the daydelta functions, even though the daydelta is less than the full multiple of 24h.