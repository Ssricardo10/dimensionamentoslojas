"""Script de teste para validar a alocação de coordenadores."""

from src.models import Loja
from src.coordinators import CoordenadorAllocator


def teste_alocacao():
    """Testa a alocação com dados de exemplo."""
    
    # Cria lojas de teste
    lojas_teste = [
        # Lojas grandes (>10 PAs)
        Loja(id=1, nome="Agência Centro", un="OC", municipio="São Paulo", 
             endereco="Av. Paulista, 1000", horario="7H AS 18H",
             vagas_agentes=15, vagas_triagistas=2, total_hcs=90, status="Ativo",
             lat=-23.5505, lng=-46.6333),
        
        Loja(id=2, nome="Agência Zona Leste", un="OL", municipio="Itaquera",
             endereco="Rua X, 500", horario="8H AS 17H",
             vagas_agentes=12, vagas_triagistas=1, total_hcs=60, status="Ativo",
             lat=-23.5236, lng=-46.4724),
        
        # Lojas médias (5-10 PAs)
        Loja(id=3, nome="Agência Zona Norte", un="ON", municipio="Santana",
             endereco="Rua Y, 300", horario="8H AS 16H",
             vagas_agentes=8, vagas_triagistas=1, total_hcs=40, status="Ativo",
             lat=-23.5073, lng=-46.6289),
        
        Loja(id=4, nome="Agência Zona Sul", un="OS", municipio="Santo Amaro",
             endereco="Rua Z, 200", horario="8H AS 16H",
             vagas_agentes=6, vagas_triagistas=1, total_hcs=30, status="Ativo",
             lat=-23.6561, lng=-46.7367),
        
        # Lojas pequenas (≤2 PAs) — candidatas a agrupamento
        Loja(id=5, nome="Agência Pequena 1", un="OO", municipio="Lapa",
             endereco="Rua A, 100", horario="8H AS 14H",
             vagas_agentes=2, vagas_triagistas=0, total_hcs=10, status="Ativo",
             lat=-23.5312, lng=-46.6834),
        
        Loja(id=6, nome="Agência Pequena 2", un="OO", municipio="Pinheiros",
             endereco="Rua B, 150", horario="9H AS 12H",
             vagas_agentes=1, vagas_triagistas=0, total_hcs=5, status="Ativo",
             lat=-23.5460, lng=-46.6926),
        
        Loja(id=7, nome="Agência Pequena 3", un="OO", municipio="Vila Madalena",
             endereco="Rua C, 180", horario="8H AS 12H",
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
    
    print(f"\n📈 DISTRIBUIÇÃO")
    resumo = resultado['resumo_por_tipo']
    print(f"   Lojas Grandes (>10 PAs): {resumo['lojas_grandes']}")
    print(f"   Lojas ≤10 PAs: {resumo['lojas_pequenas']}")
    print(f"   Lojas com 2 turnos: {resumo['lojas_2_turnos']}")
    print(f"   Grupos Formados: {resumo['grupos_formados']}")
    print(f"   Necessidade bruta: {resumo['bruto_sem_agrupamento']}")
    print(f"   Economia agrupamento: {resumo['economia']}")
    print(f"   Alocados: {resumo['alocados']}")
    
    print(f"\n📋 COORDENADORES ALOCADOS")
    for coord in resultado['coordenadores']:
        extra = ""
        if coord['tipo'] == 'agrupador':
            nomes = [g['loja_nome'] for g in coord.get('grupo_lojas', [])]
            extra = f" [Grupo: {', '.join(nomes)}, dist={coord.get('distancia_km',0)}km]"
        elif coord['tipo'] == 'dupla':
            extra = f" [dupla_com={coord.get('dupla_com','')}]"
        print(f"   Coord #{coord['id']:03d} | {coord['tipo']:10s} | {coord['turno']:12s} | "
              f"{coord['vagas_agentes']:2d} PAs | {coord['loja_nome']}{extra}")
    
    print(f"\n🤝 GRUPOS DE LOJAS")
    for grupo in resultado['grupos_pequenas']:
        print(f"\n   Coordenador #{grupo['coordenador_id']:03d} ({grupo['num_lojas']} lojas)")
        print(f"      Distância máxima: {grupo['distancia_maxima_km']} km")
        print(f"      Tempo deslocamento: ~{grupo['tempo_deslocamento_min']} min")
        for loja in grupo['lojas']:
            print(f"      └─ {loja['loja_nome']} ({loja['vagas_agentes']} PAs, {loja['horario']})")
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO")
    print("="*70 + "\n")
    
    return resultado


if __name__ == "__main__":
    teste_alocacao()
