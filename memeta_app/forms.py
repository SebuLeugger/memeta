from django import forms
from .models import CardFront, CardBack, Card, Preferences, Rep



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
        fields = ('courses',)# 'user')
        labels = {
            'courses': '',
        }
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),#attrs={'class': 'form-check'}), #irgendwie müsste es in ein form-check div rein und im label müsste dann die class form-check-label sein  #bootstrap macht das komisch mit diesen checkboxes..., es setzt sie auf eine zeile über der options-beschreibung
#            'user': forms.TextInput(attrs={'value': '', 'id': 'user_auto', 'type': 'hidden'}),
        }

class ChangePreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('courses',)
        labels = {
            'courses': '',
        }
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),#attrs={'class': 'form-check-label'}),
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
