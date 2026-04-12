"""Sistema de alocação inteligente de 61 Coordenadores SABESP.

Regras:
- 1 turno único por loja (expediente comercial contínuo)
- >10 PAs → 2 coordenadores
- ≤10 PAs → 1 coordenador
- Agrupamento de lojas pequenas próximas para atingir meta de 61
"""

from __future__ import annotations
from src.models import Loja
from src.distance import haversine


class CoordenadorAllocator:
    """Aloca exatamente 61 coordenadores entre postos de trabalho."""

    TOTAL_COORDENADORES = 61
    MAX_POSICOES_1_COORD = 10       # até 10 PAs = 1 coordenador
    DISTANCIA_VIAVEL_KM = 50        # distância máxima entre lojas agrupadas

    def __init__(self, lojas: list[Loja]):
        self.lojas = lojas
        self.coordenadores: list[dict] = []
        self.grupos: list[dict] = []
        self._next_id = 0

    def _proximo_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def alocar(self) -> dict:
        # Separa lojas grandes (>10 PAs) e pequenas (≤10 PAs)
        grandes = [l for l in self.lojas if l.vagas_agentes > self.MAX_POSICOES_1_COORD]
        pequenas = [l for l in self.lojas if l.vagas_agentes <= self.MAX_POSICOES_1_COORD]

        # Bruto: grandes×2 + pequenas×1
        bruto = len(grandes) * 2 + len(pequenas)
        economia_necessaria = bruto - self.TOTAL_COORDENADORES

        # --- 1. Aloca lojas grandes (2 coords cada, turno único) ---
        for loja in grandes:
            for seq in (1, 2):
                cid = self._proximo_id()
                par_id = cid + 1 if seq == 1 else cid - 1
                self.coordenadores.append({
                    "id": cid,
                    "nome": f"Coordenador {cid}",
                    "tipo": "dupla",
                    "loja_id": loja.id,
                    "loja_nome": loja.nome,
                    "municipio": loja.municipio,
                    "horario": loja.horario,
                    "turno": "Expediente",
                    "vagas_agentes": loja.vagas_agentes,
                    "dupla_com": par_id,
                    "status": "alocado",
                })

        # --- 2. Agrupa lojas pequenas para economizar coordenadores ---
        # Ordena por PAs (menos PAs primeiro = mais fácil agrupar)
        pequenas_sorted = sorted(pequenas, key=lambda l: l.vagas_agentes)

        # Calcula matriz de distâncias entre lojas pequenas
        pares_distancia = []
        for i, l1 in enumerate(pequenas_sorted):
            for j, l2 in enumerate(pequenas_sorted):
                if j <= i:
                    continue
                dist = haversine(l1.lat, l1.lng, l2.lat, l2.lng)
                if dist <= self.DISTANCIA_VIAVEL_KM:
                    pares_distancia.append((dist, l1, l2))
        pares_distancia.sort(key=lambda x: x[0])

        # Agrupa pares mais próximos até atingir economia necessária
        agrupadas = set()  # IDs de lojas já agrupadas
        grupos_formados = []

        for dist, l1, l2 in pares_distancia:
            if len(grupos_formados) >= economia_necessaria:
                break
            if l1.id in agrupadas or l2.id in agrupadas:
                continue
            agrupadas.add(l1.id)
            agrupadas.add(l2.id)
            grupos_formados.append({
                "lojas": [l1, l2],
                "distancia_km": round(dist, 1),
            })

        # Aloca coords para grupos (1 coord por grupo de 2 lojas)
        for idx, grupo in enumerate(grupos_formados):
            cid = self._proximo_id()
            lojas_grupo = grupo["lojas"]
            nomes = " + ".join(l.nome for l in lojas_grupo)
            self.coordenadores.append({
                "id": cid,
                "nome": f"Coordenador {cid}",
                "tipo": "agrupador",
                "loja_id": lojas_grupo[0].id,
                "loja_nome": nomes,
                "municipio": ", ".join(l.municipio for l in lojas_grupo),
                "horario": lojas_grupo[0].horario,
                "turno": "Expediente",
                "vagas_agentes": sum(l.vagas_agentes for l in lojas_grupo),
                "status": "alocado",
                "grupo_lojas": [
                    {"loja_id": l.id, "loja_nome": l.nome, "municipio": l.municipio,
                     "vagas_agentes": l.vagas_agentes, "horario": l.horario}
                    for l in lojas_grupo
                ],
                "distancia_km": grupo["distancia_km"],
            })
            self.grupos.append({
                "id": f"GRP_{idx+1:03d}",
                "coordenador_id": cid,
                "coordenador_nome": f"Coordenador {cid}",
                "lojas": [
                    {"loja_id": l.id, "loja_nome": l.nome, "municipio": l.municipio,
                     "vagas_agentes": l.vagas_agentes, "horario": l.horario}
                    for l in lojas_grupo
                ],
                "distancia_maxima_km": grupo["distancia_km"],
                "tempo_deslocamento_min": round(grupo["distancia_km"] * 2.5),
                "num_lojas": len(lojas_grupo),
            })

        # --- 3. Aloca lojas pequenas individuais (não agrupadas) ---
        for loja in pequenas_sorted:
            if loja.id in agrupadas:
                continue
            cid = self._proximo_id()
            self.coordenadores.append({
                "id": cid,
                "nome": f"Coordenador {cid}",
                "tipo": "individual",
                "loja_id": loja.id,
                "loja_nome": loja.nome,
                "municipio": loja.municipio,
                "horario": loja.horario,
                "turno": "Expediente",
                "vagas_agentes": loja.vagas_agentes,
                "status": "alocado",
            })

        # --- 4. Monta mapeamento loja → coordenadores ---
        mapa_loja = {}
        for c in self.coordenadores:
            if c["tipo"] == "agrupador":
                for lg in c.get("grupo_lojas", []):
                    lid = lg["loja_id"]
                    mapa_loja.setdefault(lid, []).append({
                        "coord_id": c["id"], "coord_nome": c["nome"],
                        "tipo": "agrupador", "compartilhado_com": [
                            gl["loja_nome"] for gl in c["grupo_lojas"] if gl["loja_id"] != lid
                        ]
                    })
            else:
                lid = c["loja_id"]
                mapa_loja.setdefault(lid, []).append({
                    "coord_id": c["id"], "coord_nome": c["nome"],
                    "tipo": c["tipo"],
                })

        return {
            "total_coordenadores": self._next_id,
            "meta_coordenadores": self.TOTAL_COORDENADORES,
            "status": "completo" if self._next_id == self.TOTAL_COORDENADORES else "ajuste_necessario",
            "coordenadores": self.coordenadores,
            "grupos_pequenas": self.grupos,
            "mapa_loja": mapa_loja,
            "resumo_por_tipo": {
                "lojas_grandes": len(grandes),
                "lojas_pequenas": len(pequenas),
                "grupos_formados": len(grupos_formados),
                "economia": economia_necessaria,
                "bruto_sem_agrupamento": bruto,
                "alocados": self._next_id,
            },
        }
