"""Configurações globais do projeto."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Caminhos
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
WEB_DIR = ROOT_DIR / "web"

# Arquivos
LOJAS_XLSX = DATA_DIR / "Endereço Lojas.xlsx"
FUNCIONARIOS_XLSX = DATA_DIR / "Endereço Vendedores.xlsx"
DADOS_JSON = OUTPUT_DIR / "dados_alocacao.json"
CACHE_JSON = OUTPUT_DIR / "cache_geocoding.json"

# Carrega .env
load_dotenv(ROOT_DIR / ".env")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Regras de negócio
DISTANCIA_MAXIMA_KM = 50
FATOR_TEMPO_MIN_POR_KM = 2.5  # minutos por km em SP (trânsito)
CUSTO_KM = 0.50  # R$ por km
DIAS_UTEIS_MES = 22

# Cores por zona/UN
CORES_ZONAS = {
    "OL": {"nome": "Zona Leste", "cor": "#e74c3c"},
    "ON": {"nome": "Zona Norte", "cor": "#3498db"},
    "OC": {"nome": "Zona Central", "cor": "#9b59b6"},
    "OS": {"nome": "Zona Sul", "cor": "#27ae60"},
    "OO": {"nome": "Zona Oeste", "cor": "#f39c12"},
}
