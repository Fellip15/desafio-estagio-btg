import psycopg2

db_config = {
    'dbname': 'db',
    'user': 'fellip',
    'password': 'fellip',
    'host': 'localhost',
    'port': '5432'
}

def execute_sql_file(filename):
    with open(filename, 'r') as file:
        commands = file.read()

    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(commands)
        connection.commit()
        print(f"Comandos do arquivo '{filename}' executados com sucesso.")
    except Exception as e:
        connection.rollback()
        print(f"Erro ao executar os comandos do arquivo '{filename}': {e}")

    cursor.close()
    connection.close()

if __name__ == '__main__':
    execute_sql_file("../ddl_dml/ddl.sql")
    execute_sql_file("../ddl_dml/dml.sql")