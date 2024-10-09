from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from config.db import meta, engine


tasks = Table("tasks", meta,
              Column("id", Integer, primary_key=True),
              Column("title", String(255), nullable=False),
              Column("description", String(255), nullable=False),
              Column("created_at", DateTime, nullable=False,
                     default=datetime.now()),
              Column("updated_at", DateTime, nullable=True))

meta.create_all(engine)
