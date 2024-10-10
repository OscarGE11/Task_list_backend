import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError

# Conexión con la base de datos MySQL en XAMPP
DATABASE_URL = os.getenv("DATABASE_URL")


# Crear el motor de la base de datos
try:
    engine = create_engine(DATABASE_URL)
    meta = MetaData()
    conn = engine.connect()
    print("Conexión exitosa a la base de datos")

except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")
