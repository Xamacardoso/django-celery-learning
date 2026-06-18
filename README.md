# Django & Celery Course

Este projeto é um ambiente de aprendizado e desenvolvimento configurado para integrar o **Django** com o **Celery** utilizando **Redis** como Message Broker. O ambiente é totalmente conteinerizado com **Docker** e **Docker Compose**, facilitando a execução e o desenvolvimento local.

## 📚 Teoria
Os conceitos da estrutura da aplicação e do curso estão no arquivo [CONCEPTS.md](@CONCEPTS.md)

## 🛠️ Tecnologias Utilizadas

* **Python 3.14.4** (através da imagem Alpine)
* **Django 6.0.6**
* **Celery 5.6.3**
* **Redis 6** (como message broker/backend de resultados)
* **SQLite** (banco de dados padrão)
* **Docker & Docker Compose**

---

## 📂 Estrutura do Projeto

Abaixo está o detalhamento da estrutura de diretórios e arquivos do projeto:

```text
django-celery-course/
├── .gitignore              # Definição de arquivos/diretórios ignorados pelo Git
├── .python-version         # Especificação da versão do Python utilizada localmente
├── README.md               # Documentação principal do projeto (este arquivo)
├── docker-compose.yml      # Configuração dos serviços Docker (Django e Redis)
└── dcelery/                # Diretório raiz do projeto Django e Dockerfile
    ├── Dockerfile          # Instruções de build para a imagem Docker do Django
    ├── requirements.txt    # Dependências de pacotes Python
    ├── entrypoint.sh       # Script de inicialização executado antes de subir o Django
    ├── db.sqlite3          # Banco de dados SQLite3
    ├── manage.py           # Script administrativo do Django
    └── dcelery/            # Diretório de configurações do Django
        ├── __init__.py     # Arquivo de inicialização do pacote Python
        ├── settings.py     # Configurações do Django (lê variáveis do ambiente)
        ├── urls.py         # Rotas/URLs principais do projeto
        ├── asgi.py         # Configuração de servidor assíncrono (ASGI)
        └── wsgi.py         # Configuração de servidor síncrono clássico (WSGI)
```

---

## 📝 Detalhamento dos Arquivos Principais

### 🐳 Arquivos Docker

* **[docker-compose.yml]** - Define dois serviços essenciais para a aplicação:
  1. **`django`**:
     * Constrói a imagem a partir do diretório `./dcelery` usando o `Dockerfile`.
     * Executa `python manage.py runserver 0.0.0.0:8000`.
     * Monta um volume sincronizando `./dcelery` com `/usr/src/app/` dentro do container (funcionando como hot-reload de código).
     * Mapeia a porta **8001** da máquina host para a porta **8000** do container.
     * Configura variáveis de ambiente como `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS` e `DATABASE_URL`.
  2. **`redis`**:
     * Sobe uma instância do Redis na versão 6 exposta na porta padrão `6379`. É o intermediário (Broker) responsável por receber as tarefas assíncronas do Django e enfileirá-las para o Celery.

* **[dcelery/Dockerfile](dcelery/Dockerfile)** - Define a imagem Docker para o container Django:
  * Utiliza a imagem leve `python:3.14.4-alpine`.
  * Configura variáveis de ambiente do Python (`PYTHONDONTWRITEBYTECODE=1` para evitar arquivos `.pyc` e `PYTHONUNBUFFERED=1` para exibir logs em tempo real).
  * Atualiza o `pip`, instala os pacotes descritos em `requirements.txt`.
  * Copia o script `entrypoint.sh` e define ele como o `ENTRYPOINT` principal.

* **[dcelery/entrypoint.sh](dcelery/entrypoint.sh)** - Um script executado assim que o container `django` inicia:
  1. Aplica as migrações automáticas de banco de dados (`python manage.py migrate`).
  2. Executa o comando final do serviço (`exec "$@"`) garantindo que o processo web do Django rode com o PID 1 (permitindo o encerramento correto do container).

---

### ⚙️ Arquivos Django

* **[dcelery/requirements.txt](@dcelery/requirements.txt)** - Contém as bibliotecas necessárias para rodar o projeto, destacando-se o `Django`, `celery`, `redis` e as ferramentas CLI necessárias para o Celery.

* **[dcelery/dcelery/settings.py](dcelery/dcelery/settings.py)** - Arquivo central de configurações do Django adaptado para containers, onde:
  * `SECRET_KEY` é carregada via variável de ambiente, com fallback de desenvolvimento.
  * `DEBUG` e `ALLOWED_HOSTS` são parametrizados para rodar de maneira flexível.

---

## 🚀 Como Executar o Projeto

Para rodar todo o ambiente localmente, certifique-se de ter o Docker e Docker Compose instalados e execute:

```bash
# Para iniciar os containers (Django e Redis) em segundo plano
docker compose up -d

# Para acompanhar os logs de execução
docker compose logs -f
```

A aplicação Django estará acessível em: [http://localhost:8001/](http://localhost:8001/)
