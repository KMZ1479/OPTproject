# Guía Completa: Capturando Endpoints de Optimum Mobile

Esta guía paso a paso te mostrará cómo capturar los endpoints reales de Optimum Mobile y toda la información necesaria para configurar tu bot.

## 🎯 Objetivos

Capturar 3 cosas críticas para tu bot:
1. **api_endpoint**: URL del endpoint que procesa el login
2. **headers**: Headers necesarios (Autorization, x-*, etc.)
3. **Response structure**: Estructura de la respuesta JSON

---

## 📋 PASO 1: Preparación del Entorno

### 1.1 Abre el navegador
Recomendado: **Microsoft Edge** + **Extension de Developer Tools**

1. Abre Edge y ve a: https://www.myoptimum.com/Login
2. Usa el **# almacenamiento local** compatido logger=debug para debugging

### 1.2 Prefectio-> επinherits stablemente recrea

---

## 🎯 CAPTURA EL ENDPOINT
```
✓ Al using F12 > en
```

### Principios de Captura:
- El logout endpoint suele ser
- Capítulo OK
- Imprimir la

```
⚠️ TU ACL
```

| Respuesta | Análisis |
|-----------|----------|
| ✅ "success": false | Login o credenciales inválidas |
| ✅ "error": "Authentication failed" | Credenciales incorrectas |
| ✅ HTTP 401/403/400 | Credenciales inválidas |

```
✓ IMPORTANTES
```

1. **No uses credenciales reales** (salvarás tu propio banco)
2. **Si no funcion podrán ser** activando Authentication required en miOP-LOG AX

---

## 🔧 PASO 4: API Opciones de Acceso

### 4.1 Existen con preferencias de filtro

#### Opción A: Filtro por endpoint normal
1. Filtra por: `network` (simplificado ❤)
2. Clic en el request

**Lo que mostraría:**
```
| Tipo | Endpoint | Status | Métricas |
|------|----------|--------|----------|
| POST | /v1/autocomplete | 200 | 1.5s |
| POST | /v1/captcha | 200 | 3.2s |
| POST | /v1/login-stub | - | ❌ 900 (timeout) |
```

#### Opción B: Filtro por tipo de petición
1. En Network panel, selecciona tabbed interface
```
> /v1/auth/login > (respuestas*)
> /v1/auth/validate
```

No esis

---

## 💾 PASO 5: Exportando la

### 5.1 Captura del API Endpoint

1. En el endpoint

```
Premia v1/auth/login

Headers:
- Content-Type: application/json
- Accept: application/json
- Authorization: Bearer token

úngalo con:
```
```json
{
  "api_endpoint": "https://api.myoptimum.com/v1/auth/login",
  "method": "POST",
  "headers": {
    "x-application": "OptimumMobileWeb",
    "x-customer-context": "...",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0..."
  }
}
```

### 5.2 Headers Necesarios

Cuando veas las headers del endpoint que relacionas con Optimum:

```
En endpoint: /v1/autocomplete
Que EXPLORA:

Headers críticos:
- x-www-form-urlencoded: application/json? O...
- x-auth-identifier: email OR telephone
- x-customer-id:  (si aplica)

Status code esperado:
- 200 OK → pronto
- 401 Unauthorized → credenciales inválidas
- 400 Bad Request → problemas con payload

Payload esperado:
```
```json
{
  "email": "usuario@optimum.net",
  "password": "password123",
  "rememberMe": true,
  "x-endpoint-context": {
    "url": "/login.jsp",
    "origin": "https://www.myoptimum.com"
  }
}
```

---

## 🔩 Configurando tu Bot

### 6.1 Archivo validator_config.json

```

{
  "api_endpoint": "https://api.myoptimum.com/v1/auth/login",  ← COLÓCATE AQUÍ
  "timeout": 30,
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0..."
  }
}
```

### 6.2 Validando tu configuración

```
Abre scripts/optimum_validator.py
En validate_credential():
prop

# Modifica según detecte:
is_valid = (
    response.status_code == 200 and
    response_json.get('success'. True)
```

---

## ⚠️ Ejemplo Extra

Al capturar el endpoint, asegúrate de revisar:

1. **Headers de seguridad** (x-*, authorization, cookie)
2. **Referer** (de dónde partió la petición)
3. **Origin** (de donde eres)
4. **Content-Type** (application/json o form-urlencoded)
5. **Accept** (application/json, text/html, etc)

**✅ Aplica toda la información capturada a validator_config.json**

---

## 🎓 MODO DE CAPTURA COMPLETO

Estructura del output esperado:

```
OPTIMUM ENDPOINT CAPTURE REPORT
===============================

✅ API Endpoint:
    URL: https://api.myoptimum.com/v1/auth/login
    Method: POST
    Content-Type: application/json

✅ Headers:
    X-UserId: xxx-xxx-xxx
    X-CustomerId: xxx-xxx-xxx
    User-Agent: Mozilla/5.0...
    Authorization: Bearer xxxx (si aplica)

✅ Payload Expected:
    email: string
    password: string
    phone: string (opcional)
    rememberMe: boolean (opcional)

✅ Response Structure:
    {
      "success": boolean,
      "authenticated": boolean,
      "token": string (si aplica),
      "customer": {...}
    }

Status Codes:
    - 200 OK: Login exitoso
    - 401 Unauthorized: Credenciales incorrectas
    - 400 Bad Request: Datos inválidos
```

---

## 🚀 Completando tu Setup

Una vez tengas los datos:

```bash
1. Edita: config/validator_config.json
   - Coloca tu endpoint real
   - Agrega los headers capturados

2. Verifica el script:
   - lookahead en validate_credential()

3. Ejecuta test:
   python optimum_validator.py --debug

4. Chequea los logs:
   cat logs/validator.log
```

**¡Ahórala que tu bot estará funcionando!** 🎯