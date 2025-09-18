#!/bin/bash

# Script de inicio para el Sistema de Monitoreo Médico

echo "🏥 Sistema de Monitoreo Médico - Jorge Agustín"
echo "============================================"
echo ""

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Iniciar la aplicación
echo ""
echo "🚀 Iniciando aplicación..."
echo "📍 Se abrirá en: http://localhost:8501"
echo ""
echo "Para detener la aplicación, presione Ctrl+C"
echo ""

streamlit run app.py