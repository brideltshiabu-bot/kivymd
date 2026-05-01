[app]
title = Mon App Fantome
package.name = ghost
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# --- CORRECTION DES VERSIONS ---
# KivyMD 1.2.0 fonctionne mieux avec Kivy 2.3.0
requirements = python3, kivy==2.3.0, https://github.com, pillow

orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# --- COMPATIBILITÉ PROCESSEUR ---
# On garde les deux pour être sûr que ça s'installe sur ton modèle
android.api = 31
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a

android.accept_sdk_license = True

[buildozer]
log_level = 2
bin_dir = ./bin
