"""Script principal: gera dados_alocacao.json."""

import sys
import json
from pathlib import Path

# Permite importar src/ de qualquer lugar
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import DADOS_JSON, OUTPUT_DIR
from src.geocoding import Geocoder
from src.allocation import load_lojas, load_funcionarios, build_json


def main():
    print("\n" + "=" * 60)
    print("  SABESP - Sistema de Alocação por Proximidade v3.0")
    print("=" * 60)

    # Geocoder
    print("\n🔑 Inicializando Google Maps API...")
    geocoder = Geocoder()

    # Lojas
    print("\n📍 Geocodificando lojas...")
    lojas = load_lojas(geocoder)
    print(f"  ✓ {len(lojas)} lojas processadas")

    # Funcionários
    print("\n👥 Geocodificando funcionários...")
    funcionarios = load_funcionarios(geocoder)
    print(f"  ✓ {len(funcionarios)} funcionários processados")

    # Estatísticas de geocoding
    print("\n📊 Estatísticas de geocoding:")
    geocoder.print_stats()

    # Gera JSON
    print("\n💾 Gerando JSON...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dados = build_json(lojas, funcionarios)
    DADOS_JSON.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  ✓ {DADOS_JSON}")

    print("\n" + "=" * 60)
    print(f"  ✅ {len(lojas)} lojas | {len(funcionarios)} funcionários")
    print(f"  📁 {DADOS_JSON}")
    print(f"  🚀 Próximo: python scripts/serve.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
