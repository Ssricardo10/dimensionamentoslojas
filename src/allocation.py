"""Carrega dados dos Excel e geocodifica."""

from __future__ import annotations

import pandas as pd

from src.config import LOJAS_XLSX, FUNCIONARIOS_XLSX, CORES_ZONAS
from src.models import Loja, Funcionario
from src.geocoding import Geocoder
from src.distance import haversine, tempo_deslocamento, custo_mensal
from src.coordinators import CoordenadorAllocator


def load_lojas(geocoder: Geocoder) -> list[Loja]:
    """Carrega lojas do Excel e geocodifica endereços."""
    df = pd.read_excel(LOJAS_XLSX)
    lojas: list[Loja] = []

    for idx, row in df.iterrows():
        municipio = str(row["Município"])
        endereco = str(row["Endereço Completo"])

        print(f"  [{idx+1}/{len(df)}] {row['Agência']}")
        lat, lng = geocoder.geocode(endereco, municipio)

        lojas.append(Loja(
            id=idx + 1,
            nome=str(row["Agência"]),
            un=str(row["UN"]),
            municipio=municipio,
            endereco=endereco,
            horario=str(row["Horário"]),
            vagas_agentes=int(row["QTDE PAs"]) if pd.notna(row["QTDE PAs"]) else 0,
            vagas_triagistas=int(row["Triagistas"]) if pd.notna(row["Triagistas"]) else 0,
            total_hcs=int(row["Total HCs"]) if pd.notna(row["Total HCs"]) else 0,
            status=str(row["Status"]) if pd.notna(row["Status"]) else "-",
            lat=lat,
            lng=lng,
            supervisores=int(row["Coordenador"]) if "Coordenador" in df.columns and pd.notna(row.get("Coordenador")) else 0,
        ))

    return lojas


def load_funcionarios(geocoder: Geocoder) -> list[Funcionario]:
    """Carrega funcionários do Excel e geocodifica endereços."""
    df = pd.read_excel(FUNCIONARIOS_XLSX)
    funcionarios: list[Funcionario] = []

    for idx, row in df.iterrows():
        cidade = str(row["CIDADE"])
        endereco = str(row["Endereço Completo"])

        print(f"  [{idx+1}/{len(df)}] {row['NOME']}")
        lat, lng = geocoder.geocode(endereco, cidade)

        funcionarios.append(Funcionario(
            cadastro=str(row["CADASTRO"]),
            nome=str(row["NOME"]),
            endereco=endereco,
            cidade=cidade,
            status=str(row["DESCRIÇÃO"]) if pd.notna(row["DESCRIÇÃO"]) else "Ativo",
            resposta_interesse=str(row["Resposta Formes"]) if pd.notna(row["Resposta Formes"]) else "-",
            lat=lat,
            lng=lng,
        ))

    return funcionarios


def build_json(lojas: list[Loja], funcionarios: list[Funcionario]) -> dict:
    """Monta o JSON final consumido pelo frontend."""
    
    # 1. Dados das lojas
    lojas_data = []
    for loja in lojas:
        zona_info = CORES_ZONAS.get(loja.un, {})
        lojas_data.append({
            "id": loja.id,
            "nome": loja.nome,
            "un": loja.un,
            "zona": zona_info.get("nome", "?"),
            "municipio": loja.municipio,
            "endereco": loja.endereco,
            "horario": loja.horario,
            "vagas_agentes": loja.vagas_agentes,
            "vagas_triagistas": loja.vagas_triagistas,
            "total_hcs": loja.total_hcs,
            "status": loja.status,
            "lat": loja.lat,
            "lng": loja.lng,
            "cor_hex": zona_info.get("cor", "#95a5a6"),
        })

    # 2. Dados dos funcionários
    funcs_data = []
    for func in funcionarios:
        # Calcula distância para cada loja
        proximas = []
        for loja in lojas:
            dist = haversine(func.lat, func.lng, loja.lat, loja.lng)
            proximas.append({
                "loja_id": loja.id,
                "loja_nome": loja.nome,
                "distancia_km": dist,
                "tempo_min": tempo_deslocamento(dist),
                "custo_mensal": custo_mensal(dist),
            })
        proximas.sort(key=lambda x: x["distancia_km"])

        funcs_data.append({
            "cadastro": func.cadastro,
            "nome": func.nome,
            "endereco": func.endereco,
            "cidade": func.cidade,
            "status": func.status,
            "resposta_interesse": func.resposta_interesse,
            "lat": func.lat,
            "lng": func.lng,
            "lojas_proximas": proximas,
        })

    # 3. Alocação de coordenadores
    try:
        allocator = CoordenadorAllocator(lojas)
        alocacao_coords = allocator.alocar()
        
        coordenadores_data = {
            "total": alocacao_coords["total_coordenadores"],
            "meta": alocacao_coords["meta_coordenadores"],
            "status": alocacao_coords["status"],
            "alocados": alocacao_coords["coordenadores"],
            "grupos_pequenas": alocacao_coords["grupos_pequenas"],
            "mapa_loja": alocacao_coords["mapa_loja"],
            "resumo": alocacao_coords["resumo_por_tipo"],
        }
    except Exception as e:
        print(f"\n⚠️ Erro ao alocar coordenadores: {e}")
        print("Continuando sem dados de coordenadores...")
        coordenadores_data = None

    result = {
        "lojas": lojas_data,
        "funcionarios": funcs_data,
        "cores_zonas": CORES_ZONAS,
    }
    
    if coordenadores_data:
        result["coordenadores"] = coordenadores_data
    
    return result
