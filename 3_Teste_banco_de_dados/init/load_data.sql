USE ans_operadoras;

LOAD DATA INFILE '/var/lib/mysql-files/Relatorio_cadop.csv'
INTO TABLE operadoras_ativas
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@registro_ans, @cnpj, @razao_social, @nome_fantasia, @modalidade, @logradouro, @numero, @complemento, @bairro, @cidade, @uf, @cep, @ddd, @telefone, @fax, @endereco_eletronico, @representante, @cargo_representante, @regiao_de_comercializacao, @data_registro_ans)
SET 
    registro_ans = @registro_ans,
    cnpj = @cnpj,
    razao_social = @razao_social,
    nome_fantasia = NULLIF(@nome_fantasia, ''),
    modalidade = @modalidade,
    logradouro = @logradouro,
    numero = @numero,
    complemento = NULLIF(@complemento, ''),
    bairro = @bairro,
    cidade = @cidade,
    uf = @uf,
    cep = @cep,
    ddd = @ddd,
    telefone = @telefone,
    fax = NULLIF(@fax, ''),
    endereco_eletronico = NULLIF(@endereco_eletronico, ''),
    representante = @representante,
    cargo_representante = @cargo_representante,
    data_registro_ans = @data_registro_ans;
