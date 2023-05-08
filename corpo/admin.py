from django.contrib import admin
from .models import (
    User,
    Pedido, 
    Produto,
    Card,
)
# Register your models here.
admin.site.register(User)
admin.site.register(Pedido)
admin.site.register(Produto)
admin.site.register(Card)