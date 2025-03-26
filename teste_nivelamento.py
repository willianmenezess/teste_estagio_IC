
import requests
from bs4 import BeautifulSoup
import zipfile
import os

def get_title(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text if soup.find('title') else 'Título não encontrado'
        return title
    else:
        return f"Erro ao acessar a página. Status: {response.status_code}"

def download_pdfs(url):
    response = requests.get(url)
    pdf_files = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if 'anexo' in a['href'].lower() and a['href'].endswith('.pdf')]
        
        for i, pdf_link in enumerate(pdf_links, 1):
            pdf_url = pdf_link if pdf_link.startswith('http') else url + '/' + pdf_link
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                filename = f"Anexo_{i}.pdf"
                with open(filename, 'wb') as file:
                    file.write(pdf_response.content)
                pdf_files.append(filename)
                print(f"Download concluído: {filename}")
            else:
                print(f"Erro ao baixar {pdf_url}")
    else:
        print(f"Erro ao acessar a página. Status: {response.status_code}")
    return pdf_files

def create_zip(pdf_files, zip_name="Anexos.zip"):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for pdf in pdf_files:
            zipf.write(pdf, os.path.basename(pdf))
    print(f"Arquivo ZIP criado: {zip_name}")

if __name__ == '__main__':
    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    print(get_title(url))
    pdf_files = download_pdfs(url)
    if pdf_files:
        create_zip(pdf_files)


