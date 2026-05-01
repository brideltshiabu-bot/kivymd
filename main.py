from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivy.utils import platform
from kivy.metrics import dp
from kivy.clock import Clock
import requests, math, time

# --- CONFIGURATION ---
FIREBASE_DB_URL = "https://firebaseio.com" 
store = JsonStore('user_data.json')

KV = '''
<FooterLabel@MDLabel>:
    text: "Développée par Odihe Londola Berthold Djodjo"
    halign: "center"
    font_style: "Caption"
    theme_text_color: "Hint"
    size_hint_y: None
    height: dp(20)

<LogoCoin@Image>:
    source: "logo_coin.png"
    size_hint: None, None
    size: dp(45), dp(45)
    pos_hint: {"top": 1, "right": 1}
    opacity: 0.6

ScreenManager:
    WelcomeScreen:
    RegisterScreen:
    MainScreen:
    ProfileScreen:
    FavoritesScreen:
    DonationScreen:
    SuggestionScreen:
    ContactScreen:

<WelcomeScreen>:
    name: 'welcome'
    canvas.before:
        Color:
            rgba: 0.1, 0.4, 0.8, 1
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation: 'vertical'
        padding: [dp(40), dp(60), dp(40), dp(20)]
        spacing: dp(20)
        MDIcon:
            icon: "shield-check-outline"
            font_size: "100sp"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": .5}
        MDLabel:
            text: "ALERTE_APP"
            halign: "center"
            font_style: "H4"
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        MDLabel:
            text: "Protection active 24h/24.\\nSécurité instantanée."
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.9, 0.9, 0.9, 1
        Widget:
            size_hint_y: 1
        MDFillRoundFlatButton:
            text: "DÉMARRER LA PROTECTION"
            size_hint_x: 1
            md_bg_color: 1, 1, 1, 1
            text_color: 0.1, 0.4, 0.8, 1
            on_release: root.manager.current = 'main' if app.check_user_exists() else 'register'
        FooterLabel:

<RegisterScreen>:
    name: 'register'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Création de compte"
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(25)
            spacing: dp(15)
            MDTextField:
                id: user_name
                hint_text: "Nom complet"
                mode: "rectangle"
            MDTextField:
                id: user_phone
                hint_text: "Numéro de téléphone"
                mode: "rectangle"
            MDFillRoundFlatButton:
                text: "S'INSCRIRE"
                size_hint_x: 1
                on_release: app.register_user(user_name.text, user_phone.text)
            Widget:
            FooterLabel:

<MainScreen>:
    name: 'main'
    md_bg_color: 0.1, 0.4, 0.8, 1
    MDFloatLayout:
        MDTopAppBar:
            title: "Alerte_App"
            pos_hint: {"top": 1}
            right_action_items: [["heart", lambda x: app.change_screen('donation')], ["chat-question", lambda x: app.change_screen('suggestion')], ["phone", lambda x: app.change_screen('contact')]]
            elevation: 0
            md_bg_color: 0.1, 0.4, 0.8, 1
        
        LogoCoin:

        Widget:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, app.pulse_opacity
                Ellipse:
                    pos: self.center_x - app.pulse_radius/2, self.center_y - app.pulse_radius/2
                    size: app.pulse_radius, app.pulse_radius
        
        MDIconButton:
            id: sos_btn
            icon: "alert"
            md_bg_color: 0.9, 0.1, 0.1, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint: None, None
            size: dp(120), dp(120)
            on_release: app.trigger_emergency()
        
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(100)
            pos_hint: {"center_x": .5, "center_y": .08}
            MDCard:
                size_hint_x: .9
                pos_hint: {"center_x": .5}
                radius: [dp(20),]
                MDBoxLayout:
                    MDIconButton:
                        icon: "home"
                        size_hint_x: .33
                    MDIconButton:
                        icon: "account-cog"
                        size_hint_x: .33
                        on_release: root.manager.current = 'profile'
                    MDIconButton:
                        icon: "account-multiple-plus"
                        size_hint_x: .33
                        on_release: root.manager.current = 'favorites'
            FooterLabel:
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.7

<FavoritesScreen>:
    name: 'favorites'
    on_enter: app.load_favorites_list()
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Contacts de confiance"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        
        MDBoxLayout:
            padding: dp(15)
            spacing: dp(10)
            size_hint_y: None
            height: dp(80)
            MDTextField:
                id: fav_phone
                hint_text: "Chercher un numéro"
            MDIconButton:
                icon: "magnify"
                on_release: app.search_user_before_add(fav_phone.text)

        MDCard:
            id: search_result_card
            size_hint: .9, None
            height: 0
            opacity: 0
            pos_hint: {"center_x": .5}
            padding: dp(15)
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: dp(15)
                MDIcon:
                    icon: "account-circle"
                    font_size: "48sp"
                MDBoxLayout:
                    orientation: 'vertical'
                    MDLabel:
                        id: search_name
                        bold: True
                    MDRaisedButton:
                        text: "AJOUTER"
                        on_release: app.confirm_add_favorite()

        ScrollView:
            MDList:
                id: fav_list
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
            padding: dp(25)
            spacing: dp(15)
            orientation: 'vertical'
            MDTextField:
                id: edit_name
                hint_text: "Nom"
                mode: "rectangle"
            MDTextField:
                id: edit_phone
                hint_text: "Téléphone"
                mode: "rectangle"
            MDRaisedButton:
                text: "ENREGISTRER LES MODIFICATIONS"
                size_hint_x: 1
                on_release: app.update_profile(edit_name.text, edit_phone.text)
            Widget:
            FooterLabel:

<DonationScreen>:
    name: 'donation'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Soutenir"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(30)
            MDLabel:
                text: "Airtel Money: +243 844033904\\nOrange Money: +243 823789353"
                halign: "center"
            Widget:
        FooterLabel:

<SuggestionScreen>:
    name: 'suggestion'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Suggestion"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            padding: dp(20)
            spacing: dp(10)
            orientation: 'vertical'
            MDTextField:
                id: sugg_text
                hint_text: "Votre message..."
                multiline: True
            MDRaisedButton:
                text: "ENVOYER"
                on_release: app.send_suggestion(sugg_text.text)
            Widget:
        FooterLabel:

<ContactScreen>:
    name: 'contact'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Contact"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
        MDBoxLayout:
            padding: dp(30)
            MDLabel:
                text: "Email: o.londola@gmail.com\\nTel: +243 844033904"
                halign: "center"
            Widget:
        FooterLabel:
'''

