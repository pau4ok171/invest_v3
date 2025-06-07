from django import forms


class SearchListForm(forms.Form):
    query = forms.CharField(label='Query', max_length=50)


class UsernameVerificationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=255)
