"""Sistema de alocação de Supervisores SABESP.

Premissas:
1. Lojas com supervisores já definidos no Excel (coluna "Coordenador") são respeitadas.
2. Lojas sem supervisor (valor 0) recebem alocação automática:
   - 1~3 PAs: 1 supervisor pode cobrir até 3 lojas próximas (≤30 km)
   - 4~6 PAs: 1 supervisor pode cobrir até 2 lojas próximas (≤30 km)
   - 7+ PAs sem supervisor: 1 supervisor dedicado
3. Total disponível: 61 supervisores
4. Se o mínimo de agrupamentos já exceder o budget, pares/trios mais distantes
   são quebrados e recebem supervisor dedicado.
"""

from __future__ import annotations

from src.models import Loja
from src.distance import haversine


class CoordenadorAllocator:
    """Aloca supervisores respeitando os já definidos e distribuindo o restante."""

    TOTAL_SUPERVISORES = 61
    DISTANCIA_MAX_GRUPO_KM = 30
    LOJA_2_TURNOS = "chacara santo antonio"

    def __init__(self, lojas: list[Loja]):
        self.lojas = lojas
        self.supervisores: list[dict] = []
        self.grupos: list[dict] = []
        self._next_id = 0

    def _proximo_id(self) -> int:
        self._next_id += 1
        return self._next_id

    # ------------------------------------------------------------------
    def alocar(self) -> dict:
        lojas_com_qtd: list[tuple[Loja, int, int]] = []
        sem_supv: list[Loja] = []
        total_excel = 0
        ajuste_turno = 0

        for loja in self.lojas:
            qtd_excel = loja.supervisores
            extra_turno = 0

            if loja.nome.strip().lower() == self.LOJA_2_TURNOS and qtd_excel < 2:
                extra_turno = 2 - qtd_excel

            qtd_fixa = qtd_excel + extra_turno
            total_excel += qtd_excel
            ajuste_turno += extra_turno

            if qtd_fixa > 0:
                lojas_com_qtd.append((loja, qtd_fixa, qtd_excel))
            else:
                sem_supv.append(loja)

        total_fixos = total_excel + ajuste_turno
        budget = self.TOTAL_SUPERVISORES - total_fixos

        # --- 1. Supervisores já definidos (do Excel) ---
        for loja, qtd_fixa, qtd_excel in lojas_com_qtd:
            for s in range(qtd_fixa):
                origem = "excel" if s < qtd_excel else "turno"
                cid = self._proximo_id()
                self.supervisores.append({
                    "id": cid,
                    "nome": f"Supervisor {cid}",
                    "tipo": "dedicado",
                    "origem": origem,
                    "loja_id": loja.id,
                    "loja_nome": loja.nome,
                    "municipio": loja.municipio,
                    "horario": loja.horario,
                    "vagas_agentes": loja.vagas_agentes,
                    "status": "alocado",
                })

        # --- 2. Classificar lojas sem supervisor ---
        pequenas = sorted([l for l in sem_supv if l.vagas_agentes <= 3],
                          key=lambda x: x.vagas_agentes)
        medias = sorted([l for l in sem_supv if 4 <= l.vagas_agentes <= 6],
                        key=lambda x: x.vagas_agentes)
        grandes = [l for l in sem_supv if l.vagas_agentes > 6]

        # --- 3. Formar agrupamentos candidatos ---
        agrupamentos = []  # (tipo, lojas, dist_max, economia)

        # Trios para pequenas (1-3 PAs) — economia de 2 cada
        usadas: set[int] = set()
        for i, l1 in enumerate(pequenas):
            if l1.id in usadas:
                continue
            for j, l2 in enumerate(pequenas[i+1:], i+1):
                if l2.id in usadas:
                    continue
                d1 = haversine(l1.lat, l1.lng, l2.lat, l2.lng)
                if d1 > self.DISTANCIA_MAX_GRUPO_KM:
                    continue
                for l3 in pequenas[j+1:]:
                    if l3.id in usadas:
                        continue
                    d2 = haversine(l1.lat, l1.lng, l3.lat, l3.lng)
                    d3 = haversine(l2.lat, l2.lng, l3.lat, l3.lng)
                    if d2 <= self.DISTANCIA_MAX_GRUPO_KM and d3 <= self.DISTANCIA_MAX_GRUPO_KM:
                        dmax = max(d1, d2, d3)
                        agrupamentos.append(("trio", [l1, l2, l3], dmax, 2))
                        usadas.update({l1.id, l2.id, l3.id})
                        break
                if l1.id in usadas:
                    break

        # Pares para pequenas restantes — economia de 1
        peq_sobra = [l for l in pequenas if l.id not in usadas]
        for i, l1 in enumerate(peq_sobra):
            if l1.id in usadas:
                continue
            best = None
            for l2 in peq_sobra[i+1:]:
                if l2.id in usadas:
                    continue
                d = haversine(l1.lat, l1.lng, l2.lat, l2.lng)
                if d <= self.DISTANCIA_MAX_GRUPO_KM and (best is None or d < best[0]):
                    best = (d, l2)
            if best:
                agrupamentos.append(("par_peq", [l1, best[1]], best[0], 1))
                usadas.update({l1.id, best[1].id})

        # Pares para médias (4-6 PAs) — economia de 1
        usadas_med: set[int] = set()
        dists = []
        for i, l1 in enumerate(medias):
            for l2 in medias[i+1:]:
                d = haversine(l1.lat, l1.lng, l2.lat, l2.lng)
                dists.append((d, l1, l2))
        dists.sort(key=lambda x: x[0])
        for d, l1, l2 in dists:
            if d > self.DISTANCIA_MAX_GRUPO_KM:
                break
            if l1.id in usadas_med or l2.id in usadas_med:
                continue
            agrupamentos.append(("par_med", [l1, l2], d, 1))
            usadas_med.update({l1.id, l2.id})

        # Isoladas
        peq_iso = [l for l in pequenas if l.id not in usadas]
        med_iso = [l for l in medias if l.id not in usadas_med]

        # --- 4. Ajustar para caber no budget ---
        economia_total = sum(a[3] for a in agrupamentos)
        minimo = len(sem_supv) - economia_total

        # Se sobrando budget, quebrar agrupamentos mais distantes
        agrupamentos.sort(key=lambda x: -x[2])  # mais distante primeiro
        mantidos = list(agrupamentos)
        quebrados: list[list[Loja]] = []
        supv_necessarios = minimo

        while supv_necessarios < budget and mantidos:
            pior = mantidos.pop(0)
            supv_necessarios += pior[3]
            quebrados.extend(pior[1])

        # Se superou o budget, desfazer última quebra
        if supv_necessarios > budget and quebrados:
            ultimo = agrupamentos[len(agrupamentos) - len(mantidos) - 1]
            mantidos.insert(0, ultimo)
            supv_necessarios -= ultimo[3]
            for l in ultimo[1]:
                quebrados.remove(l)

        # --- 5. Gerar supervisores para lojas sem supervisor ---
        # 5a. Dedicados (grandes + isoladas + quebradas)
        dedicadas = list(grandes) + list(peq_iso) + list(med_iso) + quebrados
        for loja in dedicadas:
            cid = self._proximo_id()
            self.supervisores.append({
                "id": cid,
                "nome": f"Supervisor {cid}",
                "tipo": "dedicado",
                "origem": "calculado",
                "loja_id": loja.id,
                "loja_nome": loja.nome,
                "municipio": loja.municipio,
                "horario": loja.horario,
                "vagas_agentes": loja.vagas_agentes,
                "status": "alocado",
            })

        # 5b. Itinerantes (agrupamentos mantidos)
        for idx, (tipo, lojas_g, dist, _eco) in enumerate(mantidos):
            cid = self._proximo_id()
            nomes = " + ".join(l.nome for l in lojas_g)
            self.supervisores.append({
                "id": cid,
                "nome": f"Supervisor {cid}",
                "tipo": "itinerante",
                "origem": "calculado",
                "loja_id": lojas_g[0].id,
                "loja_nome": nomes,
                "municipio": ", ".join(l.municipio for l in lojas_g),
                "horario": " / ".join(l.horario for l in lojas_g),
                "vagas_agentes": sum(l.vagas_agentes for l in lojas_g),
                "status": "alocado",
                "grupo_lojas": [
                    {"loja_id": l.id, "loja_nome": l.nome, "municipio": l.municipio,
                     "vagas_agentes": l.vagas_agentes, "horario": l.horario}
                    for l in lojas_g
                ],
                "distancia_km": round(dist, 1),
            })
            self.grupos.append({
                "id": f"GRP_{idx+1:03d}",
                "supervisor_id": cid,
                "supervisor_nome": f"Supervisor {cid}",
                "lojas": [
                    {"loja_id": l.id, "loja_nome": l.nome, "municipio": l.municipio,
                     "vagas_agentes": l.vagas_agentes, "horario": l.horario}
                    for l in lojas_g
                ],
                "distancia_maxima_km": round(dist, 1),
                "num_lojas": len(lojas_g),
            })

        # --- 6. Mapa loja → supervisores ---
        mapa_loja: dict[int, list[dict]] = {}
        for s in self.supervisores:
            if s["tipo"] == "itinerante":
                for lg in s.get("grupo_lojas", []):
                    lid = lg["loja_id"]
                    mapa_loja.setdefault(lid, []).append({
                        "supv_id": s["id"], "supv_nome": s["nome"],
                        "tipo": "itinerante",
                        "compartilhado_com": [
                            gl["loja_nome"] for gl in s["grupo_lojas"]
                            if gl["loja_id"] != lid
                        ],
                    })
            else:
                lid = s["loja_id"]
                mapa_loja.setdefault(lid, []).append({
                    "supv_id": s["id"], "supv_nome": s["nome"],
                    "tipo": s["tipo"], "origem": s["origem"],
                })

        return {
            "total_coordenadores": self._next_id,
            "meta_coordenadores": self.TOTAL_SUPERVISORES,
            "status": "completo" if self._next_id == self.TOTAL_SUPERVISORES else "ajuste_necessario",
            "coordenadores": self.supervisores,
            "grupos_pequenas": self.grupos,
            "mapa_loja": mapa_loja,
            "resumo_por_tipo": {
                "ja_alocados_excel": total_excel,
                "ajustes_turno": ajuste_turno,
                "lojas_com_supervisor_excel": sum(1 for _, _, q_excel in lojas_com_qtd if q_excel > 0),
                "lojas_sem_supervisor": len(sem_supv),
                "pequenas_1_3": len(pequenas),
                "medias_4_6": len(medias),
                "grandes_7_mais": len(grandes),
                "grupos_formados": len(mantidos),
                "lojas_agrupadas": sum(len(a[1]) for a in mantidos),
                "supervisores_calculados": self._next_id - total_excel,
                "alocados": self._next_id,
            },
        }
