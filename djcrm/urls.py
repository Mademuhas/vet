"""djcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from corpo.views import (
    LandingPageView, USerCreateView, UserListView, UserDeleteView, UserDetailView, UserUpdateView, ProdutoCreateView, ProdutoDeleteView, ProdutoListView, ProdutoUpdateView, ProdutoDetailView,
    CardCreateView, PedidoCreateView, PedidoDetailView, PedidoListView, pedido_csv, PedidoDeleteView, PedidoAdmUpdateView, CardDeleteView, CardUpdateView,
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing'),
    ###### Usuarios ########
    path('user/create', USerCreateView.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/list', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/update', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name='user-delete'),
    ######## Produtos #########
    path('produto/list', ProdutoListView.as_view(), name='produto-list'),
    path('produto/<int:pk>', ProdutoDetailView.as_view(), name='produto-detail'),
    path('produto/<int:pk>/update', ProdutoUpdateView.as_view(), name='produto-update'),
    path('produto/<int:pk>/delete', ProdutoDeleteView.as_view(), name='produto-delete'),
    path('produto/create', ProdutoCreateView.as_view(), name='produto-create'),
    ######### Pedido ##############
    path('pedido/list', PedidoListView.as_view(), name='pedido-list'),
    path('pedido/<int:pk>', PedidoDeleteView.as_view(), name='pedido-delete'),
    path('pedido/create', PedidoCreateView.as_view(), name='pedido-create'),
    path('pedidoadm/<int:pk>/update', PedidoAdmUpdateView.as_view(), name='pedidoadm-update'),
    path('pedido/<int:pk>/detail', PedidoDetailView.as_view(), name='pedido-detail'),
    path('card/create/<int:pk>', CardCreateView.as_view(), name='card-create'),
    path('card/update/<int:pk>', CardUpdateView.as_view(), name='card-update'),
    path('card/delete/<int:pk>', CardDeleteView.as_view(), name='card-delete'),
    path('pedido_csv', pedido_csv, name='pedido-csv'),            
]
