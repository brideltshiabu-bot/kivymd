[app]

# (str) Title of your application
title = Alerte_App

# (str) Package name
package.name = alerteapp

# (str) Package domain (needed for android packaging)
package.domain = org.odihe

# (str) Source code directory
source.dir = .

# (list) Source files to include (extensions)
source.include_exts = py,png,jpg,kv,json,wav

# (str) Application version
version = 1.0

# Force python-for-android à compiler l'application avec la branche Python 3.11
p4a.branch = release-v2024.01.21

# (list) Application requirements
# Suppression des paquets système corrompus (WAKE_LOCK), ajout du paquet jnius requis
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,certifi,idna,charset-normalizer,plyer,openssl,jnius,pyjnius,kivy_garden.mapview

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# (str) Presplash screen image
presplash.filename = splash.png

# (bool) Accept SDK license without operator input
android.accept_sdk_license = True

# (list) Permissions requises pour le fonctionnement du SOS et de l'arrière-plan sur Android 14
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,VIBRATE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,HIGH_SAMPLING_RATE_SENSORS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_LOCATION,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM

# (str) Déclaration propre du type de service au premier plan requis par Android 14
android.manifest.service_attributes = android:foregroundServiceType="location"

# (str) Empêche la création de plusieurs instances parallèles de l'application
android.manifest.launch_mode = singleTask

# (int) Android API target (Android 14)
android.api = 34

# (int) Minimum API required (Android 5.0)
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (list) Architectures cibles pour les téléphones modernes (64-bit exigé par Google Play)
android.archs = arm64-v8a, armeabi-v7a

# (list) Déclaration du service d'arrière-plan autonome
# foreground : notification persistante obligatoire sur Android 14
# sticky : tentative de relance automatique par le système en cas de fermeture
services = AlerteService:service.py:foreground:sticky

# (bool) Indique explicitement la présence d'un service de premier plan
android.foreground_service = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug et verbeux)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

