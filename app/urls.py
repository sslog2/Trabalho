from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'

urlpatterns = [
    # Jogador URLs
    path('jogadores/', views.JogadorListView.as_view(), name='lista_jogador'),
    path('jogadores/<int:pk>/', views.JogadorDetailView.as_view(), name='detalhe_jogador'),
    path('jogadores/adicionar/', views.JogadorCreateView.as_view(), name='adicionar_jogador'),
    path('jogadores/<int:pk>/editar/', views.JogadorUpdateView.as_view(), name='editar_jogador'),
    path('jogadores/<int:pk>/excluir/', views.JogadorDeleteView.as_view(), name='excluir_jogador'),

    # Personagem URLs
    path('personagens/', views.PersonagemListView.as_view(), name='lista_personagem'),
    path('personagens/<int:pk>/', views.PersonagemDetailView.as_view(), name='detalhe_personagem'),
    path('personagens/adicionar/', views.PersonagemCreateView.as_view(), name='adicionar_personagem'),
    path('personagens/<int:pk>/editar/', views.PersonagemUpdateView.as_view(), name='editar_personagem'),
    path('personagens/<int:pk>/excluir/', views.PersonagemDeleteView.as_view(), name='excluir_personagem'),

    # URL de login e logout
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('excluir_evento/<int:evento_id>/', views.excluir_evento, name='excluir_evento'),
    path('spell_list', views.spell_list, name='spell_list'),
    path('spell/<int:spell_id>/', views.spell_detail, name='spell_detail'),
]