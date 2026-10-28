from typing import Dict, List, Optional

from app.db import get_connection


class SQLiteAlertasRepository:
    def _obter_status_atual(self, alerta_id: str) -> str:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT status_acionamento
                FROM acionamentos
                WHERE alerta_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (alerta_id,),
            ).fetchone()

        if not row or not (row["status_acionamento"] or "").strip():
            return "Sem acionamento"
        return row["status_acionamento"]

    def listar_alertas(self) -> List[Dict]:
        with get_connection() as conn:
            alertas_rows = conn.execute(
                "SELECT id, ticket, evento, descricao_timeline FROM alertas ORDER BY created_at DESC"
            ).fetchall()

            alertas: List[Dict] = []
            for row in alertas_rows:
                alerta = {
                    "id": row["id"],
                    "ticket": row["ticket"],
                    "evento": row["evento"],
                    "status_atual": self._obter_status_atual(row["id"]),
                    "descricao_timeline": row["descricao_timeline"] or "",
                    "acionamentos": self.listar_acionamentos_por_alerta(row["id"]),
                }
                alertas.append(alerta)

            return alertas

    def buscar_alertas_por_ticket(self, termo_ticket: str) -> List[Dict]:
        termo = termo_ticket.strip()
        if not termo:
            return self.listar_alertas()

        with get_connection() as conn:
            alertas_rows = conn.execute(
                """
                SELECT id, ticket, evento, descricao_timeline
                FROM alertas
                WHERE ticket LIKE ?
                ORDER BY created_at DESC
                """,
                (f"%{termo}%",),
            ).fetchall()

        alertas: List[Dict] = []
        for row in alertas_rows:
            alertas.append(
                {
                    "id": row["id"],
                    "ticket": row["ticket"],
                    "evento": row["evento"],
                    "status_atual": self._obter_status_atual(row["id"]),
                    "descricao_timeline": row["descricao_timeline"] or "",
                    "acionamentos": self.listar_acionamentos_por_alerta(row["id"]),
                }
            )
        return alertas

    def buscar_alerta(self, alerta_id: str) -> Optional[Dict]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, ticket, evento, descricao_timeline FROM alertas WHERE id = ?",
                (alerta_id,),
            ).fetchone()

        if not row:
            return None

        return {
            "id": row["id"],
            "ticket": row["ticket"],
            "evento": row["evento"],
            "status_atual": self._obter_status_atual(row["id"]),
            "descricao_timeline": row["descricao_timeline"] or "",
            "acionamentos": self.listar_acionamentos_por_alerta(row["id"]),
        }

    def inserir_alerta(self, alerta: Dict) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO alertas (id, ticket, evento, status, descricao_timeline) VALUES (?, ?, ?, ?, ?)",
                (
                    alerta["id"],
                    alerta["ticket"],
                    alerta["evento"],
                    alerta["status"],
                    alerta.get("descricao_timeline", ""),
                ),
            )

    def atualizar_alerta(self, alerta_id: str, ticket: str, evento: str, descricao_timeline: str) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE alertas SET ticket = ?, evento = ?, descricao_timeline = ? WHERE id = ?",
                (ticket, evento, descricao_timeline, alerta_id),
            )

    def remover_alerta(self, alerta_id: str) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM alertas WHERE id = ?", (alerta_id,))

    def listar_acionamentos_por_alerta(self, alerta_id: str) -> List[Dict]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, nome, time, horario, atendeu, status_acionamento
                FROM acionamentos
                WHERE alerta_id = ?
                ORDER BY id ASC
                """,
                (alerta_id,),
            ).fetchall()

        return [
            {
                "id": row["id"],
                "nome": row["nome"],
                "time": row["time"],
                "horario": row["horario"] or "",
                "atendeu": row["atendeu"] or "-",
                "status_acionamento": row["status_acionamento"] or "",
            }
            for row in rows
        ]

    def inserir_acionamento(
        self,
        alerta_id: str,
        nome: str,
        time: str,
        horario: str,
        atendeu: str,
        status_acionamento: str,
    ) -> None:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO acionamentos (alerta_id, nome, time, horario, atendeu, status_acionamento)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (alerta_id, nome, time, horario, atendeu, status_acionamento),
            )

    def remover_acionamento(self, acionamento_id: int) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM acionamentos WHERE id = ?", (acionamento_id,))
