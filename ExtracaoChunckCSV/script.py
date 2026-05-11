import pandas as pd
import json

file_input = "Catalogo-Produtos.xlsx - Planilha1.csv"
file_output = "catalogo_produtos.json"

try:
    df = pd.read_csv(file_input)

    def limpar_preco(valor):
        try:
            if pd.isna(valor): return 0.0
            return float(str(valor).replace(',', '.'))
        except:
            return 0.0

    def limpar_estoque(valor):
        try:
            if pd.isna(valor): return 0
            return int(float(str(valor).replace(',', '.')))
        except:
            return 0

    catalogo = []
    for _, row in df.iterrows():
        preco_base = limpar_preco(row['Preço (R$)'])
        preco_promo = limpar_preco(row['Preço Promo (R$)'])
        
        desconto = 0
        if preco_base > 0:
            desconto = int((1 - (preco_promo / preco_base)) * 100)

        produto = {
            "sku": row['SKU'],
            "nome": row['Nome do Produto'],
            "marca": row['Marca'],
            "modelo": row['Modelo'],
            "categoria": f"{row['Categoria']} > {row['Subcategoria']}",
            "financeiro": {
                "preco_original": preco_base,
                "preco_promocional": preco_promo,
                "desconto_percentual": desconto
            },
            "detalhes": {
                "resumo": row['Descrição Curta'],
                "especificacoes_completas": row['Descrição Completa'],
                "garantia": row['Garantia']
            },
            "logistica": {
                "estoque_atual": limpar_estoque(row['Estoque (un)']),
                "peso_kg": limpar_preco(row['Peso (kg)']),
                "dimensoes": row['Dimensões (cm)']
            },
            "tags": str(row['Tags / Palavras-chave']).split(',') if pd.notna(row['Tags / Palavras-chave']) else []
        }
        catalogo.append(produto)

    with open(file_output, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, indent=4, ensure_ascii=False)

    print(f"Sucesso! {len(catalogo)} produtos convertidos para {file_output}")

except Exception as e:
    print(f"Erro ao processar: {e}")