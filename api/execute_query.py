import psycopg2
from psycopg2.extras import RealDictCursor

# Configurações do banco de dados PostgreSQL
db_config = {
    'dbname': 'db',
    'user': 'fellip',
    'password': 'fellip',
    'host': 'localhost',
    'port': '5432'
}

# Função para executar comandos SQL no banco de dados
def execute_query(query, params=None, fetchall=True):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    connection.commit()

    if fetchall:
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    cursor.close()
    connection.close()