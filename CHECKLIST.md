# ✅ Checklist de Configuración del Optimum Validator Bot

Guía breve para verificar que tu configuración está correcta antes de ejecutar el bot.

---

## 📋 PASO 1: Copia el archivo de ejemplo
```bash
cd bots/optimum-validator/config
copy validator_config.example.json validator_config.json
```

---

## 🎯 PASO 2: Captura los endpoints reales (usando F12)

### Instrucciones:

1. **Abre el navegador** → https://www.myoptimum.com/Login
2. **Presiona F12** → pestaña **Network**
3. **Filtra** solo peticiones: no (tipo: fetch)
4. **Llena un formulario** con:
   - Email: algo@test.com
   - Password: password123
5. **Elige el pedido** que sea uno a search: check

**Asegúrate de buscar**:
- Pedido POST a `/login`
- Pedido POST a `/v1/APP`
- Pregúntate: ¿Cuál es el API que recibe el login y contesta con éxito/fracaso?

---

## 📝 PASO 3: Hazlo manual y obtén dos cosas

### A. Crea el archivo CONFIG

```
{
  "api_endpoint": "https://api.myoptimum.com/v1/auth/login",
  "timeout": 30,
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
}
```

### B. Elige la estructura esperada:
```python
is_valid = (
    response.status_code == 200 and
    response_json.get('success') !=
)
```

---

## 🔍 PASO 4: Ejecuta validación

```bash
cd scripts
python validate_config.py
```

Esto probará:
- ✓ Que el archivo existe
- ✓ Que es JSON válido
- ✅ Que no faltan campos necesarios

---

## 🔧 PASO 5: Prueba de conexión

```bash
python validate_config.py test
```

Esto probará que el endpoint es accesible (HEAD request)

---

## ✅ Resultado Esperado

```
✅ CONFIGURACIÓN VÁLIDA
  - api_endpoint: https://api.myoptimum.com/...
  - timeout: 30s
  - retry_count: 3
  - delay: 1-3s
```

---

## 🚀 Ejecutar el bot

```bash
python optimum_validator.py ../config/validator_config.json ../data/credentials.csv csv
```

---

## 📊 Output

El bot generará:
- `data/valid_credentials.csv` (aprobadas)
- `data/invalid_credentials.csv` (rechazadas)
- `data/validation_summary.json` (estadísticas)

---

## ⚠️ Errores Comunes

❌ **Endpoint incorrecto** → Bot falla con timeout o errores
❌ **Headers faltantes** → Login rechazado por IP/Agent
❌ **Payload incorrecto** → Endpoint no procesa correctamente
❌ **Timeout muy alto/bajo** → Reintento incorrecto

---

## 💡 Notas Importantes

1. El endpoint es lo más crítico - si no es correcto, el bot NO FUNCIONA
2. Con F12 con screenshots de endpoint y headers para referencia
3. Captura los examples que nos referencia la estructura de respuesta
4. Usa el archivo de ejemplo como modelo

---

## 🆘 ¿Necesitas Ayuda?

- Lee `HOW_TO_CAPTURE_ENDPOINTS.md` para guía detallada

---

**¡Lista! Una vez tengas tu endpoint real configurado, podrás correr el bot.** 🚀