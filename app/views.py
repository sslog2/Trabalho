# Imports do Python
import calendar
from datetime import datetime
from typing import Any

# Imports de bibliotecas externas
import requests

# Imports do Django
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.views.generic import (
    TemplateView, FormView, CreateView, DeleteView, 
    DetailView, ListView, UpdateView
)

# Imports de módulos do projeto
from .models import Jogador, Personagem, Evento, Spell
from .forms import PersonagemForm, JogadorForm, LoginForm, EventoForm, EventoFormSet,  SpellForm

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'  # Redireciona para a página inicial ou outro local após login bem-sucedido

    def form_valid(self, form):
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']
        usuario = authenticate(self.request, username=email, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect(self.get_success_url())  # Redireciona para a URL configurada em success_url
        else:
            return self.form_invalid(form)

@login_required
def calendario_view(request):
    # Obter o ano e mês selecionados ou o atual
    today = datetime.today()
    year = today.year
    month = today.month

    if request.GET.get('month'):
        month = int(request.GET.get('month'))

    # Obter os meses do ano para o select box
    months = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]
    
    # Obter eventos para o mês selecionado
    eventos = Evento.objects.filter(data_evento__year=year, data_evento__month=month)

    # Organizar os eventos por dia
    event_days = {}
    for event in eventos:
        day = event.data_evento.day
        if day not in event_days:
            event_days[day] = []
        event_days[day].append(event)

    # Converter o dicionário para uma lista de tuplas (dia, lista de eventos)
    event_days_list = [(day, events) for day, events in event_days.items()]

    # Preparar o calendário do mês
    cal = calendar.Calendar(firstweekday=6)  # Semana começa no domingo
    days = cal.monthdayscalendar(year, month)

    # Criar a estrutura do calendário com eventos
    calendar_with_events = []
    for week in days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                # Adiciona o dia e os eventos para esse dia
                week_data.append({
                    'day': day,
                    'events': event_days.get(day, [])
                })
        calendar_with_events.append(week_data)

    # Obter o nome do mês
    month_name = months[month - 1][1]

    # Criar o formulário de evento (para quando o formulário for submetido)
    if request.method == 'POST':
        evento_form = EventoForm(request.POST)
        if evento_form.is_valid():
            evento_form.save()
            return redirect('app:calendario')  # Redireciona de volta para a página do calendário
    else:
        evento_form = EventoForm()

    # Passar as variáveis para o template
    return render(request, 'calendario.html', {
        'calendar': calendar_with_events,
        'year': year,
        'month': month,
        'month_name': month_name,
        'selected_month': month,
        'months': months,
        'event_days': event_days_list,  # Passando a lista de eventos por dia
        'jogadores': Jogador.objects.all(),
        'personagens': Personagem.objects.all(),
        'evento_form': evento_form,  # Formulário de criação de evento
    })

def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        evento.delete()
        return redirect('app:calendario')  # Redireciona para a página do calendário

    return render(request, 'app/excluir_evento.html', {'evento': evento})

def fetch_spells_from_api():
    base_url = 'https://www.dnd5eapi.co'  # A base da URL da API
    url = f'{base_url}/api/spells'
    
    response = requests.get(url)
    data = response.json()
    
    for spell_data in data['results']:
        spell_url = f'{base_url}{spell_data["url"]}'  # Completa a URL do feitiço
        Spell.objects.get_or_create(name=spell_data['name'], url=spell_url)

@login_required
# View para listar as magias
def spell_list(request):
    spells = Spell.objects.all()
    return render(request, 'spell_list.html', {'spells': spells})

@login_required
# View para detalhes de uma magia
def spell_detail(request, spell_id):
    spell = Spell.objects.get(id=spell_id)
    response = requests.get(spell.url)
    spell_data = response.json()
    return render(request, 'spell_detail.html', {'spell': spell_data})

# Jogador Views
class JogadorListView(LoginRequiredMixin, ListView):
    model = Jogador
    template_name = 'jogador/jogador_list.html'
    context_object_name = 'jogadores'

class JogadorDetailView(LoginRequiredMixin, DetailView):
    model = Jogador
    template_name = 'jogador/jogador_detail.html'
    context_object_name = 'jogador'

class JogadorCreateView(LoginRequiredMixin, CreateView):
    model = Jogador
    form_class = JogadorForm
    template_name = 'jogador/jogador_create.html'
    success_url = reverse_lazy('app:adicionar_jogador')

class JogadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Jogador
    form_class = JogadorForm
    template_name = 'jogador/jogador_update.html'
    success_url = reverse_lazy('app:lista_jogador')

class JogadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Jogador
    template_name = 'jogador/jogador_delete.html'
    success_url = reverse_lazy('app:lista_jogador')


# Personagem Views
class PersonagemListView(LoginRequiredMixin, ListView):
    model = Personagem
    template_name = 'personagem/lista_personagem.html'
    context_object_name = 'personagens'

class PersonagemDetailView(LoginRequiredMixin, DetailView):
    model = Personagem
    template_name = 'personagem/detalhe_personagem.html'
    context_object_name = 'personagem'

class PersonagemCreateView(LoginRequiredMixin, CreateView):
    model = Personagem
    form_class = PersonagemForm
    template_name = 'personagem/adicionar_personagem.html'
    success_url = reverse_lazy('app:adicionar_personagem')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Adiciona dados adicionais ao formulário (como classes e raças)
        try:
            response_classes = requests.get("https://www.dnd5eapi.co/api/classes/")
            kwargs['classes'] = response_classes.json().get('results', [])
        except requests.RequestException:
            kwargs['classes'] = []

        try:
            response_racas = requests.get("https://www.dnd5eapi.co/api/races/")
            kwargs['racas'] = response_racas.json().get('results', [])
        except requests.RequestException:
            kwargs['racas'] = []

        kwargs['jogadores'] = Jogador.objects.all()
        return kwargs

class PersonagemUpdateView(LoginRequiredMixin, UpdateView):
    model = Personagem
    form_class = PersonagemForm
    template_name = 'personagem/editar_personagem.html'
    success_url = reverse_lazy('app:lista_personagem')

    def get_form_kwargs(self):
        # Obtém os argumentos do formulário padrão
        kwargs = super().get_form_kwargs()
        
        # Adiciona dados adicionais ao formulário, como classes e raças da API
        try:
            response_classes = requests.get("https://www.dnd5eapi.co/api/classes/")
            kwargs['classes'] = response_classes.json().get('results', [])
        except requests.RequestException:
            kwargs['classes'] = []

        try:
            response_racas = requests.get("https://www.dnd5eapi.co/api/races/")
            kwargs['racas'] = response_racas.json().get('results', [])
        except requests.RequestException:
            kwargs['racas'] = []

        # Passa os jogadores para o formulário
        kwargs['jogadores'] = Jogador.objects.all()
        
        return kwargs

class PersonagemDeleteView(LoginRequiredMixin, DeleteView):
    model = Personagem
    template_name = 'personagem/personagem_delete.html'
    success_url = reverse_lazy('app:lista_personagem')
