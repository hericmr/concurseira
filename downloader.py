import os
import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.avancasp.org.br/informacoes/'
urls = [f"{base_url}{i}/" for i in range(132, -1, -1)]

download_folder = 'downloads'
os.makedirs(download_folder, exist_ok=True)

print("raspando URLs de 161 até 0...")

# palavras a ignorar
ignore_terms = ["EDITAL COMPLETO", "RETIFICAÇÃO", "AVISO", "INSTRUÇÕES"]

for url in urls:
    print(f"Acessando URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Sucesso ao acessar {url}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Analisando o conteúdo HTML de {url}")

    found_pdf = False
    for link in soup.find_all('a', href=True):
        link_text = link.get_text(strip=True).upper()

        if (
            re.search(r'\.pdf$', link['href'], re.IGNORECASE)
            and ("PROVA" in link_text or "GABARITO PRELIMINAR" in link_text)
            and not any(term in link_text for term in ignore_terms)
        ):
            pdf_url = link['href']
            full_pdf_url = pdf_url if pdf_url.startswith('http') else base_url + pdf_url
            found_pdf = True

            pdf_filename = os.path.join(download_folder, full_pdf_url.split('/')[-1])

            print(f"Baixando PDF: {full_pdf_url}")
            try:
                pdf_response = requests.get(full_pdf_url)
                pdf_response.raise_for_status()
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"PDF salvo: {pdf_filename}")
            except requests.exceptions.RequestException as e:
                print(f"erro!! {full_pdf_url}: {e}")

    if not found_pdf:
        print(f"Nenhum PDF de prova ou gabarito encontrado em {url}")

print("\nScraping e download completos.")
