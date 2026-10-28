from dataclasses import dataclass, field
from typing import List


@dataclass
class Acionamento:
    nome: str
    time: str
    horario: str
    atendeu: str


@dataclass
class Alerta:
    id: str
    ticket: str
    evento: str
    status: str
    acionamentos: List[Acionamento] = field(default_factory=list)