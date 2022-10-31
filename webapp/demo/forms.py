from django import forms
from django.contrib.auth.models import User
from django_freeradius.models import RadiusCheck


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')
        if not username and not password and not email:
            raise forms.ValidationError('You have to write something!')

        # check if email is already taken
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken!')


class ClientDataSubscriptionForm(forms.Form):
    client = forms.ChoiceField(choices=[(client.username, client.username) for client in User.objects.filter(is_superuser=False)])
    attribute_type = forms.ChoiceField(choices=[('Max-Daily-Session', 'Max-Daily-Session'), ('Max-All-Session', 'Max-All-Session'), ('Max-Daily-Session-Traffic', 'Max-Daily-Session-Traffic')])
    operator = forms.ChoiceField(choices=[('=', '='),
                     (':=', ':='),
                     ('==', '=='),
                     ('+=', '+='),
                     ('!=', '!='),
                     ('>', '>'),
                     ('>=', '>='),
                     ('<', '<'),
                     ('<=', '<='),
                     ('=~', '=~'),
                     ('!~', '!~'),
                     ('=*', '=*'),
                     ('!*', '!*')], initial=':=')
    attribute_value = forms.IntegerField(min_value=0) # set to positive integer
    

    def clean(self):
        cleaned_data = super(ClientDataSubscriptionForm, self).clean()
        client = cleaned_data.get('client')
        attribute_type = cleaned_data.get('attribute_type')
        operator = cleaned_data.get('operator')
        attribute_value = cleaned_data.get('attribute_value')
        if not client and not attribute_type and not operator and not attribute_value:
            raise forms.ValidationError('You have to write something!')

        # check if attribute is already taken
        if RadiusCheck.objects.filter(username=client, attribute=attribute_type).exists():
            raise forms.ValidationError('Attribute already taken!')

    def save(self):
        client = self.cleaned_data['client']
        attribute_type = self.cleaned_data['attribute_type']
        operator = self.cleaned_data['operator']
        attribute_value = self.cleaned_data['attribute_value']
        radius_check = RadiusCheck(username=client, attribute=attribute_type, op=operator, value=attribute_value)
        radius_check.save()
        return radius_check



