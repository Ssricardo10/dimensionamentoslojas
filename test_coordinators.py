"""Script de teste para validar a alocação de coordenadores."""

from src.models import Loja
from src.coordinators import CoordenadorAllocator


def teste_alocacao():
    """Testa a alocação com dados de exemplo."""
    
    # Cria lojas de teste
    lojas_teste = [
        # Lojas grandes (>10 PAs)
        Loja(id=1, nome="Agência Centro", un="OC", municipio="São Paulo", 
             endereco="Av. Paulista, 1000", horario="Seg-Sex 6h às 22h",
             vagas_agentes=15, vagas_triagistas=2, total_hcs=90, status="Ativo",
             lat=-23.5505, lng=-46.6333),
        
        Loja(id=2, nome="Agência Zona Leste", un="OL", municipio="Itaquera",
             endereco="Rua X, 500", horario="Seg-Feriados 8h às 18h",
             vagas_agentes=12, vagas_triagistas=1, total_hcs=60, status="Ativo",
             lat=-23.5236, lng=-46.4724),
        
        # Lojas médias (5-10 PAs)
        Loja(id=3, nome="Agência Zona Norte", un="ON", municipio="Santana",
             endereco="Rua Y, 300", horario="Seg-Sex 8h às 18h",
             vagas_agentes=8, vagas_triagistas=1, total_hcs=40, status="Ativo",
             lat=-23.5073, lng=-46.6289),
        
        Loja(id=4, nome="Agência Zona Sul", un="OS", municipio="Santo Amaro",
             endereco="Rua Z, 200", horario="Seg-Sex 8h às 18h",
             vagas_agentes=6, vagas_triagistas=1, total_hcs=30, status="Ativo",
             lat=-23.6561, lng=-46.7367),
        
        # Lojas pequenas (≤2 PAs)
        Loja(id=5, nome="Agência Pequena 1", un="OO", municipio="Lapa",
             endereco="Rua A, 100", horario="Seg-Sex 8h às 18h",
             vagas_agentes=2, vagas_triagistas=0, total_hcs=10, status="Ativo",
             lat=-23.5312, lng=-46.6834),
        
        Loja(id=6, nome="Agência Pequena 2", un="OO", municipio="Pinheiros",
             endereco="Rua B, 150", horario="Seg-Sex 8h às 18h",
             vagas_agentes=1, vagas_triagistas=0, total_hcs=5, status="Ativo",
             lat=-23.5460, lng=-46.6926),
        
        Loja(id=7, nome="Agência Pequena 3", un="OO", municipio="Vila Madalena",
             endereco="Rua C, 180", horario="Seg-Sex 8h às 18h",
             vagas_agentes=2, vagas_triagistas=0, total_hcs=10, status="Ativo",
             lat=-23.5580, lng=-46.6818),
    ]
    
    # Executa alocação
    allocator = CoordenadorAllocator(lojas_teste)
    resultado = allocator.alocar()
    
    # Exibe resultados
    print("\n" + "="*70)
    print("📊 TESTE DE ALOCAÇÃO DE COORDENADORES")
    print("="*70)
    
    print(f"\n📌 RESUMO EXECUTIVO")
    print(f"   Total de Coordenadores Alocados: {resultado['total_coordenadores']}")
    print(f"   Meta: {resultado['meta_coordenadores']}")
    print(f"   Status: {resultado['status']}")
    
    print(f"\n📈 DISTRIBUIÇÃO POR TIPO DE LOJA")
    resumo = resultado['resumo_por_tipo']
    print(f"   Lojas Grandes (>10 PAs): {resumo['lojas_grandes']}")
    print(f"   Lojas Pequenas (≤2 PAs): {resumo['lojas_pequenas']}")
    print(f"   Grupos Pequenas: {resumo['grupos_pequenas']}")
    print(f"   Alocados: {resumo['alocados']}/{resumo['necessidade_inicial']}")
    
    print(f"\n📋 COORDENADORES ALOCADOS POR TURNO")
    for loja_id in range(1, 8):
        coords_loja = [c for c in resultado['coordenadores'] if c['loja_id'] == loja_id]
        if coords_loja:
            loja_nome = coords_loja[0]['loja_nome']
            vagas = coords_loja[0]['vagas_agentes']
            print(f"\n   {loja_nome} ({vagas} PAs):")
            for coord in coords_loja:
                print(f"      ✓ Coord. #{coord['id']:03d} | {coord['turno']:8} | {coord['tipo']}")
    
    print(f"\n🤝 GRUPOS DE LOJAS PEQUENAS")
    for grupo in resultado['grupos_pequenas']:
        print(f"\n   Coordenador #{grupo['coordenador_id']:03d} ({grupo['num_lojas']} lojas)")
        print(f"      Distância máxima: {grupo['distancia_maxima_km']} km")
        print(f"      Tempo deslocamento: {grupo['tempo_deslocamento_min']} min")
        for loja in grupo['lojas']:
            print(f"      └─ {loja['loja_nome']} ({loja['vagas_agentes']} analistas)")
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO")
    print("="*70 + "\n")
    
    return resultado


if __name__ == "__main__":
    teste_alocacao()
