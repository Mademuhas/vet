from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
import csv
from .models import (
    User, Produto, Pedido, Card
)
from .forms import (
    CustomUserCreationForm, ProdutoCreationForm, PedidoCreationForm, CardCreationForm, PedidoAdmUpdateForm, CardUpdateForm, CardFormSet
)
# Create your views here.
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class USerCreateView(generic.CreateView):
    template_name = 'user_create.html'
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("user-list")

class UserListView(generic.ListView):
    template_name = "user_list.html"
    paginate_by = 20
    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            queryset = User.objects.filter(username__icontains=search)
        else:
            queryset = User.objects.all()
        return queryset
    
class UserDetailView(generic.DetailView):
    template_name = "user_detail.html"
    def get_queryset(self):
        return User.objects.filter()
    
class UserDeleteView(generic.DeleteView):
    template_name = "user_delete.html"
    
    def get_queryset(self):
        return User.objects.filter()
    
    def get_success_url(self):
        return reverse("user-list")
    
class UserUpdateView(generic.UpdateView):
    template_name = "user_update.html"
    form_class = CustomUserCreationForm
    
    def get_queryset(self):
        return User.objects.filter()
    
    def get_success_url(self):
        return reverse("user-list")

########## Produtosss ########


class ProdutoCreateView(generic.CreateView):
    template_name = 'produto_create.html'
    form_class = ProdutoCreationForm
    
    def get_success_url(self):
        return reverse("produto-list")

class ProdutoListView(generic.ListView):
    template_name = "produto_list.html"
    paginate_by = 20
    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            queryset = Produto.objects.filter(Q(nome__icontains=search) | Q(pk__icontains=search))
        else:
            queryset = Produto.objects.all()
        return queryset
    
class ProdutoDetailView(generic.DetailView):
    template_name = "produto_detail.html"
    def get_queryset(self):
        return Produto.objects.filter()
    
class ProdutoDeleteView(generic.DeleteView):
    template_name = "produto_delete.html"
    
    def get_queryset(self):
        return Produto.objects.filter()
    
    def get_success_url(self):
        return reverse("produto-list")
    
class ProdutoUpdateView(generic.UpdateView):
    template_name = "produto_update.html"
    form_class = ProdutoCreationForm
    
    def get_queryset(self):
        return Produto.objects.filter()
    
    def get_success_url(self):
        return reverse("produto-list")
    
    ######## Pedido ?#############
class PedidoListView(generic.ListView):
    template_name = "pedido_list.html"
    paginate_by = 20
    def get_queryset(self):
        search = self.request.GET.get('search')
        toggle = self.request.GET.get('toggle')
        filter = self.request.GET.get('filter')
        if search:
            if self.request.user.role == 'Super Admin' or self.request.user.role == 'Funcionario':
                queryset = Pedido.objects.filter(nome__icontains=search)
            else:
                queryset = Pedido.objects.filter(Q(autor=self.request.user) & Q(nome__icontains=search) )
        elif filter:
            if self.request.user.role == 'Cliente':
                queryset = Pedido.objects.filter(Q(autor=self.request.user) & Q(status=filter))
            else:
                queryset = Pedido.objects.filter(status=filter)
                
        else:
            if self.request.user.role == 'Super Admin' or self.request.user.role == 'Funcionario':
                if filter:
                    queryset = Pedido.objects.filter(Q(status=filter))
                else:
                    queryset = Pedido.objects.filter(~Q(status='Pendente')).order_by('-pk')
            else:   
                queryset = Pedido.objects.filter(autor=self.request.user).order_by('-data')
          
        return queryset
    
