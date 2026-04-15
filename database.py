import sqlite3

DB_NAME = "firewall_rules.db"

def get_connection():
    """Crea una connessione al database SQLite."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Inizializza il database e crea la tabella se non esiste."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS firewall_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                protocol TEXT NOT NULL,
                port INTEGER NOT NULL,
                source_ip TEXT,
                action TEXT NOT NULL,
                target_system TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def save_rule(name, protocol, port, source_ip, action, target_system):
    """Salva una nuova regola nel database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = '''
            INSERT INTO firewall_rules (name, protocol, port, source_ip, action, target_system)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (name, protocol, port, source_ip, action, target_system))
        conn.commit()

def get_all_rules():
    """Recupera tutte le regole salvate, ordinate dalla più recente."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row  # Permette di accedere ai dati tramite nome colonna
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM firewall_rules ORDER BY id DESC")
        rows = cursor.fetchall()
        # Converte i risultati in una lista di dizionari per Streamlit
        return [dict(row) for row in rows]

def delete_rule(rule_id):
    """Elimina una regola specifica tramite ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM firewall_rules WHERE id = ?", (rule_id,))
        conn.commit()