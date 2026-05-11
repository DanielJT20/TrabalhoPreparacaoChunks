import fitz  # PyMuPDF
import re
import os
import unicodedata

# --- CONFIGURAÇÕES DO PROTOCOLO V3.0 ---
ARQUIVO_PDF = "Manual-Ferias-SIGRH.pdf"
BASE_DIR = "Corpus_SIGRH_Final"

def slugify(text):
    """Gera nomes de arquivos e pastas limpos, sem acentos ou símbolos."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def formatar_nome_arquivo(idx, secao_num, tema, entidade):
    """Cria um nome de arquivo padronizado: 001-sec3-solicitacao-servidor.txt."""
    tema_slug = slugify(tema)[:25]
    entidade_slug = slugify(entidade)
    return f"{idx:03d}-sec{secao_num}-{tema_slug}-{entidade_slug}.txt"

def extrair_metadados(idx, secao, sub, entidade, dimensao, texto, overlap, arquivo_nome):
    """Gera o cabeçalho de metadados obrigatório do protocolo."""
    tokens = int(len(texto.split()) * 1.3)
    return f"""[TIPO: Manual/Procedimento]
[FONTE: {ARQUIVO_PDF}]
[SEÇÃO: {secao}]
[PÁGINA: Extração Integral]
[DIMENSÃO_PRIMÁRIA: {dimensao}]
[ENTIDADE: {entidade}]
[TEMA: {sub}]
[CONTEXTO_HIERÁRQUICO: Manual > {secao} > {sub}]
[CHUNKS_RELACIONADOS: {idx-1:03d} if idx > 1 else "None"]
[TIPO_ESTRUTURA: Normal]
[TAMANHO: {tokens} tokens]
[EXCEÇÃO_TAMANHO: Não]
[OVERLAP: {"Sim" if overlap else "Não"}]
[NOME CHUNK: {slugify(entidade)}]
[NOME ARQUIVO CHUNK: {arquivo_nome}]"""

def processar_manual():
    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    doc = fitz.open(ARQUIVO_PDF)
    
    # Extração literal das 21 páginas do manual[cite: 2].
    texto_bruto = ""
    for pagina in doc:
        txt = pagina.get_text("text")
        # Etapa 1: Limpeza de ruído visual.
        txt = re.sub(r'(Manual de Férias|GEBEN/DGDP/SEA|Página \d+ de \d+)', '', txt)
        texto_bruto += txt

    # Divide pelas seções principais (1, 2, 3...)[cite: 2].
    secoes_principais = re.split(r'\n(\d\s[A-ZÀ-Ú].+)', texto_bruto)
    
    global_id = 1
    buffer_overlap = ""

    for i in range(1, len(secoes_principais), 2):
        titulo_completo = secoes_principais[i].strip()
        secao_num = titulo_completo.split()[0]
        conteudo_secao = secoes_principais[i+1]
        
        # Cria pasta física por seção[cite: 3].
        pasta_secao = f"secao_{secao_num}_{slugify(titulo_completo[2:])}"
        caminho_secao = os.path.join(BASE_DIR, pasta_secao)
        if not os.path.exists(caminho_secao): os.makedirs(caminho_secao)
        
        # Define dimensão primária (Ator para Seção 3, Tópico para as demais)[cite: 3].
        dimensao = "ATOR/RESPONSÁVEL" if secao_num == "3" else "TÓPICO/CLÁUSULA"
        
        # Divide por subtópicos (Ex: 2.1, 3.1.1)[cite: 2].
        sub_temas = re.split(r'(\d\.\d\.?\d?\s[A-ZÀ-Ú].+)', conteudo_secao)
        
        for j in range(1, len(sub_temas), 2):
            tema = sub_temas[j].strip()
            corpo = sub_temas[j+1]
            
            # Seção 3: Divisão rigorosa por atores conforme protocolo[cite: 3].
            atores = ["Servidor", "Gestor/Superior imediato", "Setorial/Seccional de Gestão de Pessoas"]
            if dimensao == "ATOR/RESPONSÁVEL" and any(a in corpo for a in atores):
                blocos = re.split(r'\n(Servidor|Gestor/Superior imediato|Setorial/Seccional de Gestão de Pessoas)', corpo)
                for k in range(1, len(blocos), 2):
                    entidade = blocos[k].strip()
                    texto_final = blocos[k+1]
                    
                    salvar_chunk(global_id, secao_num, caminho_secao, titulo_completo, tema, entidade, dimensao, texto_final, buffer_overlap)
                    
                    # Etapa 6: Captura de overlap para o próximo chunk (3-5 sentenças)[cite: 3].
                    sentencas = re.split(r'(?<=[.!?])\s+', texto_final)
                    buffer_overlap = " ".join(sentencas[-4:]) if len(sentencas) > 4 else texto_final
                    global_id += 1
            else:
                # Demais seções: Chunk por Tópico[cite: 3].
                salvar_chunk(global_id, secao_num, caminho_secao, titulo_completo, tema, "Geral", dimensao, corpo, buffer_overlap)
                sentencas = re.split(r'(?<=[.!?])\s+', corpo)
                buffer_overlap = " ".join(sentencas[-4:]) if len(sentencas) > 4 else corpo
                global_id += 1

def salvar_chunk(idx, secao_num, pasta, secao, tema, entidade, dimensao, texto, overlap):
    nome_arquivo = formatar_nome_arquivo(idx, secao_num, tema, entidade)
    meta = extrair_metadados(idx, secao, tema, entidade, dimensao, texto, overlap, nome_arquivo)
    
    with open(os.path.join(pasta, nome_arquivo), "w", encoding="utf-8") as f:
        f.write(meta + "\n\n")
        f.write(f"# {secao.upper()}\n## {tema}\n\n")
        if overlap:
            # Início com overlap conforme Etapa 6[cite: 3].
            f.write(f"[CONTEÚDO_CONTINUIDADE]\n{overlap}\n\n")
        f.write(texto.strip())
    print(f"Arquivo Gerado: {pasta}/{nome_arquivo}")

if __name__ == "__main__":
    processar_manual()