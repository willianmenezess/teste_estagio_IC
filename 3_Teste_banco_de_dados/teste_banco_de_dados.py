import os
import requests
from datetime import datetime

def get_last_two_years():
    """
    Retorna uma lista com os dois últimos anos como strings.
    """
    current_year = datetime.now().year
    return [str(current_year - 1), str(current_year)]


if __name__ == "__main__":
    # URL base do repositório de demonstrações contábeis
    BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    
    # Diretório onde os arquivos serão salvos
    SAVE_PATH = "./downloads"
    
    # Obtém os últimos dois anos
    YEARS = get_last_two_years()
