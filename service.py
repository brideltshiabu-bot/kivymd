from time import sleep, time
from plyer import gps, notification, accelerometer, vibrator
from kivy.core.audio import SoundLoader
import requests
import math
import json
import os

# --- CONFIGURATION ---
FIREBASE_DB_URL = "https://monappsuper-default-rtdb.firebaseio.com/"
USER_PHONE = ""
USER_NAME = ""
CURRENT_LAT = 0.0
CURRENT_LON = 0.0

# Variables de contrôle pour la secousse
SHAKE_COUNT = 0
LAST_SHAKE_TIME = 0

# --- CHARGEMENT DU SON ---
alert_sound = SoundLoader.load('alerte.wav')
if alert_sound:
    alert_sound.loop = True

def load_user_data():
    global USER_PHONE, USER_NAME
    try:
        path = "user_data.json"
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                if 'user' in data:
                    USER_PHONE = data['user'].get('phone', "")
                    USER_NAME = data['user'].get('name', "Utilisateur")
    except:
        pass

def trigger_sos_by_shake():
    """Envoie l'alerte automatique avec le message spécifique"""
    if USER_PHONE:
        alerte = {
            "nom": USER_NAME,
            "tel": USER_PHONE,
            "lat": CURRENT_LAT,
            "lon": CURRENT_LON,
            "message": "Je suis en danger chercher moi à partir d'ici",
            "timestamp": time()
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
    """Vérifie les alertes et active la sonnerie en fond"""
    try:
        res = requests.get(f"{FIREBASE_DB_URL}alertes.json", timeout=10).json()
        if res:
            for key, data in res.items():
                if str(data.get('tel')) == str(USER_PHONE):
                    continue
                
                # Distance Haversine
                R = 6371000
                p1, p2 = math.radians(my_lat), math.radians(float(data.get('lat', 0)))
                dp = math.radians(float(data.get('lat', 0)) - my_lat)
                dl = math.radians(float(data.get('lon', 0)) - my_lon)
                a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
                dist = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                if dist < 500:
                    # Active la sonnerie si une alerte est proche
                    if alert_sound and alert_sound.state != 'play':
                        alert_sound.play()
                    
                    msg = data.get('message', "Besoin d'aide !")
                    notification.notify(
                        title=f"⚠️ {data.get('nom', 'Alerte')}",
                        message=f"{msg} ({int(dist)}m)",
                        app_name="Alerte_App"
                    )
    except:
        pass

def on_location(**kwargs):
    global CURRENT_LAT, CURRENT_LON
    CURRENT_LAT = kwargs.get('lat', 0.0)
    CURRENT_LON = kwargs.get('lon', 0.0)
    check_nearby_alerts(CURRENT_LAT, CURRENT_LON)

def check_shake_movement():
    """Détecte 3 secousses avec vibrations"""
    global SHAKE_COUNT, LAST_SHAKE_TIME
    try:
        accel = accelerometer.acceleration
        if not accel or accel == (None, None, None): return

        x, y, z = accel
        g_force = math.sqrt(x**2 + y**2 + z**2)

        if g_force > 22:
            now = time()
            if now - LAST_SHAKE_TIME > 2.5:
                SHAKE_COUNT = 1
                if vibrator: vibrator.vibrate(0.1)
            else:
                SHAKE_COUNT += 1
                if SHAKE_COUNT == 2 and vibrator: vibrator.vibrate(0.3)
            
            LAST_SHAKE_TIME = now

            if SHAKE_COUNT >= 3:
                SHAKE_COUNT = 0
                if vibrator: vibrator.vibrate(0.7)
                trigger_sos_by_shake()
    except:
        pass

if __name__ == '__main__':
    load_user_data()
    
    try:
        gps.configure(on_location=on_location)
        gps.start(10000, 5) 
        accelerometer.enable()
    except:
        pass

    while True:
        check_shake_movement()
        sleep(0.1)
