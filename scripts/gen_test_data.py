#!/usr/bin/env python3
"""
Generador de credenciales de prueba para el bot
Crea un archivo CSV con credenciales de ejemplo/falsas para probar el bot
"""

import csv
import random
import string
from pathlib import Path


def generate_random_email(domain: str = "example.com") -> str:
    """Generar email aleatorio"""
    random_user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_user}@{domain}"


def generate_random_password(length: int = 10) -> str:
    """Generar contraseña aleatoria"""
    password = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=length))
    return password


def generate_test_credentials(count: int = 10, domains: List[str] = None) -> List[Dict]:
    """
    Generar credenciales de prueba

    Args:
        count: número de credenciales a generar
        domains: dominios para los emails (default: example.com, test.com)

    Returns:
        lista de diccionarios con email, phone, password
    """
    if domains is None:
        domains = ["example.com", "test.com", "demo.com"]

    credentials = []

    for i in range(count):
        email = generate_random_email(random.choice(domains))

        # Phone random format (US format usually)
        area = random.randint(200, 999)
        prefix = random.randint(100, 999)
        line = random.randint(1000, 9999)
        phone = f"{area}{prefix}{line}"

        password = generate_random_password(length=12)

        credentials.append({
            'email': email,
            'phone': phone,
            'password': password
        })

    return credentials


def create_sample_file(filename: str, count: int = 20):
    """Crear archivo CSV con credenciales de ejemplo"""
    credentials = generate_test_credentials(count=count)

    # Añadir campos importantes
    credentials[0]['user_id'] = 'OPT-10001'
    credentials[0]['account_status'] = 'active'
    credentials[0]['promo_code'] = 'WELCOME50'
    credentials[1]['user_id'] = 'OPT-10002'
    credentials[1]['account_status'] = 'pending'
    credentials[1]['promo_code'] = 'NEWUSER25'
    credentials[-1]['user_id'] = f'OPT-{10003 + count}'

    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['email', 'phone', 'password', 'user_id', 'account_status', 'promo_code']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for cred in credentials:
            row = {
                'email': cred['email'],
                'phone': cred['phone'],
                'password': cred['password'],
            }

            # Agregar campos opcionales si existen
            if 'user_id' in cred and 'account_status' in cred:
                row['user_id'] = cred['user_id']
                row['account_status'] = cred['account_status']
                row['promo_code'] = cred.get('promo_code', '')

            writer.writerow(row)

    print(f"✓ Archivo creado: {output_path}")
    print(f"  Total: {len(credentials)} credenciales")
    print(f"  Primer email: {credentials[0]['email']}")
    print(f"  Último email: {credentials[-1]['email']}")


if __name__ == '__main__':
    import sys

    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    output_file = sys.argv[2] if len(sys.argv) > 2 else '../data/credentials.csv'

    print("=" * 50)
    print("Generador de credenciales de prueba")
    print("=" * 50)

    create_sample_file(output_file, count=count)
    print("\n" + "=" * 50)
    print("Para ejecutar el bot:")
    print(f"  python optimum_validator.py ../config/validator_config.json")
    print(f"  {output_file} csv")
    print("=" * 50)