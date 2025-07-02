from django import forms


class PortfolioCreateForm(forms.Form):
    portfolio_name = forms.CharField()


class PortfolioUpdateForm(forms.Form):
    company_id = forms.IntegerField(min_value=0)
    action = forms.ChoiceField(choices={'include': 'create', 'exclude': 'delete'})
