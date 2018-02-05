from django import forms

class DfColumnForm(forms.Form):

        df_columns = forms.ChoiceField(
        label='df_columns',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        required=True,
    )
        df_date = forms.ChoiceField(
        label='df_date',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        required=True,
    )
        df_budget = forms.IntegerField(
        label='df_budget',
        #default=int(1000),
        required=True,
    )
        df_goal = forms.ChoiceField(
        label='df_goal',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        required=True,
    )
        df_control = forms.ChoiceField(
        label='df_control',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        required=True,
    )
                
                