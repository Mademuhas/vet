from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect, reverse


# Create your models here.
class User(AbstractUser):
    SOURCE_CHOICES = (
        ('Super Admin','Super Admin'),
        ('Funcionario','Funcionario'),
        ('Cliente','Cliente')
    )
    email = models.EmailField(max_length=254)
    nome = models.CharField(max_length=55, null=True, blank=True, default=None)
    tel = models.CharField(max_length=55, null=True, blank=True, default=None)
    role = models.CharField(max_length=55, choices=SOURCE_CHOICES, default='Super Admin')
    
    def __str__(self):
        return f"{self.nome}"


class Imprimir(models.Model):
    pedidos = models.ManyToManyField("Pedido", related_name='imprimir')

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome}"

class Card(models.Model):
    SOURCE_CHOICES = (
        ('Sim', 'Sim'),
        ('Nao', 'Nao'),
    )
    produto = models.ForeignKey('Produto', related_name='card_produto', on_delete=models.CASCADE)
    teste = models.CharField(choices=SOURCE_CHOICES, max_length=10, null=True, blank=True, default='Nao')
    quantidade = models.PositiveIntegerField(default=0)
    is_retorno = models.BooleanField(default=False)
    pedido = models.ForeignKey('Pedido', blank=True, null=True, default=None ,related_name='card_pedido', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.produto}"
       
class Pedido(models.Model):


    SOURCE_CHOICES = (
        ('Enviado', 'Enviado'),
        ('Aceito', 'Aceito'),
        ('Em preparo', 'Em preparo'),
        ('Em rota de entrega. Teste de Compatibilidade Pendente', 'Em rota de entrega. Teste de Compatibilidade Pendente'),
        ('Em rota de entrega', 'Em rota de entrega'),
        ('Entregue', 'Entregue'),
        ('Teste Encubado', 'Teste Enbubado'),
        ('Teste Compatível! Livre para transfundir', 'Teste Compatível! Livre para transfundir'),
        ('Pedido Com Cancelamento', 'Pedido Com Cancelamento'),        

    )

    nome = models.CharField(max_length=50)
    status = models.CharField(choices=SOURCE_CHOICES, max_length=55, default='Enviado')
    autor = models.ForeignKey('User', related_name='autor_pedido', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=255, null=True, blank=True, default=None)
    lugar = models.PositiveIntegerField(default=0)
    is_retorno = models.BooleanField(default=False)
    is_teste = models.BooleanField(default=False)
    
    
    @property
    def is_comp(self):
        teste = False
        for card in self.card_pedido.all():
            if card.teste == 'Sim':
                teste = True
        return teste
    




    def __str__(self):
        return f"{self.nome}"
