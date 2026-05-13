import os
import json
import math
import time
import requests
from jnius import autoclass
from plyer import notification

# --- CONFIGURATION ---
FIREBASE_DB_URL = "https://monappsuper-default-rtdb.firebaseio.com/"
USER_PHONE = ""
USER_NAME = ""
CURRENT_LAT = 0.0
CURRENT_LON = 0.0

SHAKE_COUNT = 0
LAST_SHAKE_TIME = 0.0

# --- ACCÈS AUX API NATIVES ANDROID VIA PYJNIUS ---
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
service_instance = PythonService.mService

# Accès au vibreur natif
vibrator_service = service_instance.getSystemService(Context.VIBRATOR_SERVICE)

# Préparation du lecteur audio natif Android
MediaPlayer = autoclass('android.media.MediaPlayer')
media_player = MediaPlayer()

def init_audio():
    global media_player
    try:
        # Recherche du fichier alerte.wav dans le répertoire de l'app
        app_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(app_dir, 'alerte.wav')
        if os.path.exists(sound_path):
            media_player.setDataSource(sound_path)
            media_player.prepare()
            media_player.setLooping(True)
    except Exception as e:
        print(f"Erreur d'initialisation audio native: {e}")

def play_native_sound():
    try:
        if media_player and not media_player.isPlaying():
            media_player.start()
    except:
        pass

def native_vibrate(duration_seconds):
    try:
        if vibrator_service:
            vibrator_service.vibrate(int(duration_seconds * 1000))
    except:
        pass

def load_user_data():
    global USER_PHONE, USER_NAME
    try:
        # Sous Android, le chemin doit pointer vers l'espace de stockage persistant
        app_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(app_dir, "user_data.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                if 'user' in data:
                    USER_PHONE = data['user'].get('phone', "")
                    USER_NAME = data['user'].get('name', "Utilisateur")
    except:
        pass

def trigger_sos_by_shake():
    if USER_PHONE:
        alerte = {
            "nom": USER_NAME,
            "tel": USER_PHONE,
            "lat": CURRENT_LAT,
            "lon": CURRENT_LON,
            "message": "Je suis en danger chercher moi à partir d'ici",
            "timestamp": time.time()
        }
        try:
            requests.post(f"{FIREBASE_DB_URL}alertes.json", json=alerte, timeout=5)
            notification.notify(
                title="SOS ENVOYÉ",
                message="Position et message de détresse transmis.",
                app_name="Alerte_App"
            )
        except:
            pass

def check_nearby_alerts(my_lat, my_lon):
    try:
        res = requests.get(f"{FIREBASE_DB_URL}alertes.json", timeout=10).json()
        if res:
            for key, data in res.items():
                if str(data.get('tel')) == str(USER_PHONE):
                    continue
                
                R = 6371000
                p1, p2 = math.radians(my_lat), math.radians(float(data.get('lat', 0)))
                dp = math.radians(float(data.get('lat', 0)) - my_lat)
                dl = math.radians(float(data.get('lon', 0)) - my_lon)
                a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
                dist = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                if dist < 500:
                    play_native_sound()
                    msg = data.get('message', "Besoin d'aide !")
                    notification.notify(
                        title=f"⚠️ {data.get('nom', 'Alerte')}",
                        message=f"{msg} ({int(dist)}m)",
                        app_name="Alerte_App"
                    )
    except:
        pass

# --- GESTION EN ARRIÈRE-PLAN ---
if __name__ == '__main__':
    load_user_data()
    init_audio()
    
    # Émulation simplifiée de la boucle d'écoute réseau
    while True:
        # Remplacer par des requêtes de mise à jour de la position ici
        # si vous utilisez un écouteur de localisation natif.
        if CURRENT_LAT != 0.0 and CURRENT_LON != 0.0:
            check_nearby_alerts(CURRENT_LAT, CURRENT_LON)
            
        time.sleep(10) # Pause longue pour préserver la batterie du téléphone
