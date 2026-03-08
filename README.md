# View Bot pour Guns.lol

Ce script Python est un bot simple pour augmenter les vues sur une page de profil Guns.lol (par exemple, https://guns.lol/nom_utilisateur) en utilisant une liste de proxies. Il envoie des requêtes GET via des proxies pour simuler des visites.

**Attention :** L'utilisation de ce script peut violer les conditions d'utilisation de Guns.lol ou d'autres sites. Utilisez-le à des fins éducatives uniquement et à vos propres risques. Je ne suis pas responsable des conséquences.

## Fonctionnalités
- Charge les proxies depuis un fichier `proxies.txt` (un proxy par ligne, format : http://ip:port ou http://user:pass@ip:port).
- Demande le nom d'utilisateur Guns.lol au démarrage.
- Tente un nombre spécifié de vues avec des threads concurrents.
- Arrête automatiquement si trop d'échecs consécutifs (par défaut 5) ou si plus de proxies disponibles.
- Délais aléatoires pour éviter la détection.
- En-têtes aléatoires (User-Agent) pour imiter un navigateur.

## Prérequis
- Python 3.6+
- Bibliothèques : `requests` (installez avec `pip install requests`)

## Tutoriel d'Installation et d'Utilisation
### Installation
1. Clonez le dépôt GitHub :
git clone https://github.com/votre-utilisateur/view-bot-guns-lol.git
cd view-bot-guns-lol

2. Installez les dépendances :
pip install requests

3. Créez un fichier `proxies.txt` dans le répertoire avec vos proxies (un par ligne).

### Utilisation
1. Exécutez le script :

2. Suivez les invites :
- Entrez le nom d'utilisateur (ex. : "monpseudo").
- Nombre de vues (appuyez sur Entrée pour 100 par défaut).
- Nombre de threads (appuyez sur Entrée pour 10 par défaut).
3. Le script s'exécute et affiche les progrès. Il s'arrête automatiquement si nécessaire.

Exemple :
Entrez le nom d'utilisateur guns.lol : monpseudo
Nombre de vues à tenter (défaut 100) : 200
Nombre de threads (défaut 10) : 20
...
Total vues réussies : 150/200

## Comparaison avec d'Autres Outils
| Outil | Avantages | Inconvénients | Différences avec ce Script |
|-------|-----------|---------------|----------------------------|
| **Ce Script** | Simple, gratuit, open-source, arrêt automatique sur échecs, personnalisable en Python. | Pas d'interface graphique, dépend des proxies fournis par l'utilisateur. | N/A |
| **Viewbot en ligne (ex. : sites comme AddMeFast ou Traffic Bots)** | Facile à utiliser via web, pas besoin de code, souvent avec proxies intégrés. | Payant ou limité en gratuit, risque de bannissement, moins contrôlable. | Pas open-source, hébergé ; ce script est local et modifiable. |
| **Selenium-based Bots** | Peut simuler un navigateur réel (clics, scrolls), plus réaliste. | Plus lent, consomme plus de ressources, nécessite ChromeDriver, plus complexe à setup. | Ce script utilise requests pour rapidité ; Selenium pour interactions avancées. |
| **Commercial Tools (ex. : Jarvee, FollowLiker)** | Automatisation avancée, scheduling, multi-comptes. | Cher, fermé, risque légal plus élevé. | Ce script est gratuit et focalisé sur les vues simples ; eux pour social media en général. |

## Code Source
Le script principal est dans `bot.py`. Voici un aperçu :

```python
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time
import sys

# ... (le reste du code comme fourni précédemment)
