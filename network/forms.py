from django import forms

class PostForm(forms.Form):
    body = forms.CharField(label="", widget=forms.Textarea)
    body.widget.attrs.update({'class': 'form-control compose__body'})
    body.widget.attrs.update({'placeholder': 'Say something!'})
    body.widget.attrs.update({'rows':'3', 'cols':''})