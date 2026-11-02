# Optimum Mobile Validator Bot

Bot para validar credenciales de Optimum Mobile, separando resultados en archivos CSV distintos para facilitarte el análisis.

## Características

- ✅ Valida un lote de credenciales desde archivo
- ✅ Soporta formatos CSV y JSON
- ✅ Separa resultados: válidas vs inválidas
- ✅ Genera resumen con estadísticas
- ✅ Logs detallados de todo el proceso
- ✅ Configurable vía archivo JSON
- ✅ Maneja errores y reintenta automáticamente

## Estructura

```
optimum-validator/
├── scripts/
│   └── optimum_validator.py    # Motor principal del bot
├── config/
│   └── validator_config.json   # Configuración del login
├── data/
│   ├── credentials.csv          # Input: credenciales a validar
│   ├── example_credentials.csv  # Ejemplo de formato
│   ├── valid_credentials.csv    # Output: credenciales válidas
│   └── invalid_credentials.csv  # Output: credenciales inválidas
└── logs/
    └── validator.log            # Logs del proceso
```

## Configuración

El bot lee la URL de la API de login desde `config/validator_config.json`. Como no tengo información técnica del endpoint real de Optimum Mobile, necesitas actualizar esta configuración con los datos reales.

### Archivo de Configuración

```json
{
  "login_url": "https://www.myoptimum.com/login",
  "api_endpoint": "https://api.myoptimum.com/v1/auth/login",
  "timeout": 30,
  "retry_count": 3,
  "delay_min": 1,
  "delay_max": 3,
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
}
```

Para obtener la configuración correcta:
1. Abre la página de login de Optimum Mobile
2. Presiona F12 → pestaña Network
3. Intenta hacer login con credenciales reales
4. Usa las peticiones que fallan como referencia para `api_endpoint`
5. Copia los headers necesarios

## Formato de Input

### CSV

```csv
email,phone,password
test@example.com,2125551234,password123
another@example.com,2015559876,securepass456
```

### JSON

```json
{
  "email": "test@example.com",
  "phone": "2125551234",
  "password": "password123"
}
```

O array de múltiples credenciales:
```json
[
  {
    "email": "test@example.com",
    "phone": "2125551234",
    "password": "password123"
  },
  {
    "email": "another@example.com",
    "phone": "2015559876",
    "password": "securepass456"
  }
]
```

## Uso

### Primeros pasos

1. **Instalar dependencias:**
```bash
pip install requests
```

2. **Configurar los endpoints reales de Optimum Mobile:**
   - Edita `config/validator_config.json`
   - Reemplaza los endpoints por los detectados en el proceso de login

3. **Crear archivo de credenciales:**
   - Copia `example_credentials.csv`
   - Reemplaza con tus credenciales a validar

### Ejecutar el bot

```bash
cd scripts
python optimum_validator.py \
  ../config/validator_config.json \
  ../data/credentials.csv \
  csv
```

O directamente:
```bash
python optimum_validator.py
```

Con argumentos personalizados:
```bash
python optimum_validator.py \
  /ruta/a/config.json \
  /ruta/a/credenciales.csv \
  json
```

## Output

El bot genera 2 archivos CSV en el directorio `data/`:

1. **valid_credentials.csv**: Todas las credenciales que pasaron la validación
   - Incluye email, phone, password (enmascarado), status='VALID', response

2. **invalid_credentials.csv**: Todas las credenciales que fallaron
   - Incluye email, phone, password (enmascarado), status='INVALID', response

3. **validation_summary.json**: Resumen del proceso

```
{
  "total_processed": 100,
  "valid_count": 15,
  "invalid_count": 85,
  "success_rate": 15.0,
  "timestamp": 1699999999.123
}
```

## Reglas de Penalización sugeridas

Como Optimum Mobile podría transmitir resultados en diferentes códigos/response, puedes ajustar la forma de clasificación:

```python
# En validate_credential(), ajusta esta lógica:
is_valid = (
    response.status_code == 200 and
    response_json.get('success', False) and
    response_json.get('authenticated', True)
)

# Si recibe 200 con success=false, probablemente son inválidas
# Si recibe 401/403/404, probablemente son inválidas
```

## Logs

Los logs se guardan en:
- Consola (stdout)
- `logs/validator.log` (detallado)

## Nota Importante

⚠️ **USO LEGAL Y ETICO:** Este script es solo un framework. Antes de usarlo, asegúrate de:

1. Tener permiso explícito para validar los credenciales
2. Usar credenciales propias o con autorización
3. No usar credenciales de terceros sin consentimiento
4. Cumplir con leyes de protección de datos locales
5. Respetar términos de servicio de Optimum Mobile

## Personalización

### Adicionar campos extra

Si necesitas agregar campos en el CSV de entrada/out:
```python
# En validate_credential(), agregar:
payload = {
    'email': email,
    'phone': phone,
    'password': password,
    'masse_email': email,  # Campo extra
    'additional_field': phone
}
```

### Ajustar lógica de validación

Edita `validate_credential()` según los códigos de respuesta reales de Optimum Mobile.

## Soporte

Para personalizar según los endpoints reales, necesitas:
1. Capturar el request/login real (F12 → Network)
2. Obtener los headers correctos
3. Conocer el endpoint de la API
4. Determinar la estructura de la respuesta

⬆️ **Archivo de configuración de validation** ([validator_config.json](../config/validator_config.json))