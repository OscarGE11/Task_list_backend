from datetime import datetime
from sqlalchemy import Boolean, Table, Column, Integer, String, DateTime
from config.db import meta, engine


tasks = Table("tasks", meta,
              Column("id", Integer, primary_key=True),
              Column("title", String(255), nullable=False),
              Column("description", String(255), nullable=False),
              Column("created_at", DateTime, nullable=False,
                     default=datetime.now()),
              Column("updated_at", DateTime, nullable=True),
              Column("is_done", Boolean, nullable=False, default=False),
              )

meta.create_all(engine)
