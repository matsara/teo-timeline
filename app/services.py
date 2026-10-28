import uuid

from app.repository import AlertasRepository


def criar_alerta(repo: AlertasRepository, ticket, evento, descricao_timeline):
	ticket = ticket.strip()
	evento = evento.strip()
	descricao_timeline = descricao_timeline.strip()

	if not ticket or not evento:
		raise ValueError("Ticket e Evento são obrigatórios.")

	alerta = {
		"id": str(uuid.uuid4()),
		"ticket": ticket,
		"evento": evento,
		"status": "",
		"descricao_timeline": descricao_timeline,
		"acionamentos": [],
	}
	repo.inserir_alerta(alerta)
	return alerta


def adicionar_acionamento(repo: AlertasRepository, alerta_id, nome, time, horario, atendeu, status_acionamento):
	nome = nome.strip()
	time = time.strip()
	horario = horario.strip()
	status_acionamento = status_acionamento.strip()

	if not nome or not time:
		raise ValueError("Nome e Time são obrigatórios.")
	if not status_acionamento:
		raise ValueError("Status do acionamento é obrigatório.")

	repo.inserir_acionamento(alerta_id, nome, time, horario, atendeu, status_acionamento)


def atualizar_alerta(repo: AlertasRepository, alerta_id, ticket, evento, descricao_timeline):
	ticket = ticket.strip()
	evento = evento.strip()
	descricao_timeline = descricao_timeline.strip()

	if not ticket or not evento:
		raise ValueError("Ticket e Evento são obrigatórios.")

	repo.atualizar_alerta(alerta_id, ticket, evento, descricao_timeline)


def remover_alerta(repo: AlertasRepository, alerta_id):
	repo.remover_alerta(alerta_id)


def remover_acionamento(repo: AlertasRepository, acionamento_id):
	repo.remover_acionamento(acionamento_id)
