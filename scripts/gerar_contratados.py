#!/usr/bin/env python3
"""
Gera JSON com dados de contratados por loja
"""
import json
import pandas as pd


def normalize_loja(value):
    loja = '' if pd.isna(value) else str(value)
    loja = ' '.join(loja.split()).strip()
    return '' if loja == '-' else loja


TITULOS_CONTAVEIS = {
    'ANALISTA ATENDIMENTO COMERCIAL TRADE',
    'PROMOTOR DIGITAL TRADE',
}

# Lê arquivo nominal
dn = pd.read_excel('Sabesp Trade - Nominal Hcs - 11.05.2026.xlsx', sheet_name='Nominal Geral')
print('✓ Arquivo nominal carregado')
print(f'  Total linhas: {len(dn)}')
print(f'  CPF nulos: {dn["CPF"].isna().sum()}')
print(f'  Loja nulas: {dn["LOJA"].isna().sum()}')
print()

dn['LOJA_NORMALIZADA'] = dn['LOJA'].apply(normalize_loja)
dn_validas = dn[dn['LOJA_NORMALIZADA'] != ''].copy()
dn_contaveis = dn_validas[
    dn_validas['TÍTULO'].astype(str).str.strip().isin(TITULOS_CONTAVEIS)
].copy()
ativos = dn_contaveis[
    dn_contaveis['DESCRIÇÃO'].astype(str).str.strip().str.lower().eq('trabalhando')
    & dn_contaveis['DEMISSÃO'].isna()
].copy()
cpfs_ativos = set(
    ativos['CPF'].dropna().map(lambda cpf: str(int(cpf)) if isinstance(cpf, float) else str(cpf).strip())
)

# Agregar por loja
contratados_por_loja = dn_contaveis.groupby('LOJA_NORMALIZADA').size().to_dict()
ativos_por_loja = ativos.groupby('LOJA_NORMALIZADA').size().to_dict()
print('Contratados por loja (top 15):')
for loja, count in sorted(contratados_por_loja.items(), key=lambda x: -x[1])[:15]:
    print(f'  {loja}: {count}')
print()

print('Ativos por loja (top 15):')
for loja, count in sorted(ativos_por_loja.items(), key=lambda x: -x[1])[:15]:
    print(f'  {loja}: {count}')
print()

# Criar mapa CPF -> Loja para marcar no modal
cpf_map = {}
cpf_status_map = {}
for _, row in dn_contaveis.iterrows():
    try:
        cpf_raw = row['CPF']
        if pd.isna(cpf_raw):
            continue
        # Trata como float (CPF é numérico no Excel)
        cpf_str = str(int(cpf_raw)) if isinstance(cpf_raw, float) else str(cpf_raw).strip()
        loja = normalize_loja(row['LOJA'])
        if cpf_str and loja:
            cpf_map[cpf_str] = loja
            cpf_status_map[cpf_str] = {
                'loja': loja,
                'ativo': cpf_str in cpfs_ativos,
            }
    except:
        pass

print(f'CPF mapeados: {len(cpf_map)}')
if cpf_map:
    amostra = list(cpf_map.items())[:3]
    for cpf, loja in amostra:
        print(f'  {cpf}: {loja}')
print()

# Salva os dados
with open('output/contratados_por_loja.json', 'w', encoding='utf-8') as f:
    json.dump(contratados_por_loja, f, indent=2, ensure_ascii=False)

with open('output/ativos_por_loja.json', 'w', encoding='utf-8') as f:
    json.dump(ativos_por_loja, f, indent=2, ensure_ascii=False)

with open('output/cpf_loja_map.json', 'w', encoding='utf-8') as f:
    json.dump(cpf_map, f, indent=2, ensure_ascii=False)

with open('output/cpf_status_map.json', 'w', encoding='utf-8') as f:
    json.dump(cpf_status_map, f, indent=2, ensure_ascii=False)

print('✓ Dados salvos em:')
print('  - output/contratados_por_loja.json')
print('  - output/ativos_por_loja.json')
print('  - output/cpf_loja_map.json')
print('  - output/cpf_status_map.json')