class WelcomeScreen(MDScreen): pass
class RegisterScreen(MDScreen): pass
class MainScreen(MDScreen): pass
class ProfileScreen(MDScreen): pass
class FavoritesScreen(MDScreen): pass
class DonationScreen(MDScreen): pass
class SuggestionScreen(MDScreen): pass
class ContactScreen(MDScreen): pass

class Alerte_App(MDApp):
    pulse_radius = NumericProperty(dp(110))
    pulse_opacity = NumericProperty(0.4)
    current_lat, current_lon = 0, 0
    last_power_click, power_click_count = 0, 0
    temp_found_user, dialog = None, None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self):
        self.animate_radar()
        if platform == 'android':
            self.request_android_permissions()
        Clock.schedule_interval(self.check_for_alerts, 30)
        if platform == 'android': self.listen_power_button()

    def animate_radar(self, *args):
        anim = Animation(pulse_radius=dp(300), pulse_opacity=0, duration=2, t='out_quad')
        anim.bind(on_complete=lambda *x: self.reset_radar())
        anim.start(self)

    def reset_radar(self):
        self.pulse_radius, self.pulse_opacity = dp(110), 0.4
        self.animate_radar()

    # --- NAVIGATION ---
    def change_screen(self, name): self.root.current = name
    def go_back(self): self.root.current = 'main'

    # --- RECHERCHE ET FAVORIS ---
    def search_user_before_add(self, phone):
        phone = phone.strip()
        try:
            res = requests.get(f"{FIREBASE_DB_URL}utilisateurs/{phone}.json", timeout=5).json()
            screen = self.root.get_screen('favorites')
            if res:
                self.temp_found_user = {"nom": res.get('nom'), "tel": phone}
                screen.ids.search_name.text = f"Trouvé : {res.get('nom')}"
                Animation(height=dp(100), opacity=1, duration=0.3).start(screen.ids.search_result_card)
            else:
                self.show_alert_dialog("Inconnu", "Ce numéro n'est pas inscrit.")
        except: self.show_alert_dialog("Erreur", "Connexion impossible.")

    def confirm_add_favorite(self):
        if self.temp_found_user and store.exists('user'):
            u = store.get('user')
            favs = u.get('favorites', [])
            if not any(f['tel'] == self.temp_found_user['tel'] for f in favs):
                favs.append(self.temp_found_user)
                store.put('user', name=u['name'], phone=u['phone'], favorites=favs)
                self.load_favorites_list()
                self.root.get_screen('favorites').ids.search_result_card.height = 0
                self.show_alert_dialog("Succès", "Contact ajouté.")

    def load_favorites_list(self):
        fav_list = self.root.get_screen('favorites').ids.fav_list
        fav_list.clear_widgets()
        if store.exists('user'):
            for f in store.get('user').get('favorites', []):
                item = TwoLineAvatarIconListItem(text=f['nom'], secondary_text=f['tel'])
                item.add_widget(IconLeftWidget(icon="account-star"))
                fav_list.add_widget(item)

    # --- SOS & GEOLOC ---
    def trigger_emergency(self):
        if store.exists('user'):
            u = store.get('user')
            alerte = {"nom": u['name'], "tel": u['phone'], "lat": self.current_lat, "lon": self.current_lon, "time": time.time()}
            try: requests.post(f"{FIREBASE_DB_URL}alertes.json", json=alerte, timeout=5)
            except: pass
            self.show_alert_dialog("SOS Envoyé", "Vos contacts ont été alertés.")

    def check_for_alerts(self, *args):
        try:
            res = requests.get(f"{FIREBASE_DB_URL}alertes.json", timeout=5).json()
            if not res or not store.exists('user'): return
            u = store.get('user')
            for key, data in res.items():
                if data['tel'] == u['phone']: continue
                dist = self.get_distance(self.current_lat, self.current_lon, data['lat'], data['lon'])
                if dist < 500: # Alerte si à moins de 500m
                    self.show_alert_dialog("⚠️ ALERTE PROXIMITÉ", f"{data['nom']} est en danger près de vous !")
        except: pass

    def get_distance(self, lat1, lon1, lat2, lon2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi, dlambda = math.radians(lat2-lat1), math.radians(lon2-lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # --- ANDROID SPECIFIC ---
    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION], self.setup_gps)

    def setup_gps(self, *args):
        try:
            from plyer import gps
            gps.configure(on_location=self.on_loc)
            gps.start(1000, 1)
        except: pass

    def on_loc(self, **kwargs):
        self.current_lat, self.current_lon = kwargs.get('lat', 0), kwargs.get('lon', 0)

    def listen_power_button(self):
        try:
            from android.broadcast import BroadcastReceiver
            self.br = BroadcastReceiver(lambda c, i: self.handle_power_click(), actions=['android.intent.action.SCREEN_OFF'])
            self.br.start()
        except: pass

    def handle_power_click(self):
        now = time.time()
        if now - self.last_power_click < 5: self.power_click_count += 1
        else: self.power_click_count = 1
        self.last_power_click = now
        if self.power_click_count >= 4: self.trigger_emergency()

    # --- UTILS ---
    def register_user(self, name, phone):
        if name and phone:
            store.put('user', name=name, phone=phone, favorites=[])
            try: requests.patch(f"{FIREBASE_DB_URL}utilisateurs/{phone}.json", json={"nom": name})
            except: pass
            self.root.current = 'main'

    def check_user_exists(self): return store.exists('user')

    def show_alert_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title, text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

if __name__ == '__main__':
    Alerte_App().run()
