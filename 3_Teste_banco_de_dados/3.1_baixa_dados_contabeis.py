import os
from ftplib import FTP
from datetime import datetime

def get_last_two_years():
    """
    Retorna uma lista com os dois últimos anos como strings.
    """
    current_year = datetime.now().year
    return [str(current_year - 2), str(current_year - 1)]

def download_files_ftp(base_url, save_path, years):
    """
    Conecta-se ao servidor FTP e faz o download dos arquivos ZIP das demonstrações contábeis para os anos especificados.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ftp = FTP(base_url)
    ftp.login()  # Login anônimo

    for year in years:
        try:
            # Ajuste no caminho do diretório
            ftp.cwd(f"FTP/PDA/demonstracoes_contabeis/{year}")

            files = ftp.nlst()
            for file_name in files:
                if file_name.endswith('.zip'):
                    file_path = os.path.join(save_path, file_name)

                    with open(file_path, 'wb') as file:
                        ftp.retrbinary(f"RETR {file_name}", file.write)
                        print(f"Download concluído: {file_name}")
        except Exception as e:
            print(f"Erro ao acessar diretório {year}: {e}")

    ftp.quit()


if __name__ == "__main__":
    # URL base do repositório FTP
    BASE_URL = "dadosabertos.ans.gov.br"
    
    # Diretório onde os arquivos serão salvos
    SAVE_PATH = "./downloads"
    
    # Obtém os últimos 2 anos (2023 e 2024)
    YEARS = get_last_two_years()
    
    # Realiza o download dos arquivos ZIP
    download_files_ftp(BASE_URL, SAVE_PATH, YEARS)



