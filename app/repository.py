from typing import Dict, List, Optional, Protocol


class AlertasRepository(Protocol):
	def listar_alertas(self) -> List[Dict]:
		...

	def buscar_alerta(self, alerta_id: str) -> Optional[Dict]:
		...

	def buscar_alertas_por_ticket(self, termo_ticket: str) -> List[Dict]:
		...

	def inserir_alerta(self, alerta: Dict) -> None:
		...

	def atualizar_alerta(self, alerta_id: str, ticket: str, evento: str, descricao_timeline: str) -> None:
		...

	def remover_alerta(self, alerta_id: str) -> None:
		...

	def inserir_acionamento(
		self,
		alerta_id: str,
		nome: str,
		time: str,
		horario: str,
		atendeu: str,
		status_acionamento: str,
	) -> None:
		...

	def remover_acionamento(self, acionamento_id: int) -> None:
		...
