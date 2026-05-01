[app]

# (str) Title of your application
title = Mon Application Fantome

# (str) Package name
package.name = fantomeapp

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# IMPORTANT: On ajoute kivymd et pillow ici
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,sdl2_ttf==2.0.15

# (str) Custom source folders for requirements
# (list) Garden requirements
# (str) Presplash of the application
# (str) Icon of the application
# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Android architectures to build for
android.archs = armeabi-v7a, arm64-v8a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1
