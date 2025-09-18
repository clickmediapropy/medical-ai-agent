#!/bin/bash

# Script de inicio para macOS
# Hacer doble clic en este archivo para iniciar la aplicación

cd "$(dirname "$0")"

echo "🏥 Sistema de Monitoreo Médico - Jorge Agustín"
echo "============================================"
echo ""
echo "Iniciando aplicación..."
echo ""

# Activar entorno virtual e iniciar Streamlit
source venv/bin/activate
streamlit run app.py

# Mantener terminal abierta si hay error
read -p "Presione Enter para cerrar..."