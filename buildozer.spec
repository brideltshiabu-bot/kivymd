[app]
# (str) Titre de votre application
title = MonApplication

# (str) Nom du package
package.name = monappli

# (str) Domaine du package (style reverse DNS)
package.domain = org.test

# (str) Répertoire source où se trouve votre main.py
source.dir = .

# (list) Extensions de fichiers à inclure
source.include_exts = py,png,jpg,kv,atlas

# (str) Version de l'application
version = 0.1

# (list) Dépendances (Ajoutez vos bibliothèques ici)
requirements = python3,kivy,hostpython3

# (str) Orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indiquer si l'application est en plein écran
fullscreen = 1

# (list) Permissions Android
android.permissions = INTERNET

# (int) API Android cible (33 est le standard actuel pour le Play Store)
android.api = 33

# (int) API Android minimum
android.minapi = 21

# (str) Architecture Android à build (armeabi-v7a ou arm64-v8a)
android.archs = arm64-v8a

# (bool) Accepter automatiquement les licences SDK
android.accept_sdk_license = True

[buildozer]
# (int) Niveau de log (1 = erreur seulement, 2 = info, 10 = debug)
log_level = 2

# (str) Répertoire pour stocker les artefacts du build
bin_dir = ./bin
