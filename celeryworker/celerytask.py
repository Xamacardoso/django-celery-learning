"""
TODO: Adicionar descricoes desse arquivo ao concepts e readme
"""

from celery import Celery

# Criando a instancia do Celery para a aplicacao
app = Celery('task')
  
# Configura o CELERY usando settings do arquivo celeryconfig.py
app.config_from_object('celeryconfig', namespace='CELERY')

# importa as tasks definidas em newapp.tasks
app.conf.imports = ('newapp.tasks')

# Diz pro celery para buscar tasks
app.autodiscover_tasks()