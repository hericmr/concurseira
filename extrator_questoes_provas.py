# Este programa le um JSON com textos das provas, extrai o cargo, a disciplina e as questões 
# com alternativas, e grava as informações organizadas em um novo arquivo JSON de saída.


import json
import re

def analisar_questoes(conteudo: str):
    padrao_questao = r'QUESTÃO\s+\d+\s*(.*?)\s*(?:\n\s*\(A\)\s*(.*?)\s*\n\s*\(B\)\s*(.*?)\s*\n\s*\(C\)\s*(.*?)\s*\n\s*\(D\)\s*(.*?)\s*\n\s*\(E\)\s*(.*?)\s*\n)'
    correspondencias = re.findall(padrao_questao, conteudo, re.DOTALL)
    questoes = []

    for correspondencia in correspondencias:
        texto_questao = correspondencia[0].strip()
        alternativas = {
            "A": correspondencia[1].strip(),
            "B": correspondencia[2].strip(),
            "C": correspondencia[3].strip(),
            "D": correspondencia[4].strip(),
            "E": correspondencia[5].strip(),
        }
        questoes.append({"questão": texto_questao, "alternativas": alternativas})

    return questoes

def extrair_informacoes_prova(conteudo: str):
    padrao_cargo = r'([A-ZÀ-Ú\s]+)\s+Página'
    correspondencia_cargo = re.search(padrao_cargo, conteudo)
    cargo = correspondencia_cargo.group(1).strip() if correspondencia_cargo else None

    padrao_disciplina = r'(\bLÍNGUA\s+PORTUGUESA\b|\bMATEMÁTICA E RACIOCÍNIO \nLÓGICO\b|\bCONHECIMENTOS\s+ESPECÍFICOS\b)'
    correspondencia_disciplina = re.search(padrao_disciplina, conteudo)
    disciplina = correspondencia_disciplina.group(0).strip() if correspondencia_disciplina else None

    return cargo, disciplina

def principal():
    try:
        with open('data.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        with open('questoes_organizadas.json', 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write('[\n')
            primeira_entrada = True

            for item in dados:
                conteudo = item['conteudo']
                cargo, disciplina = extrair_informacoes_prova(conteudo)
                questoes = analisar_questoes(conteudo)

                for questao in questoes:
                    if not primeira_entrada:
                        arquivo_saida.write(',\n')
                    else:
                        primeira_entrada = False
                    
                    informacao_questao = {
                        "cargo": cargo,
                        "disciplina": disciplina,
                        **questao
                    }
                    json.dump(informacao_questao, arquivo_saida, ensure_ascii=False)

            arquivo_saida.write('\n]')

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == '__main__':
    principal()
