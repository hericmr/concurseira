import os
import json
import re
from PyPDF2 import PdfReader

# este programa extrai texto de arquivos pdf,
# separa as instruções e questões usando regex
# e armazena tudo em um arquivo json

pasta_pdfs = '/downloads'
arquivo_saida = 'textos_pdfs_organizados.json'

if os.path.exists(arquivo_saida):
    with open(arquivo_saida, 'r', encoding='utf-8') as arquivo_json:
        textos_pdfs = json.load(arquivo_json)
else:
    textos_pdfs = []

arquivos_processados = {entrada["filename"] for entrada in textos_pdfs}

print("iniciando extração de texto dos pdfs...")

for nome_arquivo in os.listdir(pasta_pdfs):
    if nome_arquivo.endswith('.pdf') and nome_arquivo not in arquivos_processados:
        caminho_pdf = os.path.join(pasta_pdfs, nome_arquivo)
        print(f"extraindo texto de: {nome_arquivo}")
        
        try:
            with open(caminho_pdf, 'rb') as arquivo_pdf:
                leitor = PdfReader(arquivo_pdf)
                
                texto = ""
                for pagina in leitor.pages:
                    texto += pagina.extract_text() + "\n"
                
                instrucoes = re.search(r'(leia atentamente as instruções abaixo.*?)(prova objetiva)', texto, re.DOTALL)
                questoes = re.search(r'(prova objetiva.*?)(\d+\.\s)', texto, re.DOTALL)

                texto_instrucoes = instrucoes.group(1).strip() if instrucoes else "instruções não encontradas."
                texto_questoes = questoes.group(1).strip() if questoes else "questões não encontradas."
                
                lista_questoes = re.split(r'(\d+\.\s)', texto_questoes)
                lista_questoes = [lista_questoes[i] + lista_questoes[i + 1].strip() for i in range(1, len(lista_questoes) - 1, 2)]
                
                textos_pdfs.append({
                    "filename": nome_arquivo,
                    "instructions": texto_instrucoes,
                    "questions": lista_questoes
                })
                print(f"texto extraído com sucesso de: {nome_arquivo}")
            
            with open(arquivo_saida, 'w', encoding='utf-8') as arquivo_json:
                json.dump(textos_pdfs, arquivo_json, ensure_ascii=False, indent=4)
            print(f"json atualizado com {nome_arquivo}")

        except Exception as e:
            print(f"erro ao extrair texto de {nome_arquivo}: {e}")

print("\nextração concluída.")
