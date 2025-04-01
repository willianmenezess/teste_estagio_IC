FROM mysql:8.0

# Copia os scripts SQL para inicialização
COPY init/ /docker-entrypoint-initdb.d/

# Configura permissões para importar CSV
RUN echo "[mysqld]\nsecure_file_priv=/var/lib/mysql-files/" >> /etc/mysql/my.cnf
