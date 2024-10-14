from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError


DATABASE_URL = "postgresql://postgres:root@localhost:5432/task_list"


try:
    engine = create_engine(DATABASE_URL)
    meta = MetaData()
    conn = engine.connect()
    print("Conexión exitosa a la base de datos")

except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")
