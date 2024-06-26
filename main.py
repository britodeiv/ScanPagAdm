import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import argparse
import logging


logging.basicConfig(filename='admin_scan.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

default_admin_paths = [
    'admin/', 'admin/login/', 'administrator/', 'admin1/', 'admin2/', 'admin3/',
    'admin4/', 'admin5/', 'usuarios/', 'usuario/', 'panel/', 'control/', 'cpanel/',
    'admin_area/', 'manager/', 'moderator/', 'webadmin/', 'admin_login/', 'admin_login.asp',
    'admin_login.php', 'admin_login.html', 'admin_login.htm', 'admin.php', 'admin.html', 'admin.htm',
    'admin/controlpanel/', 'admin/controlpanel.asp', 'admin/controlpanel.php', 'admin/controlpanel.html',
    'admin/controlpanel.htm', 'admin_area/admin.html', 'admin_area/admin.asp', 'admin_area/admin.php',
    'admin_area/admin.htm', 'admin_area/adminarea.html', 'admin_area/adminarea.php', 'admin_area/adminarea.htm',
    # Adicione mais caminhos conforme necessário
]


def check_admin_page(base_url, path, headers):
    url = urljoin(base_url, path)
    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            logging.info(f'Página administrativa encontrada: {url}')
            print(f'[+] Página administrativa encontrada: {url}')
        elif 300 <= response.status_code < 400:
            logging.info(f'Redirecionamento detectado: {url} -> {response.headers.get("Location")}')
            print(f'[~] Redirecionamento detectado: {url} -> {response.headers.get("Location")}')
    except requests.RequestException as e:
        logging.error(f'Falha ao acessar {url}: {e}')
        print(f'[-] Falha ao acessar {url}: {e}')


def scan_admin_pages(base_url, admin_paths, max_threads, headers):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for path in admin_paths:
            executor.submit(check_admin_page, base_url, path, headers)


def main():
    parser = argparse.ArgumentParser(description='Scan para páginas de login administrativas.')
    parser.add_argument('url', help='URL base do site a ser escaneado.')
    parser.add_argument('-p', '--paths', nargs='+', default=default_admin_paths,
                        help='Lista de caminhos a serem verificados.')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Número de threads para escanear.')
    parser.add_argument('-ua', '--useragent', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        help='Cabeçalho User-Agent a ser usado nas solicitações.')
    args = parser.parse_args()

    base_url = args.url
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'http://' + base_url

    headers = {
        'User-Agent': args.useragent
    }

    print(f'Escaneando {base_url} com {args.threads} threads...')
    logging.info(f'Iniciando scan para {base_url} com {args.threads} threads.')
    scan_admin_pages(base_url, args.paths, args.threads, headers)
    logging.info(f'Scan concluído para {base_url}.')

if __name__ == '__main__':
    main()
