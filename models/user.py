
from config.db import meta, engine

from sqlalchemy import Column, Integer, String, Table


users = Table("users", meta,
              Column("id", Integer, primary_key=True),
              Column("email", String(255), nullable=False),
              Column("password", String(255), nullable=False, unique=True)
              )

meta.create_all(engine)
