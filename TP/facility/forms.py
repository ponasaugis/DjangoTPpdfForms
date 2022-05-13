from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, inlineformset_factory

from .models import Agent, Order, OrderLine, EqModels, Equipement, Types, Project, Manufacturers


class AgentAddForm(ModelForm):
    class Meta:
        model = Agent
        fields = ('first_name', 'last_name', 'ccms_id', 'phone', 'email', 'country', 'city', 'street', 'project_id')
        labels = {
            'first_name': '',
            'last_name': '',
            'ccms_id': '',
            'phone': '',
            'email': '',
            'country': '',
            'city': '',
            'street': '',
            'project_id': 'Select project',
        }

        help_texts = {
            'first_name': None,
            'last_name': None,
            'ccms_id': None,
            'phone': None,
            'email': None,
            'country': None,
            'city': None,
            'street': None,
            'project_id': None,
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'ccms_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CCMS ID'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'street': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter street and apartment number'}),
            'project_id': forms.Select(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'id', 'agent_id', 'comment'
        labels = {'agent_id': '', 'comment': '', }
        help_texts = {'agent_id': None, 'comment': None, }
        widgets = {'agent_id': forms.Select(attrs={'class': 'form-control w-25'}),
                   'comment': forms.Textarea(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs \
            .update({
            'class': 'form-control',
            'placeholder': 'Leave comment if needed',
            'rows': '2',
        })

        self.fields['agent_id'].empty_label = 'Select Agent'


class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ('equipement_id', 'sn', 'status')
        labels = {'equipement_id': '', 'status': '', 'sn': '', }
        help_texts = {'equipement_id': None, 'sn': None, 'status': None, }
        widgets = {'equipement_id': forms.Select(attrs={'class': 'form-control m-2 col'}),
                   'status': forms.Select(attrs={'class': 'form-control m-2 col'}),
                   'sn': forms.TextInput(attrs={'class': 'form-control m-2 col'}), }

    def __init__(self, *args, **kwargs):
        super(OrderLineForm, self).__init__(*args, **kwargs)
        self.fields['sn'].widget.attrs \
            .update({
            'class': 'form-control m-2 col',
            'placeholder': 'Enter Serial Number',
        })
        self.fields['equipement_id'].empty_label = 'Select Equipement'


OrderMetaInLineFormset = inlineformset_factory(
    Order,
    OrderLine,
    form=OrderLineForm,
    extra=5,
    can_delete=False,

)


# ----------------------------------------

class PrettyAuthenticationForm(AuthenticationForm):
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Class based forms-----------------------------------

# class OrderForma(ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#
# OrderlineFormSet = inlineformset_factory(Order, OrderLine, extra=1, fields=('equipement_id', 'sn', 'status'))


class OrderLineInline(ModelForm):
    class Meta:
        model = OrderLine
        fields = ('equipement_id', 'sn', 'status')
        labels = {'equipement_id': '', 'status': '', 'sn': '', }
        help_texts = {'equipement_id': None, 'sn': None, 'status': None, }
        widgets = {'equipement_id': forms.Select(attrs={'class': 'form-control m-0 col'}),
                   'status': forms.Select(attrs={'class': 'form-control m-0 col'}),
                   'sn': forms.TextInput(attrs={'class': 'form-control m-0 col'}), }

    def __init__(self, *args, **kwargs):
        super(OrderLineInline, self).__init__(*args, **kwargs)
        self.fields['sn'].widget.attrs \
            .update({
            'class': 'form-control m-0 col',
            'placeholder': 'Enter Serial Number',
        })
        self.fields['equipement_id'].empty_label = 'Select Equipement'

class OrderForma(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


OrderInlineFormset = inlineformset_factory(Order, OrderLine, form=OrderLineInline, extra=1, can_delete=False, can_order=False, fields ='__all__')

OrderInlineUpdateFormset = inlineformset_factory(Order, OrderLine, form=OrderLineInline, extra=1, can_delete_extra=False, can_order=False, fields =('equipement_id', 'sn', 'status'))