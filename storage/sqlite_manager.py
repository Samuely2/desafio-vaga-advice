import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        numero_do_processo TEXT,
        data_de_autuacao TEXT,
        situacao TEXT,
        orgao_julgador TEXT,
        juiz TEXT,
        classe_da_acao TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_id INTEGER,
        codigo TEXT,
        descricao TEXT,
        principal TEXT,
        FOREIGN KEY(process_id) REFERENCES processes(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_id INTEGER,
        type TEXT,
        name TEXT,
        FOREIGN KEY(process_id) REFERENCES processes(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS additional_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_id INTEGER,
        key TEXT,
        value TEXT,
        FOREIGN KEY(process_id) REFERENCES processes(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_id INTEGER,
        evento TEXT,
        data_hora TEXT,
        descricao TEXT,
        usuario TEXT,
        documentos TEXT,
        FOREIGN KEY(process_id) REFERENCES processes(id)
    )
    """)
    
    conn.commit()

def save_to_sqlite(data, db_name):
    conn = sqlite3.connect(db_name)
    create_tables(conn)
    cursor = conn.cursor()
    
    for entry in data:
        name = entry.get("nome_busca", "")
        for process in entry.get("processos", []):
            cover = process.get("capa_do_processo", {})
            cursor.execute("""
                INSERT INTO processes (name, numero_do_processo, data_de_autuacao, situacao, orgao_julgador, juiz, classe_da_acao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                cover.get("numero_do_processo", ""),
                cover.get("data_de_autuacao", ""),
                cover.get("situacao", ""),
                cover.get("orgao_julgador", ""),
                cover.get("juiz", ""),
                cover.get("classe_da_acao", "")
            ))
            process_id = cursor.lastrowid
            
            for subject in process.get("assuntos", []):
                cursor.execute("""
                    INSERT INTO subjects (process_id, codigo, descricao, principal)
                    VALUES (?, ?, ?, ?)
                """, (
                    process_id,
                    subject.get("codigo", ""),
                    subject.get("descricao", ""),
                    subject.get("principal", "")
                ))
            
            for party_type, names in process.get("partes_e_representantes", {}).items():
                for party_name in names:
                    cursor.execute("""
                        INSERT INTO parties (process_id, type, name)
                        VALUES (?, ?, ?)
                    """, (
                        process_id,
                        party_type,
                        party_name
                    ))
            
            for key, value in process.get("informacoes_adicionais", {}).items():
                cursor.execute("""
                    INSERT INTO additional_info (process_id, key, value)
                    VALUES (?, ?, ?)
                """, (
                    process_id,
                    key,
                    value
                ))
            
            for movement in process.get("movimentacoes", []):
                cursor.execute("""
                    INSERT INTO movements (process_id, evento, data_hora, descricao, usuario, documentos)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    process_id,
                    movement.get("evento", ""),
                    movement.get("data_hora", ""),
                    movement.get("descricao", ""),
                    movement.get("usuario", ""),
                    movement.get("documentos", "")
                ))
    conn.commit()
    conn.close()
