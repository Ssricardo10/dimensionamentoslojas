"""Modelos de dados: Loja e Funcionário."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Loja:
    id: int
    nome: str
    un: str
    municipio: str
    endereco: str
    horario: str
    vagas_agentes: int
    vagas_triagistas: int
    total_hcs: int
    status: str
    lat: float = 0.0
    lng: float = 0.0


@dataclass
class Funcionario:
    cadastro: str
    nome: str
    endereco: str
    cidade: str
    status: str
    resposta_interesse: str = "-"
    lat: float = 0.0
    lng: float = 0.0
