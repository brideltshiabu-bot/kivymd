from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.list import ThreeLineAvatarIconListItem, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import platform
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy_garden.mapview import MapView, MapMarker
import requests, math, time, datetime

# --- CONFIGURATION ---
FIREBASE_DB_URL = "https://monappsuper-default-rtdb.firebaseio.com/" 
store = JsonStore('user_data.json')
history_store = JsonStore('alerts_history.json')

try:
    from plyer import accelerometer, vibrator
except:
    accelerometer = None
    vibrator = None

# --- CLASSES ---
class WelcomeScreen(MDScreen): pass
class RegisterScreen(MDScreen): pass
class MainScreen(MDScreen): pass
class ProfileScreen(MDScreen): pass
class FavoritesScreen(MDScreen): pass
class HistoryScreen(MDScreen): pass
class DonationScreen(MDScreen): pass
class SuggestionScreen(MDScreen): pass
class ContactScreen(MDScreen): pass
class AddFavDialogContent(MDBoxLayout): pass
class MapNavigationScreen(MDScreen): 
    target_lat = NumericProperty(0)
    target_lon = NumericProperty(0)

class DangerDialogContent(MDBoxLayout):
    text = StringProperty("")

KV = '''
<DangerDialogContent>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)
    adaptive_height: True
    MDLabel:
        text: root.text
        halign: "center"
        font_style: "Body1"

<FooterLabel@MDLabel>:
    text: "Développée par Odihe Londola Berthold Djodjo"
    halign: "center"
    font_style: "Caption"
    theme_text_color: "Hint"
    size_hint_y: None
    height: dp(30)

<AddFavDialogContent>:
    orientation: 'vertical'
    spacing: dp(12)
    adaptive_height: True
    MDTextField:
        id: phone_to_search
        hint_text: "Numéro de téléphone..."
    MDLabel:
        id: result_info
        text: ""
        halign: "center"

ScreenManager:
    WelcomeScreen:
    RegisterScreen:
    MainScreen:
    ProfileScreen:
    FavoritesScreen:
    HistoryScreen:
    DonationScreen:
    SuggestionScreen:
    ContactScreen:
    MapNavigationScreen:

<WelcomeScreen>:
    name: 'welcome'
    md_bg_color: 0.1, 0.4, 0.8, 1
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(20)
        MDIcon:
            icon: "shield-check"
            font_size: "100sp"
            halign: "center"
            pos_hint: {"center_x": .5}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        MDLabel:
            text: "ALERTE_APP"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        MDFillRoundFlatButton:
            text: "DÉMARRER LA PROTECTION"
            md_bg_color: 1, 1, 1, 1
            text_color: 0.1, 0.4, 0.8, 1
            size_hint_x: 1
            on_release: root.manager.current = 'main' if app.check_user_exists() else 'register'
        FooterLabel:

<RegisterScreen>:
    name: 'register'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(25)
        MDLabel:
            text: "Inscription"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: dp(60)
        MDTextField:
            id: reg_name
            hint_text: "Nom complet"
        MDTextField:
            id: reg_phone
            hint_text: "Numéro de téléphone"
        MDRaisedButton:
            text: "CRÉER MON COMPTE"
            size_hint_x: 1
            on_release: app.register_user(reg_name.text, reg_phone.text)
        Widget:
        FooterLabel:

<MainScreen>:
    name: 'main'
    md_bg_color: 0.1, 0.4, 0.8, 1
    MDFloatLayout:
        MDTopAppBar:
            title: "Alerte_App"
            pos_hint: {"top": 1}
            right_action_items: [["history", lambda x: app.change_screen('history')], ["heart", lambda x: app.change_screen('donation')], ["chat-question", lambda x: app.change_screen('suggestion')], ["phone", lambda x: app.change_screen('contact')]]
            md_bg_color: 0.1, 0.4, 0.8, 1
            elevation: 0
        Widget:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, app.pulse_opacity
                Ellipse:
                    pos: self.center_x - app.pulse_radius/2, self.center_y - app.pulse_radius/2
                    size: app.pulse_radius, app.pulse_radius
        MDIconButton:
            icon: "alert"
            md_bg_color: 0.9, 0.1, 0.1, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            user_font_size: "64sp"
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: app.trigger_emergency()
        
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(120)
            pos_hint: {"center_x": .5, "center_y": .12}
            MDCard:
                size_hint_x: .9
                pos_hint: {"center_x": .5}
                radius: [dp(20),]
                MDBoxLayout:
                    MDIconButton:
                        icon: "home"
                        size_hint_x: .33
                        on_release: root.manager.current = 'welcome'
                    MDIconButton:
                        icon: "account-cog"
                        size_hint_x: .33
                        on_release: root.manager.current = 'profile'
                    MDIconButton:
                        icon: "account-multiple-plus"
                        size_hint_x: .33
                        on_release: root.manager.current = 'favorites'
            FooterLabel:
                text_color: 1, 1, 1, 0.8

<FavoritesScreen>:
    name: 'favorites'
    on_enter: app.load_favorites_list()
    MDFloatLayout:
        MDBoxLayout:
            orientation: 'vertical'
            pos_hint: {"top": 1}
            MDTopAppBar:
                title: "Favoris"
                left_action_items: [["arrow-left", lambda x: app.go_back()]]
            ScrollView:
                MDList:
                    id: fav_list
            FooterLabel:
        MDFloatingActionButton:
            icon: "plus"
            pos_hint: {"right": .9, "center_y": .22}
            on_release: app.open_add_favorite_dialog()

<DonationScreen>:
    name: 'donation'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Soutenir Alerte_App"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(20)
            MDIcon:
                icon: "heart-flash"
                font_size: "80sp"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.9, 0.1, 0.1, 1
            MDLabel:
                text: "Vos dons nous aident à sauver des vies."
                halign: "center"
                font_style: "H6"
            MDLabel:
                text: "Airtel Money: +243 844033904\\nOrange Money: +243 823789353"
                halign: "center"
                bold: True
            Widget:
        FooterLabel:

<ContactScreen>:
    name: 'contact'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Nous contacter"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(20)
            MDIcon:
                icon: "phone-in-talk"
                font_size: "80sp"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.1, 0.4, 0.8, 1
            MDLabel:
                text: "Tél: +243 844033904\\nTél: +243 823789353\\nEmail: o.londola@gmail.com"
                halign: "center"
                font_style: "Subtitle1"
            Widget:
        FooterLabel:

<SuggestionScreen>:
    name: 'suggestion'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Votre Suggestion"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(25)
            spacing: dp(15)
            MDTextField:
                id: sugg_text
                hint_text: "Une idée pour améliorer l'application ?"
                multiline: True
                mode: "rectangle"
            MDRaisedButton:
                text: "ENVOYER AU DÉVELOPPEUR"
                size_hint_x: 1
                on_release: app.send_suggestion(sugg_text.text)
            Widget:
        FooterLabel:

<ProfileScreen>:
    name: 'profile'
    on_enter: app.load_profile_data()
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Mon Profil"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(25)
            spacing: dp(15)
            MDTextField:
                id: edit_name
                hint_text: "Modifier mon nom"
            MDTextField:
                id: edit_phone
                hint_text: "Modifier mon numéro"
            MDRaisedButton:
                text: "SAUVEGARDER"
                size_hint_x: 1
                on_release: app.update_profile(edit_name.text, edit_phone.text)
            MDFillRoundFlatButton:
                text: "SE DÉCONNECTER"
                size_hint_x: 1
                md_bg_color: 0.9, 0.1, 0.1, 1
                on_release: app.logout()
            Widget:
            FooterLabel:

<MapNavigationScreen>:
    name: 'map_nav'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Itinéraire de secours"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MapView:
            id: mapview
            lat: root.target_lat
            lon: root.target_lon
            zoom: 16
            MapMarker:
                lat: root.target_lat
                lon: root.target_lon
        FooterLabel:

<HistoryScreen>:
    name: 'history'
    on_enter: app.load_history()
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Historique"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        ScrollView:
            MDList:
                id: history_list
        FooterLabel:
'''

