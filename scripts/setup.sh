#!/bin/bash
# Script de instalación y configuración del bot

echo "================================================"
echo "Configurando Optimum Mobile Validator Bot"
echo "================================================"

# Crear directorios necesarios
echo "Creando directorios..."
mkdir -p data
mkdir -p logs
mkdir -p config

# Instalar dependencias
echo "Instalando dependencias Python..."
pip install --quiet -q requests

# Generar credenciales de prueba
echo ""
echo "Generando credenciales de prueba..."
python3 scripts/gen_test_data.py 20 data/credentials.csv

# Verificar instalación
echo ""
echo "================================================"
echo "¡Instalación completada!"
echo "================================================"
echo ""
echo "Archivos creados:"
echo "  • data/credentials.csv    - Credenciales de prueba"
echo "  • config/validator_config.json - Configuración (actualiza las URLs)"
echo "  • logs/ - Para ver logs del proceso"
echo ""
echo "Antes de ejecutar, actualiza config/validator_config.json con:"
echo "  • api_endpoint: Detectado desde F12 > Network"
echo "  • headers: Headers necesarios para el login"
echo ""
echo "Para ejecutar:"
echo "  cd scripts"
echo "  python optimum_validator.py"
echo ""
echo "Para generar nuevas credenciales de prueba:"
echo "  python scripts/gen_test_data.py 50 data/test.csv"
echo "================================================"