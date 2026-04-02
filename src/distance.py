"""Cálculo de distância geográfica (Haversine)."""

from math import radians, cos, sin, asin, sqrt

from src.config import FATOR_TEMPO_MIN_POR_KM, CUSTO_KM, DIAS_UTEIS_MES


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância em km entre duas coordenadas."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return round(6371 * 2 * asin(sqrt(a)), 2)


def tempo_deslocamento(distancia_km: float) -> float:
    """Tempo estimado em minutos (trânsito SP)."""
    return round(distancia_km * FATOR_TEMPO_MIN_POR_KM, 1)


def custo_mensal(distancia_km: float) -> float:
    """Custo mensal estimado (ida e volta, 22 dias úteis)."""
    return round(distancia_km * CUSTO_KM * 2 * DIAS_UTEIS_MES, 2)