class PedidoDetailView(generic.DetailView):
    template_name = "pedido_detail.html"
    def get_queryset(self):
        cancel = self.request.GET.get('cancel')
        pagr = self.request.GET.get('pagr')
        pagl = self.request.GET.get('pagl')
        if cancel:
            Card.objects.filter(pk=cancel).update(is_retorno=True)
            aux = Card.objects.get(pk=cancel)
            ped = aux.pedido
            valor = ped.pk
            Pedido.objects.filter(pk=valor).update(status='Pedido Com Cancelamento')
        if pagr:
            aux = Pedido.objects.get(pk=pagr)
            for obj in aux.card_pedido.all():
                if obj.teste == 'Sim':
                    Pedido.objects.filter(pk=pagr).update(is_teste=True)
            st = aux.status
            teste = aux.is_teste
            if teste:
                if st == 'Pedido Com Cancelamento':
                    Pedido.objects.filter(pk=pagr).update(status='Em Preparo')
                if st == 'Enviado':
                    Pedido.objects.filter(pk=pagr).update(status='Aceito')
                if st == 'Aceito':
                    Pedido.objects.filter(pk=pagr).update(status='Em Preparo')
                if st == 'Em Preparo':
                    Pedido.objects.filter(pk=pagr).update(status='Em rota de entrega. Teste de Compatibilidade Pendente')
                if st == 'Em rota de entrega. Teste de Compatibilidade Pendente':
                    Pedido.objects.filter(pk=pagr).update(status='Teste Encubado')
                if st == 'Teste Encubado':
                    Pedido.objects.filter(pk=pagr).update(status='Teste Compatível! Livre para transfundir')                   
            else:
                if st == 'Pedido Com Cancelamento':
                    Pedido.objects.filter(pk=pagr).update(status='Em Preparo')
                if st == 'Enviado':
                    Pedido.objects.filter(pk=pagr).update(status='Aceito')
                if st == 'Aceito':
                    Pedido.objects.filter(pk=pagr).update(status='Em Preparo')
                if st == 'Em Preparo':
                    Pedido.objects.filter(pk=pagr).update(status='Em rota de entrega')
                if st == 'Em rota de entrega':
                    Pedido.objects.filter(pk=pagr).update(status='Entregue')

        if pagl:
            aux = Pedido.objects.get(pk=pagl)
            for obj in aux.card_pedido.all():
                if obj.teste == 'Sim':
                    Pedido.objects.filter(pk=pagl).update(is_teste=True)
            st = aux.status
            teste = aux.is_teste
            if teste:
                if st == 'Teste Compatível! Livre para transfundir':
                    Pedido.objects.filter(pk=pagl).update(status='Teste Encubado')
                if st == 'Teste Encubado':
                    Pedido.objects.filter(pk=pagl).update(status='Em rota de entrega. Teste de Compatibilidade Pendente')
                if st == 'Em rota de entrega. Teste de Compatibilidade Pendente':
                    Pedido.objects.filter(pk=pagl).update(status='Em Preparo')
                if st == 'Em Preparo':
                    Pedido.objects.filter(pk=pagl).update(status='Aceito')
                if st == 'Aceito':
                    Pedido.objects.filter(pk=pagl).update(status='Enviado')

            else:
                if st == 'Aceito':
                    Pedido.objects.filter(pk=pagl).update(status='Enviado')
                if st == 'Em Preparo':
                    Pedido.objects.filter(pk=pagl).update(status='Aceito')
                if st == 'Em rota de entrega':
                    Pedido.objects.filter(pk=pagl).update(status='Em Preparo')
                if st == 'Em rota de entrega':
                    Pedido.objects.filter(pk=pagl).update(status='Em Preparo') 
                if st == 'Entregue':
                    Pedido.objects.filter(pk=pagl).update(status='Em rota de entrega')                   
            
        queryset = Pedido.objects.filter()
        return queryset
    
class PedidoCreateView(generic.CreateView):
    template_name = "pedido_create.html"
    form_class = PedidoCreationForm

    def get_context_data(self, **kwargs):
        data = super(PedidoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['card'] = CardFormSet(self.request.POST)
        else:
            data['card'] = CardFormSet()
        return data


    def form_valid(self, form):
        context = self.get_context_data(form = form)
        formset = context['card']
        form.instance.autor = self.request.user
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        return super(PedidoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('pedido-list')




class PedidoAdmUpdateView(generic.UpdateView):
    template_name = "pedido_adm_update.html"
    form_class = PedidoAdmUpdateForm

    def get_queryset(self):
        return Pedido.objects.filter()



class PedidoDeleteView(generic.DeleteView):
    template_name = 'pedido_delete.html'
    def get_queryset(self):
        return Pedido.objects.filter()
    
    def get_success_url(self):
        return reverse("pedido-list")
class CardCreateView(generic.CreateView):
    template_name = "card_create.html"
    form_class = CardCreationForm
    
    def form_valid(self, form):
        form.instance.pedido = Pedido.objects.get(pk = self.kwargs['pk'])
        return super(CardCreateView, self).form_valid(form)

class CardUpdateView(generic.UpdateView):
    template_name = "card_update.html"
    form_class = CardUpdateForm
    def get_queryset(self):
        return Card.objects.filter()



class CardDeleteView(generic.DeleteView):
    template_name = "card_delete.html"

    def get_success_url(self):
        return reverse('pedido-detail', kwargs={"pk": self.object.pedido.pk})
    
    def get_queryset(self):
        return Card.objects.filter()


def pedido_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=import.csv'
    writer = csv.writer(response)

    pedidos = Pedido.objects.all()
    writer.writerow(['Pedido', 'Status', 'Empresa', 'Data', 'Item', 'Quantidade', 'Teste'])
    for pedido in pedidos :
        for card in pedido.card_pedido.all():
            writer.writerow([pedido.nome, pedido.status, pedido.autor, pedido.data.strftime("%Y-%m-%d"), card.produto, card.quantidade, card.teste])

    return response