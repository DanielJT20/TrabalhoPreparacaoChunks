# Processador de Catálogo de Produtos (ETL & RAG)

Este projeto automatiza a extração, tratamento e estruturação de dados de um catálogo de produtos farmacêuticos. O script em Python consome uma base de dados remota (CSV), realiza a limpeza dos dados e exporta o conteúdo em formato JSON estruturado em "chunks", ideal para ser utilizado em sistemas de busca semântica ou IA (RAG - Retrieval-Augmented Generation).

## 🚀 Funcionalidades

- **Carga Automática:** Faz o download do catálogo diretamente de um repositório remoto via pandas.
- **Limpeza de Dados:** Padroniza nomes de colunas, remove espaços extras e trata valores decimais e nulos.
- **Cálculo de Preço:** Prioriza o ICMS de 17% (base), com fallback para 18% caso o valor base seja nulo.
- **Geração de Chunks:** Cria uma "Âncora Semântica" no campo `text_chunk`, facilitando a busca por princípio ativo, nome comercial ou código.
- **Exportação:** Gera o arquivo `chunks_produtos.json` pronto para indexação.

## 📋 Pré-requisitos

Antes de rodar o script, você precisará ter o Python instalado e a biblioteca `pandas`.

```bash
pip install pandas
🛠️ Como Executar
Clone ou baixe os arquivos:
Certifique-se de que o arquivo script.py esteja na sua pasta de trabalho.

Execute o script:
Você pode rodar o script via terminal ou dentro de uma IDE (VS Code, PyCharm, etc.):

Bash
python script.py
Verifique a Saída:
Após a execução, uma mensagem de sucesso aparecerá no console e o arquivo chunks_produtos.json será criado no mesmo diretório.

📂 Estrutura de Arquivos
script.py: Script principal contendo a lógica de extração e transformação.

chunks_produtos.json: (Gerado após execução) Arquivo contendo os dados estruturados com metadados.

📄 Exemplo do Dado Gerado
Cada objeto no JSON segue este padrão:

JSON
{
    "id": "1000001",
    "text_chunk": "PRODUTO: ACCUVIT | CÓDIGO: 1000001 | PRINCÍPIO ATIVO: POLIVITAMÍNICO; | APRESENTAÇÃO: ACCUVIT COMREV FRX30",
    "metadata": {
        "nome_comercial": "ACCUVIT",
        "principio_ativo": "POLIVITAMÍNICO",
        "apresentacao": "ACCUVIT COMREV FRX30",
        "preco_base": 91.44
    }

💎 Como Configurar o Gem (Google Gemini)
Para testar os chunks e gerar os orçamentos, siga estas etapas:

Acesse o Gemini: Vá para a interface do Google Gemini.

Criar Novo Gem: Clique em "Gerenciar Gems" (ou ícone de +) e depois em "Novo Gem".

Upload de Conhecimento (Knowledge): Faça o upload do arquivo chunks_produtos.json gerado pelo script.

Configurar Instruções: No campo de instruções, utilize o prompt que define as regras de negócio:

Extrair quantidades e produtos.

Identificar o tipo de cliente e UF.

Aplicar 20% de ICMS para clientes do Rio de Janeiro (RJ).

Saída estrita em formato JSON.

📊 Resultado Esperado
O script gera um arquivo estruturado onde cada produto é um "chunk" enriquecido.

