from django import forms
from django.forms.models import inlineformset_factory
from . import models


class MDLTextFieldInput(forms.TextInput):
    """
    Overrides default TextInput to ensure that attribute
    'class' always is mdl textfield input
    """
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', dict())
        attrs.update({
            'class': 'mdl-textfield__input'
        })
        super(MDLTextFieldInput, self).__init__(attrs=attrs)


class DinnerPlanForm(forms.ModelForm):
    """
    Form for DinnerPlan Create/Update
    """
    class Meta:
        model = models.DinnerPlan
        exclude = ['end_date']
        widgets = {
            'start_date': MDLTextFieldInput(attrs={
                'placeholder': 'yyyy-mm-dd'
            }),
            'cost': MDLTextFieldInput()
        }

# Form for DinnerPlan that includes DinnerPlanItems inline
ItemFormSet = inlineformset_factory(models.DinnerPlan, models.DinnerPlanItem, form=DinnerPlanForm, extra=0,
                                    can_delete=False,
                                    widgets={
                                        'recipe': forms.Select(attrs={'class': 'recipe-select2'}),
                                        'day': forms.Select(attrs={'class': 'day-select2'}),
                                        'eaten': forms.CheckboxInput(attrs={'class': 'mdl-checkbox__input'})
                                    })


class RecipeForm(forms.ModelForm):
    """
    Form for Recipe Create/Update
    """
    class Meta:
        model = models.Recipe
        fields = ['title', 'url']
        widgets = {
            'title': MDLTextFieldInput(),
            'url': MDLTextFieldInput()
        }
