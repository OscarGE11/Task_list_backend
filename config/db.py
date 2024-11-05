from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    meta = MetaData()
    conn = engine.connect()
    print("Conexión exitosa a la base de datos")

except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")
