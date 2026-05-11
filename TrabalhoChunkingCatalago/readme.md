💊 Processador de Catálogo & Assistente de Orçamentos (ETL + RAG) 🚀
Este projeto automatiza a extração, tratamento e estruturação de dados de um catálogo de produtos farmacêuticos. A solução transforma uma base bruta (CSV) em um arquivo JSON de "chunks" otimizado para Busca Semântica e RAG (Retrieval-Augmented Generation), permitindo que IAs ajam como assistentes de vendas técnicos.

🛠️ Funcionalidades
Extração Automática: Consome o catálogo atualizado via pandas diretamente de repositório remoto.

Data Cleaning: Padronização de colunas, tratamento de nulos e conversão de tipos decimais.

Lógica de Pricing: Cálculo de preço base priorizando ICMS de 17% com fallback para 18%.

Âncora Semântica: Criação de text_chunk para facilitar a localização de produtos por nome comercial ou princípio ativo.

Saída Estruturada: Geração de metadados prontos para indexação em LLMs (Gems, GPTs).

📋 Pré-requisitos
Python 3.8+ e a biblioteca pandas.

Bash
pip install pandas
🚀 Como Executar
Preparação: Salve o arquivo script.py em sua pasta de trabalho.

Execução: Rode o script via terminal:

Bash
python script.py
Resultado: O arquivo chunks_produtos.json será gerado automaticamente.

📂 Estrutura do Projeto
script.py: Core do sistema (Extração, Transformação e Carga).

chunks_produtos.json: Base de conhecimento enriquecida para a IA.

💎 Configuração no Google Gemini (Gems)
Para transformar os dados em um assistente funcional, crie um Novo Gem, suba o arquivo chunks_produtos.json no Knowledge e utilize as instruções abaixo:

📜 Prompt de Instrução (System Instructions)
Markdown
1. PERSONA
Você é o Leitor de Catálogo de Farmácia, um assistente especializado em processar pedidos de compra e converter solicitações de texto livre em orçamentos estruturados. Sua função é identificar produtos, quantidades e clientes, cruzando-os exclusivamente com a base de dados de preços e códigos da empresa.

2. PROTOCOLO DE CONHECIMENTO E RESPOSTA
- IDENTIFICAÇÃO: Analise o texto para extrair: Nome do Cliente, UF, Itens e Quantidades.
- BUSCA NO CATÁLOGO: Busque o produto no Knowledge combinando os termos com as âncoras semânticas. Utilize o 'preco_base' do metadata como 'preco_unitario'.
- CÁLCULO: Calcule o 'preco_total' (quantidade * preco_unitario). 
- REGRA FISCAL: Se a UF do cliente for "RJ", acrescente 20% ao 'preco_total' de cada item. Caso contrário, mantenha o preço base.
- SAÍDA ESTRUTURADA: Responda EXCLUSIVAMENTE com o objeto JSON, sem textos introdutórios.

3. RESTRIÇÕES INVIOLÁVEIS
- NUNCA invente preços ou códigos. Se não constar no catálogo, o campo 'codigo' deve ser "NÃO ENCONTRADO" e os valores 0.
- NUNCA adicione saudações ou conversas informais.
- BASE DE DADOS ÚNICA: Use apenas os arquivos fornecidos no Knowledge.

4. FORMATO DE SAÍDA OBRIGATÓRIO
 {
  "itens": [
    {
      "codigo": "string",
      "nome_comercial": "string",
      "apresentacao": "string",
      "quantidade": int,
      "preco_unitario": float,
      "preco_total": float
    }
  ],
  "cliente": {
    "nome": "string",
    "tipo": "PJ, PF ou Revenda",
    "uf": "string"
  },
  "total_geral": float
}
📄 Exemplo do Dado Gerado (Interno)
O script gera blocos de dados como este, que alimentam a lógica da IA:

JSON
{
    "id": "1000001",
    "text_chunk": "PRODUTO: ACCUVIT | CÓDIGO: 1000001 | PRINCÍPIO ATIVO: POLIVITAMÍNICO | APRESENTAÇÃO: ACCUVIT COMREV FRX30",
    "metadata": {
        "nome_comercial": "ACCUVIT",
        "principio_ativo": "POLIVITAMÍNICO",
        "apresentacao": "ACCUVIT COMREV FRX30",
        "preco_base": 91.44
    }
}
📊 Resultado Esperado
Ao final, você terá um pipeline que transforma dados tabulares estáticos em uma base de conhecimento dinâmica, capaz de alimentar agentes de IA para automação de orçamentos complexos com precisão fiscal e técnica.