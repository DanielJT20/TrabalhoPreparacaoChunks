import pandas as pd
import json

def processar_catalogo():
    url = "https://raw.githubusercontent.com/alvaroriz/datascience_datasets/refs/heads/main/Catalogo-Produtos.csv"
    
    try:
        # Carregamos o CSV tratando as linhas problemáticas
       # Trocamos o sep para ';'
        df = pd.read_csv(
            url, 
            sep=';', 
            quotechar='"', 
            on_bad_lines='skip', 
            encoding='utf-8'
        )
        
        # REMÉDIO PARA O KEYERROR: Remove espaços extras e padroniza os nomes das colunas
        df.columns = df.columns.str.strip().str.upper()
        
        print("Colunas encontradas no arquivo:", df.columns.tolist())
        print(f"Catálogo carregado! {len(df)} produtos encontrados.")
        
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return

    chunks = []
    for _, row in df.iterrows():
        # Usamos .get() ou nomes padronizados para evitar novos KeyErrors
        # Ajuste com os nomes EXATOS que o terminal imprimiu
        nome = row.get('FAMÍLIA', 'N/A')
        codigo = row.get('CÓDIGO SAP', 'N/A')
        ativo = row.get('PRINCIPIO ATIVO', 'N/A')
        apresentacao = row.get('APRESENTAÇÃO', 'N/A')
        preco = row.get('ICMS 0 % (PF)', 0.0)

        # Montagem do conteúdo semântico para a LLM [cite: 6, 7]
        conteudo_semantico = (
            f"PRODUTO: {nome} | "
            f"CODIGO: {codigo} | "
            f"PRINCIPIO ATIVO: {ativo} | "
            f"APRESENTAÇÃO: {apresentacao}"
        )
        
        chunks.append({
            "id": str(codigo),
            "text_chunk": conteudo_semantico,
            "metadata": {
                "nome": nome,
                "ativo": ativo,
                "preco_base": preco
            }
        })

    # Salva o JSON final para a entrega 
    with open('chunks_produtos.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)
    
    print("Arquivo 'chunks_produtos.json' gerado com sucesso!")

if __name__ == "__main__":
    processar_catalogo()