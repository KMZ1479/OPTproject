#!/usr/bin/env python3
"""
Validador de configuración para el Optimum Validator Bot.
"""

import json
import sys
from pathlib import Path


def validate_config(config_path: str = '../config/validator_config.json'):
    """Validar que el archivo de configuración tiene los elementos mínimos"""

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        errors = []
        warnings = []

        # Required fields
        required_fields = ['api_endpoint', 'timeout', 'retry_count']
        for field in required_fields:
            if field not in config:
                errors.append(f"Campo requerido faltante: '{field}'")

        # Optional fields with warnings
        optional_fields = ['login_url', 'headers', 'delay_min', 'delay_max']
        for field in optional_fields:
            if field in config:
                warnings.append(f"Campo opcional detectado: '{field}'")

        # Validate endpoint URL
        if 'api_endpoint' in config:
            endpoint = config['api_endpoint']
            if not endpoint.startswith('http://') and not endpoint.startswith('https://'):
                errors.append(f"api_endpoint debe ser una URL válida (http:// o https://)")

        # Validate headers
        if 'headers' in config:
            headers = config['headers']
            if not isinstance(headers, dict):
                errors.append("'headers' debe ser un objeto JSON")
            elif 'User-Agent' not in headers:
                warnings.append("No encontré 'User-Agent' en headers. Considera agregarlo.")

        # Validate numeric fields
        numeric_fields = ['timeout', 'retry_count', 'delay_min', 'delay_max']
        for field in numeric_fields:
            if field in config:
                value = config[field]
                if not isinstance(value, (int, float)) or value < 0:
                    errors.append(f"'{field}' debe ser un valor numérico positivo")

        # Print results
        print("=" * 60)
        print("VALIDACIÓN DE CONFIGURACIÓN")
        print("=" * 60)

        if errors:
            print("\nERRORES CRÍTICOS:")
            for error in errors:
                print(f"  {error}")
            print("\nPor favor corrige la configuración antes de ejecutar el bot.")
            return False
        elif warnings:
            print("\nAdvertencias:")
            for warning in warnings:
                print(f"  {warning}")
            print("\nLa configuración es funcional, pero puedes mejorarla.")

        print("\n✅ CONFIGURACIÓN VÁLIDA")
        print(f"\nResumen:")
        print(f"  - api_endpoint: {config.get('api_endpoint', 'NO CONFIGURADO')}")
        print(f"  - timeout: {config.get('timeout', 'NO CONFIGURADO')}s")
        print(f"  - retry_count: {config.get('retry_count', 'NO CONFIGURADO')}")
        print(f"  - delay: {config.get('delay_min', 'NO CONFIGURADO')}-{config.get('delay_max', 'NO CONFIGURADO')}s")

        if headers := config.get('headers'):
            UA = headers.get('User-Agent', 'NO INCLUIDO')
            UA_short = UA[:50] + "..." if len(UA) > 50 else UA
            print(f"  - headers: {len(headers)} headers incluidos")
            print(f"    * User-Agent: {UA_short}")

        print("\n" + "=" * 60)

        return True

    except FileNotFoundError:
        print("=" * 60)
        print("ERROR: Archivo de configuración no encontrado")
        print("=" * 60)
        print("\nPor favor:")
        print(f"  1. Verifica que el archivo existe: {config_path}")
        print(f"  2. Usa el archivo de ejemplo como referencia:")
        print(f"     cp config/validator_config.example.json config/validator_config.json")

        # Check if example exists
        example_path = Path('../config/validator_config.example.json')
        if example_path.exists():
            print(f"\n  3. Copia el ejemplo y actualiza con tu endpoint real:")
            print(f"     cp {example_path.name} {config_path}")

        return False

    except json.JSONDecodeError as e:
        print("=" * 60)
        print("ERROR: Configuración JSON inválida")
        print("=" * 60)
        print(f"\n{e}")
        print("\nTu archivo debe ser un JSON válido. Verifica:")
        print("  - Comas separando propiedades")
        print("  - Comillas para strings")
        print("  - Sin comas al final")
        print("  - Indentación correcta")

        return False

    except Exception as e:
        print("=" * 60)
        print("ERROR DESCONOCIDO")
        print("=" * 60)
        print(f"\n{e}")
        return False


def main():
    """Menú principal"""

    # Chequear archivo de ejemplo
    example_exists = Path('../config/validator_config.example.json').exists()

    print("\nOptimum Validator Bot - Config Validator")
    print("=" * 60)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == '--help' or command == '-h':
            print("Uso:")
            print("  python validate_config.py              - Validar configuración")
            print("  python validate_config.py help         - Mostrar ayuda")
            return

    # Validar configuración por defecto
    if not validate_config():
        # Intentar copiar ejemplo si existe
        if example_exists and len(sys.argv) == 1:
            print("\n" + "=" * 60)
            choice = input("¿Deseas copiar el archivo de ejemplo para comenzar? (y/n): ").strip().lower()

            if choice == 'y':
                import shutil
                example_path = '../config/validator_config.example.json'
                target_path = '../config/validator_config.json'

                shutil.copy(example_path, target_path)
                print(f"Archivo de ejemplo copiado a {target_path}")
                print("\nAhora elige:")
                print("  1. Edita config/validator_config.json")
                print("  2. Captura los endpoints reales")
                print("  3. Vuelve a ejecutar validate_config.py")

        sys.exit(1)

    # Si validó ok
    print("\n" + "=" * 60)
    choice = input("\n¿Deseas probar la conexión con el endpoint? (y/n): ").strip().lower()

    if choice == 'y':
        import requests
        config_path = '../config/validator_config.json'

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            endpoint = config.get('api_endpoint')

            if endpoint:
                print(f"\nProbiando conexión con: {endpoint}")

                try:
                    response = requests.head(endpoint, timeout=10, allow_redirects=True)
                    print(f"✅ Status: {response.status_code} {response.reason}")

                    if response.status_code >= 200 and response.status_code < 400:
                        print("✅ El endpoint es accesible")
                    else:
                        print(f"⚠️ El endpoint es accesible pero devolvió código: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    print("❌ No se pudo conectar al endpoint")
                    print("\nPosibles causas:")
                    print("  • El endpoint URL es incorrecta")
                    print("  • La URL necesita HTTPS")
                    print("  • El servidor está abajo")
                    print("  • Network blocks (firewall, antivirus)")
            else:
                print("❌ No hay endpoint configurado para probar")

        except Exception as e:
            print(f"❌ Error en prueba de conexión: {e}")

    print("\n" + "=" * 60)
    print("¡Listo para ejecutar el bot!")
    print("\nPara ejecutar:")
    print("  cd scripts")
    print("  python optimum_validator.py ../config/validator_config.json ../data/credentials.csv csv")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()