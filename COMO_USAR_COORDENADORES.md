# 🎯 GUIA RÁPIDO: Alocação de 61 Coordenadores

## 📌 Resumo Executivo

Um **sistema inteligente** foi criado para distribuir 61 Coordenadores entre os Postos de Atendimento (PAs) da SABESP seguindo regras estratégicas:

| Tipo de Loja | Critério | Alocação |
|---|---|---|
| **Grande** | >10 PAs | 2 coordenadores/turno |
| **Média** | 5-10 PAs | 1 coordenador/turno |
| **Pequena** | ≤2 PAs | 1 coord para até 3 lojas |

---

## 🚀 4 Passos para Usar

### 1️⃣ Preparar Dados
```excel
data/Endereço Lojas.xlsx
├─ Coluna "QTDE PAs" = quantidade de Analistas (SEM triagista)
├─ Coluna "Horário" = turno(s) de funcionamento
└─ Coluna "Status" = Ativo/Inativo
```

### 2️⃣ Executar Alocação
```bash
cd "c:\Users\ssricardo\OneDrive - AlmavivA do Brasil\Trade Marketing - V3\Sabesp\Agente"
.\.venv\Scripts\Activate.ps1
python scripts/run.py
```

### 3️⃣ Visualizar Dashboard
```
Abra em navegador: web/coordenadores.html
```

### 4️⃣ Gerenciar/Exportar
- **Filtrar**: Por tipo (individual/dupla/agrupador)
- **Buscar**: Por loja ou município
- **Exportar**: Excel com todos os coordenadores alocados

---

## 📊 O Sistema Gera

### ✅ **61 Coordenadores Numerados** (001 a 061)

Cada um com:
- ID único
- Tipo (individual, dupla, agrupador)
- Loja atribuída
- Turno specific
- Número de PAs cobertos

### ✅ **Grupos Inteligentes de Lojas Pequenas**

Agrupa até 3 lojas com validate:
- ✓ Distância máxima: 15 km
- ✓ Tempo máximo de deslocamento: ~40 min
- ✓ Melhor resposta em emergências

### ✅ **Dashboard Completo** (coordenadores.html)

4 seções principais:     
1. **Cards**: Stats gerais (total, lojas grandes, grupos, status)
2. **Tabela**: 61 coordenadores com filtros e busca
3. **Grupos**: Visualização de agrupamentos de lojas pequenas
4. **Zonas**: Distribuição por Unidade de Negócio

---

## 🎮 Funcionalidades da Interface

```html
web/coordenadores.html
├─ 📊 Estatísticas em tempo real
├─ 🔍 Busca e filtros avançados
├─ 📋 Tabela com paginação (10 itens/página)
├─ 📥 Exportar para Excel
├─ 📍 Visualização de grupos/distâncias
└─ ℹ️ Modal com detalhes de cada coordenador
```

---

## 💻 Arquivos Criados/Modificados

### ✨ NOVOS
| Arquivo | Descrição |
|---------|-----------|
| `src/coordinators.py` | Lógica de alocação inteligente |
| `web/coordenadores.html` | Dashboard de gestão |
| `test_coordinators.py` | Script de validação |
| `COORDENADORES.md` | Documentação técnica completa |

### 🔄 MODIFICADOS
| Arquivo | O que mudou |
|---------|-----------|
| `src/allocation.py` | Integração de coordenadores ao JSON |

---

## 📈 Dados Gerados (JSON)

O arquivo `web/dados_alocacao.json` agora contém:

```json
{
  "lojas": [...],
  "funcionarios": [...],
  "coordenadores": {
    "total": 61,
    "meta": 61,
    "status": "completo",
    "alocados": [
      {"id": 1, "tipo": "individual", "loja_id": 5, "turno": "Manhã", ...},
      {"id": 2, "tipo": "dupla", "loja_id": 10, "turno": "Noite", ...},
      ...
    ],
    "grupos_pequenas": [
      {"coordenador_id": 45, "lojas": [...], "distancia_maxima_km": 8.5, ...},
      ...
    ],
    "resumo": {
      "lojas_grandes": 25,
      "lojas_pequenas": 18,
      "alocados": 61
    }
  }
}
```

---

## 🔍 Interpretar o Dashboard

### Status Possíveis
- ✅ **Completo**: 61 coordenadores alocados → Pronto!
- ⚠️ **Ajuste Necessário**: <61 coords → Revisar base de dados

### Filtros Úteis
| Filtro | Uso |
|--------|-----|
| **Todos** | Visão geral dos 61 |
| **Individuais** | Lojas médias (1/turno) |
| **Duplas** | Lojas grandes (2/turno) |
| **Agrupadores** | Coordenadores de lojas pequenas |

### Exportar Excel
- Clique: "📥 Exportar XLS"
- Arquivo: `Alocacao_Coordenadores_YYYY-MM-DD.xlsx`
- Contém: Apenas itens filtrados ou todos

---

## ⚙️ Ajustes Práticos

### Se faltarem coordenadores:
```bash
# Editar src/coordinators.py
LIMITE_LOJAS_PEQUENAS = 4      # era 3 → mais agrupamentos
DISTANCIA_VIAVEL_KM = 20        # era 15 → agrupar mais distante
```

### Se tiver muitos agrupamentos:
```bash
# Reduzir agrupamentos
LIMITE_LOJAS_PEQUENAS = 2      # era 3
LIMITE_ANALISTAS_PEQUENA = 1   # era 2 → apenas lojas muito pequenas
```

---

## 📱 Métricas Esperadas

```
Distribuição Típica (para ~45 lojas):
├─ Lojas Grandes (>10 PAs): ~25 → ~50 coordenadores (duplas)
├─ Lojas Médias (5-10 PAs): ~15 → ~8 coordenadores
└─ Lojas Pequenas (≤2 PAs): ~5  → ~3 coordenadores (agrupados)
  TOTAL: ~61 coordenadores ✓
```

---

## 🧪 Validação Rápida

Execute o teste:
```bash
python test_coordinators.py
```

Resultado esperado:
```
✅ TESTE CONCLUÍDO COM SUCESSO
```

---

## 📞 Troubleshooting

| Problema | Solução |
|----------|---------|
| dados_alocacao.json não existe | Execute: `python scripts/run.py` |
| Menos de 61 coords | Verificar QTDE PAs no Excel (sem triagista) |
| Interface não carrega | F5 ou Ctrl+Shift+Delete (limpar cache) |
| Grupos distantes demais | Reduzir `DISTANCIA_VIAVEL_KM` |

---

## 🎯 Próximos Passos

1. ✅ Executar `python scripts/run.py` com dados reais
2. ✅ Abrir `web/coordenadores.html` e validar visualmente
3. ✅ Exportar para Excel se necessário compartilhar
4. ✅ Fazer ajustes se houver mudanças nas premissas
5. ⏳ Integrar ao menu principal do sistema (futuro)

---

## 📚 Documentação Completa

Para detalhes técnicos, ver: **[COORDENADORES.md](./COORDENADORES.md)**

---

**✓ Sistema pronto para uso!**  
**Versão:** 1.0 — Abril 2026
