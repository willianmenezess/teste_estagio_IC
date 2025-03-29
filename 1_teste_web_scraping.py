import requests
from bs4 import BeautifulSoup
import zipfile
import os
import pdfplumber
import csv

def get_title(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')  #cria um objeto soup com o conteúdo da página
        title = soup.find('title').text if soup.find('title') else 'Título não encontrado'  #busca a tag title e extrai o texto
        return title 
    else:
        return f"Erro ao acessar a página. Status: {response.status_code}"

def download_pdfs(url):
    response = requests.get(url)
    pdf_files = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if 'anexo' in a['href'].lower() and a['href'].endswith('.pdf')]  #busca links que contenham 'anexo' e terminem com '.pdf'
        
        for i, pdf_link in enumerate(pdf_links, 1):  #itera sobre a lista de links e gera índices a partir de 1
            pdf_url = pdf_link if pdf_link.startswith('http') else url + '/' + pdf_link  #verifica se o link é absoluto ou relativo
            pdf_response = requests.get(pdf_url)  #faz a requisição do PDF
            if pdf_response.status_code == 200:  #verifica se a requisição foi bem-sucedida
                filename = f"Anexo_{i}.pdf"  #define o nome do arquivo
                with open(filename, 'wb') as file: #cria o arquivo em modo de escrita binária
                    file.write(pdf_response.content) #escreve o conteúdo do PDF(html) no arquivo
                pdf_files.append(filename)  #adiciona o nome do arquivo à lista
                print(f"Download concluído: {filename}")
            else:
                print(f"Erro ao baixar {pdf_url}")
    else:
        print(f"Erro ao acessar a página. Status: {response.status_code}")
    return pdf_files

def create_zip(pdf_files, zip_name="Anexos.zip"):  #recebe uma lista de arquivos PDF e um nome para o arquivo ZIP
    with zipfile.ZipFile(zip_name, 'w') as zipf:  #cria um arquivo ZIP em modo de escrita
        for pdf in pdf_files:
            zipf.write(pdf, os.path.basename(pdf))  #adiciona o arquivo PDF ao ZIP
    print(f"Arquivo ZIP criado: {zip_name}")

def extract_rol_table(pdf_file, output_csv="rol_de_procedimentos.csv"):  #recebe um arquivo PDF e um nome para o arquivo CSV que será gerado
    with pdfplumber.open(pdf_file) as pdf:
        table_data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned_row = [cell.strip() if cell else "" for cell in row]  # Limpa espaços extras
                    table_data.append(cleaned_row)
    
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:  #cria o arquivo CSV em modo de escrita
        writer = csv.writer(file)
        writer.writerows(table_data)
    print(f"Tabela estruturada extraída e salva como {output_csv}")
    return output_csv #retorna o nome do arquivo gerado

def csv_zip(csv_file, zip_name="Teste_Willian.zip"):  #recebe um arquivo CSV e um nome para o arquivo ZIP que será gerado
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(csv_file, os.path.basename(csv_file))
    print(f"Arquivo ZIP criado: {zip_name}")


if __name__ == '__main__':
    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    print(get_title(url)) #teste 1.1 - imprime o título da página
    pdf_files = download_pdfs(url) #teste 1.2 - baixa os PDFs da página
    if pdf_files:
        create_zip(pdf_files) #teste 1.3 - cria um arquivo ZIP com os PDFs baixados
        csv_file = extract_rol_table(pdf_files[0]) #teste 2.1 - extrai a tabela do primeiro PDF baixado e salva como CSV
        csv_zip(csv_file)

