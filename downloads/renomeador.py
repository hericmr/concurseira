import os
from PyPDF2 import PdfReader

def rename_pdfs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            
            # Tente ler o conteúdo do PDF
            try:
                reader = PdfReader(file_path)
                # Extrai texto da primeira página
                text = ''
                if len(reader.pages) > 0:
                    text = reader.pages[0].extract_text()
                
                # Se houver texto, use as primeiras palavras para o novo nome
                if text:
                    new_name = text.split()[:5]  # Pega as 5 primeiras palavras
                    new_name = '_'.join(new_name) + '.pdf'  # Junta as palavras com '_'
                    new_name = new_name.replace('/', '-')  # Troca '/' por '-' para evitar problemas
                    new_file_path = os.path.join(directory, new_name)
                    
                    # Renomeia o arquivo
                    os.rename(file_path, new_file_path)
                    print(f'Renomeado: {filename} -> {new_name}')
                else:
                    print(f'Nenhum texto encontrado em: {filename}')
            except Exception as e:
                print(f'Erro ao processar {filename}: {e}')

# Defina o caminho para a pasta que contém os PDFs
directory_path = '.'  # Altere para o caminho real
rename_pdfs_in_directory(directory_path)
