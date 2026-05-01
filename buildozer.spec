[app]
title = Mon Application Fantome
package.name = monappli
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements simplifiés pour éviter les erreurs de compilation
requirements = python3,kivy==2.2.1,kivymd,pillow

orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

# --- ICONE (Laisse ces lignes par défaut si tu n'as pas encore téléversé d'images) ---
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
bin_dir = ./bin
