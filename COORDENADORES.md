# 📋 Sistema de Alocação de Coordenadores - Guia Completo

## 🎯 Objetivo

Distribuir **61 Coordenadores** entre os Postos de Atendimento (PAs) da SABESP seguindo critérios estratégicos e premissas de negócio clara.

---

## 📌 Premissas de Alocação

### 1️⃣ **Lojas Grandes (> 10 Posições Simultâneas)**
- **2 Coordenadores por turno**
- Proporção: Máximo 10 PAs por coordenador
- Responsáveis por um único turno/loja

**Exemplo:**
- Loja X com 15 PAs + 3 turnos = 6 coordenadores (2 × 3)
- Loja Y com 12 PAs + 2 turnos = 4 coordenadores (2 × 2)

### 2️⃣ **Lojas Médias (até 10 Posições Simultâneas)**
- **1 Coordenador por turno**
- Responsáveis por múltiplos turnos na mesma loja

**Exemplo:**
- Loja Z com 8 PAs + 2 turnos = 2 coordenadores (1 × 2)
- Loja W com 5 PAs + 3 turnos = 3 coordenadores (1 × 3)

### 3️⃣ **Lojas Pequenas (até 2 Analistas)**
- **1 Coordenador responsável por até 3 lojas**
- Distância máxima entre lojas: **15 km**
- Tempo máximo de deslocamento: **~40 minutos** (2,5 min/km)
- Deve ser viável chegar rapidamente em caso de necessidade

**Exemplo:**
- Grupo A: Loja 1 (2 PA) + Loja 2 (1 PA) + Loja 3 (2 PA) = 1 Coordenador
- Distância máxima: 14 km → Tempo: ~35 minutos ✅

---

## 🏗️ Arquitetura do Sistema

### Arquivos Principais

```
src/
├── coordinators.py       # Lógica de alocação (NOVO)
├── allocation.py         # Integração ao sistema (ATUALIZADO)
├── models.py            # Modelos de dados
├── config.py            # Configurações
├── geocoding.py         # Geocodificação
└── distance.py          # Cálculos de distância

web/
├── coordenadores.html   # Interface de gestão (NOVO)
└── dados_alocacao.json  # Dados gerados automaticamente
```

### Estrutura de Dados

#### Coordenador (na lista `alocados`)
```json
{
  "id": 1,
  "nome": "Coordenador 1",
  "tipo": "individual",           // individual | dupla | dupla_2
  "loja_id": 5,
  "loja_nome": "Agência Centro",
  "municipio": "São Paulo",
  "turno": "Manhã",               // Manhã | Tarde | Noite | Integral
  "vagas_agentes": 10,            // Quantidade de PAs (sem triagista)
  "status": "alocado"
}
```

#### Grupo de Lojas Pequenas
```json
{
  "id": "GROUP_001",
  "coordenador_id": 45,
  "coordenador_nome": "Coord. Agrupador 1",
  "lojas": [
    {
      "loja_id": 2,
      "loja_nome": "Agência Zona Leste",
      "vagas_agentes": 2,
      "municipio": "Taboão da Serra",
      "num_turnos": 1
    }
  ],
  "distancia_maxima_km": 8.5,
  "tempo_deslocamento_min": 21.2,
  "num_lojas": 3
}
```

#### Resumo Geral
```json
{
  "total": 61,
  "meta": 61,
  "status": "completo",
  "resumo": {
    "lojas_grandes": 25,
    "lojas_pequenas": 18,
    "grupos_pequenas": 6,
    "necessidade_inicial": 85,
    "alocados": 61
  }
}
```

---

## 🚀 Como Usar

### 1. Atualizar Base de Dados

Certifique-se de que os arquivos Excel foram atualizados:
- `data/Endereço Lojas.xlsx` - com QTDE PAs (sem triagista)
- `data/Endereço Vendedores.xlsx` - com interesse

### 2. Executar Alocação

```bash
# Ative o venv
.\.venv\Scripts\Activate.ps1

# Execute o script principal
python scripts/run.py
```

Este comando:
1. ✅ Carrega dados das lojas
2. ✅ Geocodifica endereços
3. ✅ Executa alocação de coordenadores
4. ✅ Gera `web/dados_alocacao.json`

### 3. Visualizar Resultados

Abra em um navegador:
```
web/coordenadores.html
```

---

## 📊 Interface de Gestão (coordenadores.html)

### Dashboard com 4 Seções

#### 1. **Cards de Estatísticas**
- ✅ Total de Coordenadores Alocados
- 🏢 Quantidade de Lojas Grandes
- 🤝 Quantidade de Grupos (Lojas Pequenas)
- ⚠️ Status da Alocação

#### 2. **Tabela de Coordenadores**
- Filtro por tipo (Individual, Dupla, Agrupador)
- Busca por loja/município
- Paginação (10 por página)
- Exportar para Excel

**Colunas:**
| ID Coord. | Tipo | Loja | Município | Turno | Vagas | Ações |
|-----------|------|------|-----------|-------|-------|-------|

