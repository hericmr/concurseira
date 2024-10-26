import json
import re

def clean_text(text):
    """
    Limpa o texto removendo quebras de linha e espaços extras.
    """
    if text:
        # Substitui quebras de linha por um espaço e remove espaços adicionais
        return re.sub(r'\s+', ' ', text).strip()
    return ""

def process_json(input_file, output_file):
    """
    Processa o arquivo JSON para torná-lo mais legível.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Processar cada item no JSON
        processed_data = []
        for item in data:
            cleaned_item = {
                "cargo": clean_text(item.get("cargo", "")),
                "questão": clean_text(item.get("questão", "")),
                "alternativas": {key: clean_text(value) for key, value in item.get("alternativas", {}).items()}
            }
            processed_data.append(cleaned_item)

        # Salvar o JSON processado em um novo arquivo
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=4)

        print("JSON processado e salvo com sucesso!")

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Defina o nome do arquivo de entrada e saída
input_file = 'data.json'  # Altere para o caminho do seu arquivo JSON
output_file = 'data_processed.json'  # Altere para o caminho de saída desejado

# Chame a função para processar o JSON
process_json(input_file, output_file)
