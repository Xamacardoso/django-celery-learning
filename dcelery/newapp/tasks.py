"""
TODO: Adicionar descricoes desse arquivo ao concepts e readme
"""

from celery import shared_task

@shared_task
def shared_test():
    return 'shared task executed'