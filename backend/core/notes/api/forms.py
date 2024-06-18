from django import forms


class NotesCreateForm(forms.Form):
    company_id = forms.IntegerField(min_value=0)
    content = forms.CharField()
    text = forms.CharField(required=False)


class NotesUpdateForm(forms.Form):
    note_id = forms.IntegerField(min_value=0)
    content = forms.CharField()
    text = forms.CharField(required=False)
    updated = forms.DateTimeField()
