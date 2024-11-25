from django.db import models

class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True,default='jogador@email.com')

    def __str__(self):
        return self.nome

class Personagem(models.Model):
    nome = models.CharField(max_length=100)
    classe = models.CharField(max_length=50)
    nivel = models.IntegerField()
    jogador = models.ForeignKey(Jogador, related_name='personagens', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - Classe: {self.classe}, Nível: {self.nivel}"

class Evento(models.Model):
    descricao = models.TextField(null=True, blank=True)
    jogadores = models.ManyToManyField(Jogador, blank=True)  # Relacionamento com múltiplos jogadores
    personagem = models.ManyToManyField(Personagem, blank=True)  # Relacionamento com múltiplos personagens
    data_evento = models.DateField(null=True, blank=True)
    hora_evento = models.TimeField(null=True, blank=True)

    def __str__(self):
        # Contagem de jogadores e nomes dos personagens
        personagens_nomes = ', '.join([p.nome for p in self.personagem.all()])
        return f"Evento com {self.jogadores.count()} jogadores para {personagens_nomes} em {self.data_evento}"

class Spell(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name