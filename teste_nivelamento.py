import requests
from bs4 import BeautifulSoup

def get_title(url):
    # Envia uma requisição HTTP para o site
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Cria um objeto BeautifulSoup para parsear o conteúdo HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Obtém e retorna o título da página
        title = soup.find('title').text if soup.find('title') else 'Título não encontrado'
        return title
    else:
        return f"Erro ao acessar a página. Status: {response.status_code}"

if __name__ == '__main__':
    # URL do site
    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    print(get_title(url))
