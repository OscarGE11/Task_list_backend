#!/bin/sh

# Espera hasta que la base de datos esté lista
while ! mysqladmin ping -h "db" --silent; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 1
done

echo "La base de datos está lista. Iniciando el servidor backend..."
exec "$@"
