"""
TODO: Adicionar descricoes desse arquivo ao concepts e readme
"""

import os
from celery import Celery

# Define onde está o settings do django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')

# Criando a instancia do Celery para a aplicacao
app = Celery('dcelery')

# Configura o CELERY usando settings do django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Task para somar numeros
@app.task
def add_numbers(x, y):
    return x + y

# Diz pro celery para buscar tasks nas apps definidas em
# INSTALLED_APPS no settings.py
app.autodiscover_tasks(['newapp'])