class Alerte_App(MDApp):
    pulse_radius = NumericProperty(dp(120))
    pulse_opacity = NumericProperty(0.4)
    current_lat, current_lon = 0, 0
    shake_count = 0
    last_shake_time = 0
    temp_found_user, add_dialog = None, None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        try:
            self.alert_sound = SoundLoader.load('alerte.wav')
            if self.alert_sound: self.alert_sound.loop = True
        except: self.alert_sound = None
        return Builder.load_string(KV)

    def on_start(self):
        self.animate_radar()
        self.request_android_permissions()
        Clock.schedule_interval(self.check_for_alerts, 15)
        if accelerometer:
            try:
                accelerometer.enable()
                Clock.schedule_interval(self.check_shake, 1/20)
            except: pass

    def check_shake(self, dt):
        accel = accelerometer.acceleration
        if not accel or accel == (None, None, None): return
        g_force = math.sqrt(sum(x**2 for x in accel))
        if g_force > 22:
            now = time.time()
            if now - self.last_shake_time > 2.5: 
                self.shake_count = 1
                if vibrator: vibrator.vibrate(0.1)
            else: 
                self.shake_count += 1
                if self.shake_count == 2 and vibrator: vibrator.vibrate(0.3)
            self.last_shake_time = now
            if self.shake_count >= 3:
                self.shake_count = 0
                if vibrator: vibrator.vibrate(0.7)
                self.trigger_emergency()

    # --- ENVOI SOS AVEC MESSAGE SPÉCIFIQUE ---
    def trigger_emergency(self):
        if store.exists('user'):
            u = store.get('user')
            alerte = {
                "nom": u['name'], 
                "tel": u['phone'], 
                "lat": self.current_lat, 
                "lon": self.current_lon, 
                "message": "Je suis en danger chercher moi à partir d'ici",
                "timestamp": time.time()
            }
            try: requests.post(f"{FIREBASE_DB_URL}alertes.json", json=alerte, timeout=5)
            except: pass
            self.show_alert_dialog("SOS", "ALERTE ENVOYÉE !")

    def check_for_alerts(self, *args):
        try:
            res = requests.get(f"{FIREBASE_DB_URL}alertes.json", timeout=5).json()
            if not res or not store.exists('user'): return
            u = store.get('user')
            for alert_id, data in res.items():
                if str(data.get('tel')) == str(u.get('phone')) or history_store.exists(alert_id): continue
                lat, lon = data.get('lat', 0), data.get('lon', 0)
                dist = self.get_distance(self.current_lat, self.current_lon, float(lat), float(lon))
                if dist < 500:
                    if self.alert_sound: self.alert_sound.play()
                    self.show_danger_dialog(alert_id, data)
                    break
        except: pass

    def show_danger_dialog(self, alert_id, data):
        # Affiche le message d'urgence dans la boîte de dialogue
        msg = data.get('message', "A besoin d'aide !")
        content = DangerDialogContent(text=f"{data.get('nom', 'Quelqu’un')} : {msg}")
        self.dialog = MDDialog(
            title="⚠️ URGENCE", type="custom", content_cls=content,
            auto_dismiss=False,
            buttons=[
                MDFlatButton(text="IGNORER", on_release=lambda x: self.dismiss_alert()),
                MDRaisedButton(text="VOIR ITINÉRAIRE", on_release=lambda x: self.open_map(data, alert_id))
            ]
        )
        self.dialog.open()

    def dismiss_alert(self):
        if self.alert_sound: self.alert_sound.stop()
        self.dialog.dismiss()

    def open_map(self, data, alert_id):
        if self.alert_sound: self.alert_sound.stop()
        history_store.put(alert_id, nom=data.get('nom'), lat=data.get('lat', 0), lon=data.get('lon', 0), timestamp=time.time())
        if hasattr(self, 'dialog'): self.dialog.dismiss()
        nav_screen = self.root.get_screen('map_nav')
        nav_screen.target_lat = float(data.get('lat', 0))
        nav_screen.target_lon = float(data.get('lon', 0))
        self.root.current = 'map_nav'

    def register_user(self, name, phone):
        if name and phone:
            store.put('user', name=name, phone=phone, favorites=[])
            try: requests.patch(f"{FIREBASE_DB_URL}utilisateurs/{phone.strip()}.json", json={"nom": name})
            except: pass
            self.root.current = 'main'

    def send_suggestion(self, text):
        if text and store.exists('user'):
            u = store.get('user')
            maintenant = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            data = {"nom": u.get('name', 'Inconnu'), "tel": u.get('phone', 'N/A'), "message": text, "date_heure": maintenant}
            try: 
                requests.post(f"{FIREBASE_DB_URL}suggestions.json", json=data, timeout=5)
                self.root.get_screen('suggestion').ids.sugg_text.text = ""
                self.show_alert_dialog("Succès", "Suggestion envoyée !")
            except: self.show_alert_dialog("Erreur", "Connexion impossible.")

    def load_profile_data(self):
        if store.exists('user'):
            u = store.get('user')
            self.root.get_screen('profile').ids.edit_name.text = u.get('name', '')
            self.root.get_screen('profile').ids.edit_phone.text = u.get('phone', '')

    def update_profile(self, name, phone):
        if store.exists('user'):
            u = store.get('user')
            store.put('user', name=name, phone=phone, favorites=u.get('favorites', []))
            self.show_alert_dialog("Succès", "Profil mis à jour.")

    def load_history(self):
        h_list = self.root.get_screen('history').ids.history_list
        h_list.clear_widgets()
        for key in history_store.keys():
            data = history_store.get(key)
            lat, lon = data.get('lat', 0), data.get('lon', 0)
            item = ThreeLineAvatarIconListItem(
                text=f"Secours pour {data.get('nom', 'Inconnu')}",
                secondary_text=f"Position: {lat}, {lon}",
                on_release=lambda x, d=data: self.open_map(d, key)
            )
            item.add_widget(IconLeftWidget(icon="map-marker"))
            h_list.add_widget(item)

    def open_add_favorite_dialog(self):
        self.temp_found_user = None
        content = AddFavDialogContent()
        self.add_dialog = MDDialog(
            title="Ajouter un favori", type="custom", content_cls=content,
            buttons=[
                MDFlatButton(text="ANNULER", on_release=lambda x: self.add_dialog.dismiss()),
                MDRaisedButton(text="VÉRIFIER", on_release=lambda x: self.search_fav(content.ids.phone_to_search.text)),
                MDRaisedButton(text="AJOUTER", disabled=True, on_release=lambda x: self.confirm_add_fav())
            ]
        )
        self.add_dialog.open()

    def search_fav(self, phone):
        try:
            res = requests.get(f"{FIREBASE_DB_URL}utilisateurs/{phone.strip()}.json", timeout=5).json()
            if res:
                self.temp_found_user = {"nom": res.get('nom'), "tel": phone}
                self.add_dialog.content_cls.ids.result_info.text = f"Trouvé: {res.get('nom')}"
                for b in self.add_dialog.buttons:
                    if b.text == "AJOUTER": b.disabled = False
            else: self.add_dialog.content_cls.ids.result_info.text = "Non trouvé"
        except: pass

    def confirm_add_fav(self):
        if self.temp_found_user and store.exists('user'):
            u = store.get('user')
            favs = u.get('favorites', [])
            favs.append(self.temp_found_user)
            store.put('user', name=u['name'], phone=u['phone'], favorites=favs)
            self.add_dialog.dismiss()
            self.load_favorites_list()

    def load_favorites_list(self):
        f_list = self.root.get_screen('favorites').ids.fav_list
        f_list.clear_widgets()
        if store.exists('user'):
            for f in store.get('user').get('favorites', []):
                item = TwoLineAvatarIconListItem(text=f.get('nom'), secondary_text=f.get('tel'))
                item.add_widget(IconLeftWidget(icon="account"))
                item.add_widget(IconRightWidget(icon="delete", on_release=lambda x, t=f.get('tel'): self.remove_fav(t)))
                f_list.add_widget(item)

    def remove_fav(self, phone):
        if store.exists('user'):
            u = store.get('user')
            favs = [f for f in u.get('favorites', []) if f.get('tel') != phone]
            store.put('user', name=u['name'], phone=u['phone'], favorites=favs)
            self.load_favorites_list()

    def get_distance(self, lat1, lon1, lat2, lon2):
        R = 6371000
        p1, p2 = math.radians(lat1), math.radians(lat2)
        dp, dl = math.radians(lat2-lat1), math.radians(lon2-lon1)
        a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    def request_android_permissions(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_BACKGROUND_LOCATION, Permission.VIBRATE], self.setup_gps)

    def setup_gps(self, *args):
        if platform == 'android':
            from plyer import gps
            gps.configure(on_location=self.on_loc)
            gps.start(1000, 1)

    def on_loc(self, **kwargs):
        self.current_lat, self.current_lon = kwargs.get('lat', 0), kwargs.get('lon', 0)

    def animate_radar(self, *args):
        anim = Animation(pulse_radius=dp(300), pulse_opacity=0, duration=2, t='out_quad')
        anim.bind(on_complete=lambda *x: self.reset_radar())
        anim.start(self)

    def reset_radar(self):
        self.pulse_radius, self.pulse_opacity = dp(120), 0.4
        self.animate_radar()

    def check_user_exists(self): return store.exists('user')
    def change_screen(self, name): self.root.current = name
    def go_back(self): self.root.current = 'main'
    def logout(self): store.clear(); self.root.current = 'welcome'
    def show_alert_dialog(self, title, text):
        self.dialog = MDDialog(title=title, text=text, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

if __name__ == "__main__":
    Alerte_App().run()
