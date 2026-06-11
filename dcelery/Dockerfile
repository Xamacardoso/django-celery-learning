FROM python:3.14.4-alpine

WORKDIR /usr/src/app

# impede o python de escrever .pyc efazer a saida de dados ser em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copia tudo que estiver no contexto atual para dentro do workdir
COPY . /usr/src/app/

# entrypoint é o comando que roda quando o container inicia
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]