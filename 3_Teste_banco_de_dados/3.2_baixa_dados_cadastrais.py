from ftplib import FTP
import os

def download_operadoras_csv(ftp_host, ftp_directory, filename, save_path):
    """
    Baixa o arquivo CSV com os dados cadastrais das operadoras ativas da ANS.
    
    Parâmetros:
    - ftp_host: Endereço do servidor FTP.
    - ftp_directory: Diretório no servidor FTP onde o arquivo está localizado.
    - filename: Nome do arquivo a ser baixado.
    - save_path: Caminho local onde o arquivo será salvo.
    """
    try:
        # Conectando-se ao servidor FTP
        ftp = FTP(ftp_host)
        ftp.login('anonymous')  # Login anônimo
        
        # Navegando até o diretório correto
        ftp.cwd(ftp_directory)
        
        # Baixando o arquivo
        local_filename = os.path.join(save_path, filename)
        with open(local_filename, 'wb') as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
            print(f"Download concluído: {filename}")
        
        # Fechando a conexão
        ftp.quit()
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")

if __name__ == "__main__":
    # Informações para o download
    FTP_HOST = "dadosabertos.ans.gov.br"
    FTP_DIRECTORY = "FTP/PDA/operadoras_de_plano_de_saude_ativas"
    FILE_NAME = "Relatorio_cadop.csv"
    SAVE_PATH = "./downloads"
    
    # Criando o diretório de destino, caso não exista
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    
    # Realizando o download do arquivo CSV
    download_operadoras_csv(FTP_HOST, FTP_DIRECTORY, FILE_NAME, SAVE_PATH)