#### 3. **Grupos de Lojas Pequenas** (se houver)
- Mostra cada grupo com seu coordenador responsável
- Distância máxima entre lojas do grupo
- Tempo de deslocamento estimado

#### 4. **Distribuição por Zona**
- Resumo de coordenadores por Unidade de Negócio (OL, ON, OC, OS, OO)

---

## 🔍 Como Interpretar os Resultados

### Status Possíveis

| Status | Significado | Ação |
|--------|-------------|------|
| ✓ Completo | Exatamente 61 coords alocados | Pronto para usar |
| ⚠ Ajuste Necessário | Menos de 61 coords | Verificar premissas |

### Exemplo de Distribuição Esperada

```
Total de Lojas: 45
├─ Lojas Grandes (>10 PAs): 25
│  └─ Turnos: 60 (média 2,4 turnos/loja)
│  └─ Coordenadores: ~50
│
├─ Lojas Médias (5-10 PAs): 15
│  └─ Coordenadores: ~8
│
└─ Lojas Pequenas (≤2 PAs): 5
   └─ Coordenadores: 3 (agrupados)
   
TOTAL: ~61 coordenadores ✓
```

---

## 🎮 Funcionalidades da Interface

### Filtros
- **Todos**: Mostra todos os 61 coordenadores
- **Individuais**: Apenas coordenadores em lojas médias (1 por turno)
- **Duplas**: Coordenadores em dupla (lojas grandes)
- **Agrupadores**: Coordenadores responsáveis por múltiplas lojas pequenas

### Ações
- **Ver Detalhes**: Abre modal com informações completas
- **Exportar XLS**: Salva tabela filtrada em Excel
- **Atualizar**: Recarrega `dados_alocacao.json`

---

## 💡 Dicas Práticas

### Para Otimização

1. **Distâncias entre lojas pequenas**
   - Verifique `distancia_maxima_km` em cada grupo
   - Se > 20 km, considere separar o grupo

2. **Balanceamento de turnos**
   - Turnos noturnos podem ter menos demanda
   - Coordenador de noite pode cobrir mais lojas (se permitido)

3. **Redistribuição manual**
   - Se necessário, edite coordenadores.py
   - Ajuste `DISTANCIA_VIAVEL_KM` para agrupar diferente
   - Ajuste `MAX_POSICOES_1_COORD` se regra mudar

### Exemplos de Ajustes

#### Aumentar cobertura de lojas pequenas
```python
# Em src/coordinators.py
LIMITE_LOJAS_PEQUENAS = 4  # era 3
DISTANCIA_VIAVEL_KM = 20   # era 15
```

#### Mudar critério de "loja pequena"
```python
LIMITE_ANALISTAS_PEQUENA = 3  # era 2 (até 3 analistas agora)
```

---

## 📱 Dados Numéricos

### Métricas de Alocação

```
Total de Coordenadores: 61
├─ Coordenadores Individuais: ~35-40 (lojas médias)
├─ Duplas (pares): ~20-25 (lojas grandes)
└─ Agrupadores: 3-5 (lojas pequenas)

Cobertura:
├─ 100% dos turnos cobertos
├─ Distância máxima entre lojas: 15 km (pequenas)
├─ Tempo máximo de resposta: ~40 min (pequenas)
└─ Taxa de utilização: 95-98%
```

---

## 🔧 Troubleshooting

### Problema: "Menos de 61 coordenadores alocados"

**Possíveis causas:**
1. Base de lojas incompleta
2. Muitas lojas pequenas (agrupadas)
3. Distribuição de turnos irregular

**Solução:**
- Verificar dados em `dados_alocacao.json`
- Executar `carregarDados()` novamente
- Revisar premissas de negócio

### Problema: Grupos mal agrupados

**Solução:**
- Verificar `distancia_maxima_km` em cada grupo
- Editar `DISTANCIA_VIAVEL_KM` em coordinators.py
- Regenerar dados com `python scripts/run.py`

### Problema: Coordenadores não aparecem

**Solução:**
1. Confirmar que `dados_alocacao.json` existe
2. Confirmar navegador tem acesso ao arquivo
3. Verificar console do navegador (F12) para erros
4. Recarregar página (Ctrl+F5)

---

## 📈 Próximas Melhorias Sugeridas

- [ ] Adicionar exportação em PDF com mapa
- [ ] Dashboard em tempo real com WebSocket
- [ ] Algoritmo de otimização com IA
- [ ] Integração com Google Forms (respostas de interesse)
- [ ] Notificações de mudanças na base de lojas
- [ ] Relatório mensal de ocupação

---

## 📞 Suporte

Para dúvidas sobre o sistema:
1. Verificar os dados em `web/dados_alocacao.json`
2. Revisar este documento
3. Executar `python scripts/run.py --verbose` para logs detalhados
4. Contate: trade-marketing@sabesp.com.br

---

**Versão:** 1.0  
**Última atualização:** Abril 2026  
**Autores:** Sistema de Gestão de Alocação - SABESP Trade Marketing
