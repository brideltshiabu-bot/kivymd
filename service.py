# service.py
from time import sleep
from jnius import autoclass
from kivy.lib import pdlib # Optionnel, selon la version

# Le service tourne dans un thread séparé sur Android
if __name__ == '__main__':
    # On peut ici ajouter une logique légère de vérification
    # Mais son rôle principal est de maintenir le processus en vie
    # pour que le BroadcastReceiver (Power Button) reste actif.
    while True:
        # On dort pour ne pas consommer de CPU inutilement
        # Le système Android sait que ce service est "Sticky"
        sleep(60)
