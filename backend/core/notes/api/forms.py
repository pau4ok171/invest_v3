from django import forms


class NotesCreateForm(forms.Form):
    company_id = forms.IntegerField(min_value=0)
    content = forms.CharField()


class NotesUpdateForm(forms.Form):
    note_id = forms.IntegerField(min_value=0)
    content = forms.CharField()
    updated = forms.DateTimeField()
