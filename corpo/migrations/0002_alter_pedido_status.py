# Generated by Django 4.1.5 on 2023-03-01 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('Enviado', 'Enviado'), ('Aceito', 'Aceito'), ('Em preparo', 'Em preparo'), ('Em rota de entrega. Teste de Compatibilidade Pendente', 'Em rota de entrega. Teste de Compatibilidade Pendente'), ('Em rota de entrega', 'Em rota de entrega'), ('Entregue', 'Entregue'), ('Teste Encubado', 'Teste Enbubado'), ('Teste Compatível! Livre para transfundir', 'Teste Compatível! Livre para transfundir'), ('Pedido com item cancelado', 'Pedido com item cancelado')], default='Enviado', max_length=55),
        ),
    ]
