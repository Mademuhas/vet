from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from django import forms
from .models import Pedido, Produto, Card
from django.utils import timezone
from django.forms.models import inlineformset_factory

User = get_user_model()






class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('nome', 'email', 'tel', 'role', 'username')
        field_classes = {'username': UsernameField}
        
class ProdutoCreationForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ("nome", 'descricao',)

class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('produto', 'quantidade', 'teste', )
class CardUpdateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('produto', 'quantidade', 'teste')

CardFormSet = inlineformset_factory(Pedido, Card, form=CardCreationForm, extra=1)

class PedidoCreationForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('nome',  )

class PedidoAdmUpdateForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
