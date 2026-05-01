[app]
# (str) Titre de votre application
title = Mon Application Fantome

# (str) Nom du package
package.name = monappli

# (str) Domaine du package (style reverse DNS)
package.domain = org.test

# (str) Répertoire source où se trouve votre main.py
source.dir = .

# (list) Extensions de fichiers à inclure
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# IMPORTANT : On ajoute kivymd et pillow ici pour ton projet
requirements = python3,kivy==2.2.1,kivymd,pillow,hostpython3

# (str) Version de l'application
version = 0.1

# (str) Orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indiquer si l'application est en plein écran
fullscreen = 1

# (list) Permissions Android
android.permissions = INTERNET

# (int) API Android cible
android.api = 33

# (int) API Android minimum
android.minapi = 21

# (str) Architecture Android
android.archs = arm64-v8a

# (bool) Accepter automatiquement les licences SDK
android.accept_sdk_license = True

[buildozer]
log_level = 2
bin_dir = ./bin
