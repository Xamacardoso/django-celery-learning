# Conceitos da Arquitetura (Django + Celery + Redis)

Este documento descreve os conceitos fundamentais do sistema de mensageria assíncrona estruturado no projeto até o momento.

---

## 🧩 Os Três Pilares do Sistema

Atualmente, o projeto está preparado para utilizar a seguinte estrutura de mensageria:

1. **Produtor (Django)**
   * A aplicação web principal.
   * É quem cria e solicita a execução de uma tarefa (ex: enviar um e-mail, gerar um relatório).
   * Em vez de executar a tarefa pesada imediatamente (travando a requisição do usuário), ele envia uma mensagem (pedido de tarefa).

2. **Broker / Intermediário (Redis)**
   * É o intermediário que recebe as mensagens do produtor e as guarda em uma fila temporária.
   * Responsavel pela infraestrutura e entrega confiável de tasks
   * Atua como uma caixa de correio.
   * Configurado via Docker Compose como o serviço `redis`.

3. **Consumidor / Worker (Celery)**
   * É um processo separado (incluído em [requirements.txt](dcelery/requirements.txt)) que fica escutando o Broker.
   * Quando há uma nova tarefa na fila do Redis, o Celery a retira, executa a tarefa em segundo plano e, opcionalmente, devolve o resultado.

4. **Result Backend (Redis)**
   * É o local onde o Celery armazena o resultado da execução da tarefa.
   * Pode ser o mesmo Broker ou um banco de dados separado.
   * No nosso caso, será o mesmo Redis.

---

## ⏳ Fluxo de Execução (Vertical)

Quando um usuário faz uma ação que exige processamento pesado:

```text
[ Usuário ]
    │
    ▼ (Acessa uma rota)
[ Django (Produtor) ]
    │
    ├─► (1) Cria a tarefa assíncrona
    │
    ▼ (2) Envia mensagem para o Broker
[ Redis (Message Broker) ]
    │
    ├─► (3) Armazena a mensagem na fila
    │
    ▼ (4) Envia a tarefa disponível
[ Celery (Worker/Consumidor) ]
    │
    └─► (5) Processa a tarefa em segundo plano
```

---

## 🐳 Integração no Docker Compose

Atualmente, os serviços estão declarados no [docker-compose.yml](docker-compose.yml):

```text
┌──────────────────────────────────────────┐
│             DOCKER COMPOSE               │
│                                          │
│  ┌────────────────┐  Porta 6379  ┌──────┐│
│  │     django     │◄────────────►│ redis││
│  └────────────────┘              └──────┘│
│           │                              │
│           ▼ Porta 8001 (Host)            │
│    [ Navegador / Host ]                  │
└──────────────────────────────────────────┘
```

* **Comunicação interna:** O container Django se conecta ao container `redis` internamente pela porta padrão `6379`.
* **Ambiente isolado:** O banco SQLite `db.sqlite3` é mantido localmente na pasta compartilhada, permitindo persistência de dados do Django mesmo que o container seja reiniciado.
