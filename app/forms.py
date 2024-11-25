from django import forms
from .models import Personagem, Jogador, Evento, Spell
from django.forms import modelformset_factory
from django import forms

class EventoForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Evento', 'rows': 3}),
        required=False
    )
    jogadores = forms.ModelMultipleChoiceField(
        queryset=Jogador.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    personagem = forms.ModelMultipleChoiceField(
        queryset=Personagem.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    data_evento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    hora_evento = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        required=True
    )

    class Meta:
        model = Evento
        fields = ['descricao', 'jogadores', 'personagem', 'data_evento', 'hora_evento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modificando a representação do campo 'personagem' para exibir nome do personagem + jogador
        self.fields['personagem'].queryset = Personagem.objects.all()  # Obtenha todos os personagens

        # Alterando as opções no campo 'personagem' para mostrar o nome do personagem e o nome do jogador
        self.fields['personagem'].widget.choices = [
            (p.id, f"{p.nome} (Jogador: {p.jogador.nome})") for p in self.fields['personagem'].queryset
        ]


# FormSet para Evento (opcional, se você deseja criar múltiplos eventos ao mesmo tempo)
EventoFormSet = modelformset_factory(Evento, form=EventoForm, extra=1)

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha'}))

class JogadorForm(forms.ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'email']
JogadorFormSet = modelformset_factory(Jogador, form=JogadorForm)

class ImagemForm(forms.Form):
    imagem = forms.ImageField()

class PersonagemForm(forms.ModelForm):
    classe = forms.ChoiceField(choices=[])  
    raca = forms.ChoiceField(choices=[])
    nivel = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 21)])
    class Meta:
        model = Personagem
        fields = ['nome', 'classe', 'raca', 'nivel', 'jogador']

    def __init__(self, *args, **kwargs):
        classes = kwargs.pop('classes', [])  
        racas = kwargs.pop('racas', [])
        jogadores = kwargs.pop('jogadores', [])  
        super().__init__(*args, **kwargs)
        self.fields['classe'].choices = [(c['index'], c['name']) for c in classes]
        self.fields['raca'].choices = [(r['index'], r['name']) for r in racas]
        self.fields['jogador'].queryset = Jogador.objects.filter(id__in=[j.id for j in jogadores])

class SpellForm(forms.ModelForm):
    class Meta:
        model = Spell
        fields = ['name', 'url']