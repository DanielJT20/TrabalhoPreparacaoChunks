import pandas as pd
import json
import re
import unicodedata

def normalizar_coluna(col):
    if not isinstance(col, str): return col
    nfkd_form = unicodedata.normalize('NFKD', col)
    col = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    col = re.sub(r'\s+', ' ', col).strip().upper()
    return col

def safe_float(valor):
    try:
        if pd.isna(valor): return 0.0
        s = str(valor).replace(',', '.').strip()
        if not s or s == '' or s.isspace(): return 0.0
        return float(s)
    except: return 0.0

def gerar_chunks_trabalho():
    url = "https://raw.githubusercontent.com/alvaroriz/datascience_datasets/refs/heads/main/Catalogo-Produtos.csv"
    print("Processando catálogo completo (PF e PMC)...")
    
    try:
        df = pd.read_csv(url, sep=';', quotechar='"', on_bad_lines='skip', encoding='utf-8')
    except:
        df = pd.read_csv(url, sep=';', quotechar='"', on_bad_lines='skip', encoding='latin-1')

    df.columns = [normalizar_coluna(c) for c in df.columns]
    chunks_finais = []

    for _, row in df.iterrows():
        nome = str(row.get('FAMILIA', row.get('PRODUTO', 'N/A')))
        codigo = str(row.get('CODIGO SAP', row.get('CODIGO', '0')))
        apresentacao = str(row.get('APRESENTACAO', 'N/A'))
        
        precos_pf = {}
        precos_pmc = {}
        
        for aliq in ['0', '12', '17', '17.5', '18', '19', '20']:
            aliq_str = aliq.replace('.', ',')
            col_pf = [c for c in df.columns if aliq_str in c and '(PF)' in c]
            col_pmc = [c for c in df.columns if aliq_str in c and '(PMC)' in c]
            
            precos_pf[aliq] = safe_float(row.get(col_pf[0])) if col_pf else 0.0
            precos_pmc[aliq] = safe_float(row.get(col_pmc[0])) if col_pmc else 0.0

        chunk = {
            "id": codigo,
            "text_chunk": f"PRODUTO: {nome} | CODIGO: {codigo} | APRESENTACAO: {apresentacao}",
            "metadata": {
                "nome_comercial": nome,
                "apresentacao": apresentacao,
                "precos_pf": precos_pf,
                "precos_pmc": precos_pmc
            }
        }
        chunks_finais.append(chunk)

    with open('chunks_produtos.json', 'w', encoding='utf-8') as f:
        json.dump(chunks_finais, f, indent=4, ensure_ascii=False)
    print("Sucesso! Arquivo pronto para upload no Gemini.")

if __name__ == "__main__":
    gerar_chunks_trabalho()