# Processador de Catálogo de Produtos (ETL & RAG) 🚀

Este projeto automatiza a extração, tratamento e estruturação de dados de um catálogo de produtos farmacêuticos. O script transforma uma base bruta (CSV) em um arquivo JSON estruturado em "chunks", otimizado para sistemas de **Busca Semântica** e **RAG (Retrieval-Augmented Generation)**.

## 🛠️ Funcionalidades

- **Extração Automática:** Consome o catálogo atualizado diretamente de um repositório remoto via `pandas`.
- **Data Cleaning:** Padronização de colunas (uppercase/strip), tratamento de valores nulos e conversão de tipos decimais.
- **Lógica de Pricing:** Cálculo inteligente de preço base priorizando ICMS de 17% com fallback para 18%.
- **Âncora Semântica:** Criação de `text_chunk` enriquecido para facilitar a recuperação de informações por LLMs.
- **Saída Estruturada:** Geração de metadados prontos para indexação em vetores.

## 📋 Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado. A única dependência externa é a biblioteca `pandas`.

```bash
pip install pandas
🚀 Como Executar
Preparação: Salve o arquivo script.py em uma pasta de sua preferência.

Execução: Rode o script via terminal:

Bash
python script.py
Resultado: O arquivo chunks_produtos.json será gerado automaticamente no mesmo diretório com o log de sucesso no console.

📂 Estrutura do Projeto
script.py: Core do sistema (Extração, Transformação e Carga).

chunks_produtos.json: Base de conhecimento gerada para a IA.

📄 Exemplo do Dado Gerado
O formato de saída é otimizado para que a IA entenda o contexto de cada produto individualmente:

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
💎 Configuração no Google Gemini (Gems)
Para utilizar este projeto como cérebro de um assistente de vendas/orçamentos:

Criação: No Google Gemini, vá em Gerenciar Gems > Novo Gem.

Conhecimento (Knowledge): Faça o upload do arquivo chunks_produtos.json.

Instruções de Sistema: Utilize o prompt abaixo para configurar o comportamento:

"Você é um assistente de vendas farmacêuticas. Use o arquivo de conhecimento fornecido para consultar preços e produtos.
Regras de Negócio:

Extraia sempre a quantidade e o nome do produto do pedido do usuário.

Se o cliente for do Rio de Janeiro (RJ), aplique uma taxa total de 20% sobre o preco_base.

Responda estritamente em formato JSON contendo: Produto, Preço Unitário, Preço Total e Impostos Aplicados."

📊 Resultado Esperado
Ao final, você terá um pipeline que transforma dados tabulares estáticos em uma base de conhecimento dinâmica, capaz de alimentar agentes de IA para automação de orçamentos complexos.