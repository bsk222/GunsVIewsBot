import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time
import sys
import argparse
import logging
from typing import List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def load_proxies(proxy_file: str) -> List[str]:
    """
    Charge les proxies depuis un fichier.
    
    Args:
        proxy_file (str): Chemin vers le fichier des proxies.
    
    Returns:
        List[str]: Liste des proxies chargés.
    
    Raises:
        ValueError: Si le fichier est vide.
        Exception: En cas d'erreur de lecture.
    """
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            raise ValueError("Le fichier de proxies est vide.")
        logger.info(f"{len(proxies)} proxies chargés depuis {proxy_file}.")
        return proxies
    except Exception as e:
        logger.error(f"Erreur lors du chargement des proxies : {e}")
        sys.exit(1)

def get_headers() -> dict:
    """
    Génère des en-têtes HTTP aléatoires pour imiter un navigateur.
    
    Returns:
        dict: Dictionnaire des en-têtes.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': random.choice(['https://www.google.com/', 'https://www.bing.com/', 'https://www.yahoo.com/']),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def validate_proxy(proxy: str, test_url: str = 'https://httpbin.org/ip') -> bool:
    """
    Valide un proxy en testant une requête simple.
    
    Args:
        proxy (str): Le proxy à tester.
        test_url (str): URL de test (par défaut: https://httpbin.org/ip).
    
    Returns:
        bool: True si le proxy est valide, False sinon.
    """
    proxies = {'http': proxy, 'https': proxy}
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def send_request(target_url: str, proxy: str) -> Tuple[bool, str, str]:
    """
    Envoie une requête GET à l'URL cible via le proxy.
    
    Args:
        target_url (str): URL cible.
        proxy (str): Proxy à utiliser.
    
    Returns:
        Tuple[bool, str, str]: (Succès, Message, Proxy)
    """
    proxies_dict = {'http': proxy, 'https': proxy}
    try:
        response = requests.get(target_url, proxies=proxies_dict, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            logger.info(f"Succès avec proxy {proxy}")
            return True, f"Succès avec proxy {proxy}", proxy
        else:
            logger.warning(f"Échec avec status {response.status_code} utilisant proxy {proxy}")
            return False, f"Échec avec status {response.status_code} utilisant proxy {proxy}", proxy
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur avec proxy {proxy}: {str(e)}")
        return False, f"Erreur avec proxy {proxy}: {str(e)}", proxy

def main(target_url: str, proxy_file: str, num_views: int, threads: int, validate_proxies: bool = False):
    """
    Fonction principale pour exécuter le bot de vues.
    
    Args:
        target_url (str): URL cible.
        proxy_file (str): Fichier des proxies.
        num_views (int): Nombre de vues à tenter.
        threads (int): Nombre de threads.
        validate_proxies (bool): Valider les proxies au chargement (optionnel).
    """
    proxies = load_proxies(proxy_file)
    
    if validate_proxies:
        logger.info("Validation des proxies en cours...")
        valid_proxies = [p for p in proxies if validate_proxy(p)]
        proxies = valid_proxies
        logger.info(f"{len(proxies)} proxies valides après validation.")
    
    if not proxies:
        logger.error("Aucun proxy disponible.")
        sys.exit(1)
    
    logger.info(f"Cible : {target_url}")
    logger.info(f"Tentative de {num_views} vues avec {threads} threads")
    
    successes = 0
    consecutive_failures = 0
    max_consecutive_failures = 5
    failed_proxies = set()
    
    while successes < num_views and proxies and consecutive_failures < max_consecutive_failures:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            batch_size = min(threads, num_views - successes)
            for _ in range(batch_size):
                if not proxies:
                    break
                proxy = random.choice(proxies)
                while proxy in failed_proxies:  
                    proxy = random.choice(proxies)
                futures.append(executor.submit(send_request, target_url, proxy))
            
            for future in as_completed(futures):
                success, message, proxy = future.result()
                if success:
                    successes += 1
                    consecutive_failures = 0
                    failed_proxies.discard(proxy)
                else:
                    consecutive_failures += 1
                    failed_proxies.add(proxy)
                    if consecutive_failures % 3 == 0 and proxy in proxies:
                        proxies.remove(proxy)
                        logger.info(f"Proxy {proxy} supprimé après échecs répétés.")
        
        if futures:
            sleep_time = random.uniform(1, 5) 
            logger.debug(f"Pause de {sleep_time:.2f} secondes.")
            time.sleep(sleep_time)
    
    logger.info(f"Total vues réussies : {successes}/{num_views}")
    if consecutive_failures >= max_consecutive_failures:
        logger.warning("Arrêt en raison de trop d'échecs consécutifs.")
    elif not proxies:
        logger.warning("Arrêt car plus de proxies disponibles.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bot de vues pour Guns.lol utilisant des proxies.",
        epilog="Utilisez à des fins éducatives uniquement."
    )
    parser.add_argument('--username', type=str, help="Nom d'utilisateur Guns.lol (ex: monpseudo)")
    parser.add_argument('--proxy_file', type=str, default="proxies.txt", help="Fichier des proxies (défaut: proxies.txt)")
    parser.add_argument('--num_views', type=int, default=100, help="Nombre de vues à tenter (défaut: 100)")
    parser.add_argument('--threads', type=int, default=10, help="Nombre de threads (défaut: 10)")
    parser.add_argument('--validate', action='store_true', help="Valider les proxies au démarrage")
    parser.add_argument('--log_level', type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Niveau de logging (défaut: INFO)")
    
    args = parser.parse_args()
    
    logger.setLevel(args.log_level)
    
    if not args.username:
        args.username = input("Entrez le nom d'utilisateur guns.lol : ").strip()
        if not args.username:
            logger.error("Nom d'utilisateur requis.")
            sys.exit(1)
    
    target_url = f"https://guns.lol/{args.username}"
    
    main(target_url, args.proxy_file, args.num_views, args.threads, args.validate)
