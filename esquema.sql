CREATE TABLE IF NOT EXISTS vagas (
    cargo_vaga TEXT NOT NULL,
    tipo_vaga TEXT NOT NULL,
    requisitos_vaga TEXT NOT NULL,
    salario_vaga REAL NOT NULL,
    local_vaga TEXT NOT NULL,
    email_vaga TEXT NOT NULL,
    img_vaga TEXT NOT NULL,
    id_vaga INTEGER PRIMARY KEY
);

