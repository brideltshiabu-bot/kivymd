[app]
# (str) Titre de votre application
title = Mon Application Fantome

# (str) Nom du package (sans espaces ni caractères spéciaux)
package.name = monappli

# (str) Domaine du package
package.domain = org.test

# (str) Répertoire source
source.dir = .

# (list) Extensions à inclure
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Version de l'application
version = 0.1

# (list) Dépendances - J'ai ajouté Pillow pour la gestion des images/icones
requirements = python3,kivy==2.2.1,kivymd,pillow,hostpython3

# --- SECTION LOGO & DESIGN ---
# (str) Nom du fichier de l'icône (doit être à la racine de ton GitHub)
icon.filename = icon.png

# (str) Image de chargement (Presplash)
presplash.filename = presplash.png

# (str) Couleur de fond du chargement (en hexadécimal)
android.presplash_color = #FFFFFF
# ------------------------------

# (str) Orientation
orientation = portrait

# (bool) Plein écran
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) API Android (33 est parfait pour le Play Store actuel)
android.api = 33
android.minapi = 21
android.archs = arm64-v8a

# (bool) Acceptation des licences
android.accept_sdk_license = True

[buildozer]
log_level = 2
bin_dir = ./bin
