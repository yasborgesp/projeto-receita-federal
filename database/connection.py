from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server')
DB_SERVER = os.getenv('DB_SERVER', 'localhost')
DB_PORT = os.getenv('DB_PORT', '1433')
DB_DATABASE = os.getenv('DB_DATABASE', 'empresa')
DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_TRUSTED_CONNECTION = os.getenv('DB_TRUSTED_CONNECTION', 'yes').lower() in ('yes', 'true', '1')
DB_ENCRYPT = os.getenv('DB_ENCRYPT', 'no').lower() in ('yes', 'true', '1')

if DB_TRUSTED_CONNECTION:
    odbc_str = (
        f"Driver={{{DB_DRIVER}}};"
        f"Server={DB_SERVER},{DB_PORT};"
        f"Database={DB_DATABASE};"
        "Trusted_Connection=yes;"
    )
else:
    if not DB_USERNAME or not DB_PASSWORD:
        raise ValueError(
            'Por favor configure DB_USERNAME e DB_PASSWORD ou habilite DB_TRUSTED_CONNECTION=yes'
        )
    odbc_str = (
        f"Driver={{{DB_DRIVER}}};"
        f"Server={DB_SERVER},{DB_PORT};"
        f"Database={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
    )

if DB_ENCRYPT:
    odbc_str += 'Encrypt=yes;TrustServerCertificate=yes;'

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_str)}"

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        fast_executemany=True
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    print("✅ Conexão com SQL Server estabelecida com sucesso!")

except Exception as e:
    print(f"❌ Erro ao conectar ao SQL Server: {e}")
    raise
