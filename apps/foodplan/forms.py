from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.models import inlineformset_factory, modelformset_factory
from . import models


class MDLTextFieldInput(forms.TextInput):
    """
    Overrides default TextInput to ensure that attribute
    'class' always is mdl textfield input
    """
    def __init__(self, *args, **kwargs):
        new_attrs = kwargs.get('attrs', dict())
        new_attrs.update({
            'class': 'mdl-textfield__input'
        })
        kwargs['attrs'] = new_attrs
        super(MDLTextFieldInput, self).__init__(*args, **kwargs)


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
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Meal is already planned for this day",
            }
        }


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


# Form for DinnerPlan that includes DinnerPlanItems inline
ItemFormSet = inlineformset_factory(models.DinnerPlan, models.DinnerPlanItem, form=DinnerPlanForm, extra=0,
                                    can_delete=False,
                                    widgets={
                                        'recipe': forms.Select(attrs={'class': 'hn-food-recipe-select2'}),
                                        'day': forms.Select(attrs={'class': 'hn-food-day-select2'}),
                                        'eaten': forms.CheckboxInput(attrs={'class': 'mdl-checkbox__input'})
                                    })
