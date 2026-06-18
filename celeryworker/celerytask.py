"""
TODO: Adicionar descricoes desse arquivo ao concepts e readme
"""

from celery import Celery

# Criando a instancia do Celery para a aplicacao
app = Celery('task')
  
# Configura o CELERY usando settings do arquivo celeryconfig.py
app.config_from_object('celeryconfig', namespace='CELERY')

@app.task
def add_numbers(x, y):
    return x + y