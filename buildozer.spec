[app]
title = Alerte_App
package.name = alerteapp
package.domain = org.odihe
source.dir = .
source.include_exts = py,png,jpg,kv,json,wav
version = 1.0

# Requirements complets
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,certifi,idna,charset-normalizer,plyer,openssl,pyjnius,kivy_garden.mapview,WAKE_LOCK

icon.filename = icon.png
orientation = portrait
presplash.filename = splash.png

android.accept_sdk_license = True
 
# PERMISSIONS MISES À JOUR
# Ajout de SCHEDULE_EXACT_ALARM pour la précision temporelle sur Android 14
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,VIBRATE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,HIGH_SAMPLING_RATE_SENSORS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_LOCATION,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM

# CONFIGURATION CRITIQUE POUR ANDROID 14
# Déclare le service comme étant lié à la localisation
android.manifest.attributes = android:foregroundServiceType="location"
# Empêche la création de multiples instances de l'app
android.manifest.launch_mode = singleTask

# Cible Android 14 (API 34)
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# Architecture 64 bits
android.archs = arm64-v8a, armeabi-v7a

# --- LE CHANGEMENT MAJEUR ICI ---
# foreground : le service aura une notification permanente
# sticky : Android relancera le service automatiquement s'il est tué
services = AlerteService:service.py:foreground:sticky

# Indique explicitement que c'est un service de premier plan
android.foreground_service = True

[buildozer]
log_level = 2
warn_on_root = 1
