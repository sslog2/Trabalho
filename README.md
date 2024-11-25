# workshop-fabrica-2024.2
Projeto de django de Márcio Souto Maior Sousa, José Matheos Mendonça Farias, Milena Soares

## Sobre o Projeto
- Api de D&D
- Utilizando funções de adicionar_Personagem e adicionar_Jogador
- Excluir Personagem e Jogador
- Utilizando a api D&D para pegar informações de magias, classe, nivel ...
- Agendar sessão de jogo
- Login e logout

## Relação entidade
- Jogador {1,n} ------> Personagem
- Personagem {n,1} --------> Jogador

## Tecnologias Utilizadas
* [Python](https://www.python.org)
* [Django](https://www.djangoproject.com/)
* [Git](https://git-scm.com)
* [MongoDB](https://www.mongodb.com/pt-br)
* [Docker](https://www.docker.com/)

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/sslog2/workshop-fabrica-2024.2
    cd workshop-fabrica-2024.2
    ```
2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Inicie o servidor de desenvolvimento:
    ```bash
    docker compose build
    docker compose up
    ```
4. Para logar entre como username:admin password:admin

## Uso
- Acesse o servidor de desenvolvimento em `http://127.0.0.1:8000/`.

## Estrutura do Projeto

- `manage.py`: Utilitário de linha de comando do Django.
- `project/`: Diretório do projeto Django.
- `app/`: Diretório do aplicativo Django.
