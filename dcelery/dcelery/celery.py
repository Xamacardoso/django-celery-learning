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

# Configura as rotas de tasks para different queues (diferentes filas)
# Isso diz pro celery que a task shared_test deve ser processada pela queue1 e shared_test2 pela queue2
app.conf.task_routes = {
    'newapp.tasks.shared_test': {'queue': 'queue1'},
    'newapp.tasks.shared_test2': {'queue': 'queue2'},
}

# Diz pro celery para buscar tasks
app.autodiscover_tasks()