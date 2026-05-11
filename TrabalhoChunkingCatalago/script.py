import pandas as pd
import json

def gerar_chunks_trabalho():
    # URL do catálogo fornecida no enunciado 
    url = "https://raw.githubusercontent.com/alvaroriz/datascience_datasets/refs/heads/main/Catalogo-Produtos.csv"
    
    print("Iniciando o processamento do catálogo...")
    
    try:
        # Carregamento robusto: tratando separador, decimal e linhas problemáticas
        df = pd.read_csv(
            url, 
            sep=';', 
            quotechar='"', 
            on_bad_lines='skip', 
            encoding='utf-8',
            decimal=','  # Converte '12,50' para 12.5 (float)
        )
        
        # Padronização de colunas (remove espaços e coloca em maiúsculo)
        df.columns = df.columns.str.strip().str.upper()
        
        print(f"Catálogo carregado com sucesso! {len(df)} produtos encontrados.")
        
    except Exception as e:
        print(f"Erro fatal ao carregar o arquivo: {e}")
        return

    chunks_finais = []

    for _, row in df.iterrows():
        # Extração baseada na estrutura real do seu arquivo
        # Utilizamos .get para evitar quebras caso alguma coluna falhe
        nome = str(row.get('FAMÍLIA', 'N/A'))
        codigo = str(row.get('CÓDIGO SAP', 'N/A'))
        ativo = str(row.get('PRINCIPIO ATIVO', 'N/A'))
        apresentacao = str(row.get('APRESENTAÇÃO', 'N/A'))
        
        # Priorizamos o Preço Fábrica (PF) sem impostos iniciais como base
        preco_base = row.get('ICMS 0 % (PF)', 0.0)
        
        # Se o PF 0% estiver zerado, tentamos o PF 18% (comum em SP/RJ)
        if preco_base == 0.0 or pd.isna(preco_base):
            preco_base = row.get('ICMS 18 %  (PF)', 0.0)

        # Montagem da 'Âncora Semântica' (Estratégia para busca com LLM) [cite: 6, 7]
        # Incluímos sinônimos e chaves para que a LLM encontre o produto por qualquer termo
        conteudo_para_llm = (
            f"PRODUTO: {nome} | "
            f"CÓDIGO: {codigo} | "
            f"PRINCÍPIO ATIVO: {ativo} | "
            f"APRESENTAÇÃO: {apresentacao}"
        )
        
        # Estrutura de Chunk solicitada
        chunk = {
            "id": codigo,
            "text_chunk": conteudo_para_llm,
            "metadata": {
                "nome_comercial": nome,
                "principio_ativo": ativo,
                "apresentacao": apresentacao,
                "preco_base": float(preco_base) if not pd.isna(preco_base) else 0.0
            }
        }
        chunks_finais.append(chunk)

    # Exportação para o arquivo JSON (Entrega do Item 1) 
    nome_arquivo = 'chunks_produtos.json'
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(chunks_finais, f, indent=4, ensure_ascii=False)
    
    print(f"\nConcluído! Arquivo '{nome_arquivo}' gerado com sucesso.")
    print(f"Total de chunks criados: {len(chunks_finais)}")
    print("Exemplo do primeiro chunk:")
    print(json.dumps(chunks_finais[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    gerar_chunks_trabalho()