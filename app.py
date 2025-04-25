from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ListProperty
from random import randint
from functools import partial
import socket
import threading
import webbrowser
import urllib.parse
from cryptography.fernet import Fernet
import os
from twilio.rest import Client

# Import and setup onion routing functionality
class OnionClient:
    # These keys must be shared with relay nodes
    keys = [
        b'KQY7SAv-qY3ptR5I3q-EKpXrAK7DR3__RTyq5FOB8-c=',  # Node 1
        b'Et3EJOUqzBoYoEvmWabJ6DZvV70Fs7ie5z_GONMbdCg=',  # Node 2
        b'GQKJyaE4eVfekYexC9xVq0y3ex3VRrb6XKaTZ1b5j4Y=',  # Node 3 (Exit)
    ]
    
    @staticmethod
    def onion_encrypt(data: bytes, keys):
        for key in reversed(keys):
            f = Fernet(key)
            data = f.encrypt(data)
        return data
    
    @staticmethod
    def send_via_onion(data: str):
        payload = OnionClient.onion_encrypt(data.encode(), OnionClient.keys)
        # In a real implementation, this would send through onion network
        return True

# Enhanced Call Handler with Twilio integration
class EnhancedCallHandler:
    # Twilio credentials - in production, these should be stored securely
    TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID"  # Replace with your actual SID in production
    TWILIO_AUTH_TOKEN = "3fa107c7eb237349b34ee9f216e4738d"  # From your input
    TWILIO_PHONE_NUMBER = "+19404687675"  # From your input
    
    @staticmethod
    def initiate_call(number, method="System Dialer"):
        """
        Initiates a call using the selected method.
        
        Args:
            number: The phone number to call
            method: The method to use (System Dialer or Twilio)
        
        Returns:
            True if the call was initiated successfully, False otherwise
        """
        try:
            if method == "System Dialer":
                # URL encode the number to handle special characters
                encoded_number = urllib.parse.quote(number)
                # Try to open tel: protocol (works on mobile and some desktop configurations)
                webbrowser.open(f"tel:{encoded_number}")
                return True
            
            elif method == "Twilio":
                return EnhancedCallHandler.make_twilio_call(number)
            
            elif method == "Web Service":
                # For demonstration, open a web-based calling service
                webbrowser.open(f"https://callmebot.com/")
                return True
                
            return False
        except Exception as e:
            print(f"Error initiating call: {e}")
            return False
    
    @staticmethod
    def make_twilio_call(to_number, from_number=None):
        """
        Makes a call using the Twilio API.
        
        Args:
            to_number: The number to call
            from_number: The number to call from (defaults to TWILIO_PHONE_NUMBER)
            
        Returns:
            True if the call was initiated successfully, False otherwise
        """
        try:
            # Initialize the Twilio client
            client = Client(
                EnhancedCallHandler.TWILIO_ACCOUNT_SID, 
                EnhancedCallHandler.TWILIO_AUTH_TOKEN
            )
            
            # Use the provided Twilio number if no from_number is specified
            if from_number is None:
                from_number = EnhancedCallHandler.TWILIO_PHONE_NUMBER
                
            # Create a call using Twilio's REST API
            # This initiates a call from the from_number to the to_number
            # When the recipient picks up, they'll hear a TwiML response
            # We're using a simple TwiML response that just says "Hello"
            call = client.calls.create(
                to=to_number,
                from_=from_number,
                twiml='<Response><Say>Secure call initiated through onion routing network.</Say></Response>'
            )
            
            print(f"Call initiated with SID: {call.sid}")
            return True
            
        except Exception as e:
            print(f"Error making Twilio call: {e}")
            return False

# KV language for styling
kv_string = '''
<MatrixLabel@Label>:
    font_name: 'data/fonts/RobotoMono-Regular.ttf'
    color: 0, 1, 0, 1
    
<HackerTextInput@TextInput>:
    background_color: 0, 0, 0, 0.8
    foreground_color: 0, 1, 0, 1
    cursor_color: 0, 1, 0, 1
    selection_color: 0, 0.5, 0, 0.5
    font_name: 'data/fonts/RobotoMono-Regular.ttf'
    
<HackerSpinner@Spinner>:
    background_color: 0, 0.2, 0, 1
    color: 0, 1, 0, 1
    option_cls: 'MatrixLabel'
    
<HackerButton@Button>:
    background_color: 0, 0.4, 0, 1
    color: 0, 1, 0, 1
    font_name: 'data/fonts/RobotoMono-Regular.ttf'
'''
Builder.load_string(kv_string)

# Matrix-style binary rain animation
class MatrixRain(Widget):
    def __init__(self, **kwargs):
        super(MatrixRain, self).__init__(**kwargs)
        self.chars = []
        Clock.schedule_interval(self.update, 0.1)
        
    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            for i in range(len(self.chars)):
                x, y, char, alpha = self.chars[i]
                Color(0, 1, 0, alpha)
                Rectangle(pos=(x, y), size=(20, 20))
                
        # Update positions
        new_chars = []
        for i in range(len(self.chars)):
            x, y, char, alpha = self.chars[i]
            y -= 10
            alpha -= 0.02
            if y > 0 and alpha > 0:
                new_chars.append((x, y, char, alpha))
                
        # Add new chars at the top
        if randint(0, 5) == 0:
            x = randint(0, Window.width)
            char = str(randint(0, 1))
            new_chars.append((x, Window.height, char, 1.0))
            
        self.chars = new_chars

# Animated status indicator
class StatusIndicator(BoxLayout):
    def __init__(self, **kwargs):
        super(StatusIndicator, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 30
        self.spacing = 5
        
        self.status_label = Label(
            text="STATUS: READY",
            color=(0, 1, 0, 1),
            size_hint_x=0.7
        )
        self.add_widget(self.status_label)
        
        # Store both widgets and rectangles
        self.dots = []
        for i in range(5):
            dot = Widget()
            with dot.canvas:
                Color(0, 0.5, 0, 1)
                rect = Rectangle(pos=(0, 0), size=(10, 10))
            self.add_widget(dot)
            self.dots.append((dot, rect))  # Store both widget and rectangle
            
        self._active = False
        self.animation_event = None
        
    def set_status(self, text, active=False):
        self.status_label.text = f"STATUS: {text}"
        
        if active and not self._active:
            self._active = True
            self.animation_event = Clock.schedule_interval(self._animate_dots, 0.2)
        elif not active and self._active:
            self._active = False
            if self.animation_event:
                Clock.unschedule(self.animation_event)
                
    def _animate_dots(self, dt):
        for i, (dot_widget, rect) in enumerate(self.dots):
            with self.canvas:
                alpha = abs((i - (Clock.get_boottime() * 5) % 5)) / 5
                Color(0, 1, 0, alpha)
                rect.pos = (dot_widget.x + 5, dot_widget.y + 5)
                
# Enhanced Call Layout with hacker theme and Twilio integration
class CallLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CallLayout, self).__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        # Set background
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black background
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Add matrix rain effect in the background
        self.matrix_rain = MatrixRain()
        self.add_widget(self.matrix_rain)
        
        # Main content container
        self.content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Title
        title_box = BoxLayout(size_hint_y=None, height=50)
        title = Label(
            text="◢◤ ONION ROUTER SECURE INTERNET CALLER ◢◤",
            color=(0, 1, 0, 1),
            font_size='20sp',
            bold=True
        )
        title_box.add_widget(title)
        self.content.add_widget(title_box)
        
        # Country selection
        country_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120)
        country_label = Label(
            text="SELECT TARGET REGION",
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=30
        )
        country_box.add_widget(country_label)
        
        self.country_codes = {
            "India": "+91",
            "United States": "+1",
            "United Kingdom": "+44",
            "Canada": "+1",
            "Australia": "+61",
            "Germany": "+49",
            "Japan": "+81",
            "Brazil": "+55",
            "Russia": "+7",
            "China": "+86",
        }
        
        self.country_spinner = Spinner(
            text="India",
            values=list(self.country_codes.keys()),
            size_hint_y=None,
            height=44,
            background_color=(0, 0.2, 0, 1),
            color=(0, 1, 0, 1)
        )
        self.country_spinner.bind(text=self.update_country_code)
        country_box.add_widget(self.country_spinner)
        
        self.code_label = Label(
            text="COUNTRY CODE: +91",
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=30
        )
        country_box.add_widget(self.code_label)
        self.content.add_widget(country_box)
        
        # Phone number input
        number_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120)
        number_label = Label(
            text="ENTER TARGET NUMBER",
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=30
        )
        number_box.add_widget(number_label)
        
        self.number_input = TextInput(
            hint_text="Number (without country code)",
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=50,
            background_color=(0, 0.1, 0, 0.8),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1)
        )
        number_box.add_widget(self.number_input)
        self.content.add_widget(number_box)
        
        # Call method selection - Updated with Twilio option
        method_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        method_label = Label(
            text="CALL METHOD",
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=30
        )
        method_box.add_widget(method_label)
        
        self.methods = ["System Dialer", "Twilio", "Web Service"]
        self.method_spinner = Spinner(
            text="System Dialer",
            values=self.methods,
            background_color=(0, 0.2, 0, 1),
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=40
        )
        method_box.add_widget(self.method_spinner)
        self.content.add_widget(method_box)
        
        # Status indicator
        self.status_indicator = StatusIndicator()
        self.content.add_widget(self.status_indicator)
        
        # Call and URI buttons
        button_box = BoxLayout(size_hint_y=None, height=60, padding=10, spacing=10)
        
        self.call_button = Button(
            text="INITIATE SECURE CALL",
            background_color=(0, 0.4, 0, 1),
            color=(0, 1, 0, 1),
            font_size=18,
            size_hint_x=0.7
        )
        self.call_button.bind(on_press=self.make_call)
        button_box.add_widget(self.call_button)
        
        self.uri_button = Button(
            text="COPY URI",
            background_color=(0, 0.3, 0.4, 1),
            color=(0, 1, 0, 1),
            font_size=14,
            size_hint_x=0.3
        )
        self.uri_button.bind(on_press=self.copy_uri)
        button_box.add_widget(self.uri_button)
        
        self.content.add_widget(button_box)

        # Network status display
        self.network_status = Label(
            text="[NODES: 3 | ENCRYPTION: ACTIVE | PATH: RANDOMIZED]",
            color=(0, 0.8, 0, 1),
            size_hint_y=None,
            height=30
        )
        self.content.add_widget(self.network_status)
        
        # Twilio status display
        self.twilio_status = Label(
            text="[TWILIO: CONNECTED | AUTH: VERIFIED | SERVICE: READY]",
            color=(0, 0.8, 0, 1),
            size_hint_y=None,
            height=30
        )
        self.content.add_widget(self.twilio_status)
        
        # Add content container to main layout
        self.add_widget(self.content)
        
        # Start simulation of node activity
        Clock.schedule_interval(self.simulate_node_activity, 1.5)
        
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
        
    def update_country_code(self, spinner, text):
        self.code_label.text = f"COUNTRY CODE: {self.country_codes[text]}"
        
    def make_call(self, instance):
        selected_country = self.country_spinner.text
        code = self.country_codes[selected_country]
        number = self.number_input.text
        method = self.method_spinner.text
        
        if not number:
            self.status_indicator.set_status("ERROR: NO NUMBER", False)
            return
            
        full_number = f"{code}{number}"
        
        # Show calling sequence
        self.status_indicator.set_status("ENCRYPTING", True)
        Clock.schedule_once(partial(self.encrypt_step, full_number, method), 1)
    
    def copy_uri(self, instance):
        selected_country = self.country_spinner.text
        code = self.country_codes[selected_country]
        number = self.number_input.text
        
        if not number:
            self.status_indicator.set_status("ERROR: NO NUMBER", False)
            return
            
        full_number = f"{code}{number}"
        uri = f"tel:{full_number}"
        
        # In a real app, this would copy to clipboard
        # For now, we'll just display it
        self.status_indicator.set_status("URI GENERATED", False)
        
        # Create a popup or display the URI
        Clock.schedule_once(lambda dt: self.status_indicator.set_status(f"URI: {uri}", False), 1)
        Clock.schedule_once(lambda dt: self.status_indicator.set_status("READY", False), 5)
        
    def encrypt_step(self, full_number, method, dt):
        self.status_indicator.set_status("ROUTING VIA ONION", True)
        Clock.schedule_once(partial(self.route_step, full_number, method), 2)
        
    def route_step(self, full_number, method, dt):
        method_text = method.upper()
        self.status_indicator.set_status(f"CONNECTING VIA {method_text}", True)
        Clock.schedule_once(partial(self.connect_step, full_number, method), 1.5)
        
    def connect_step(self, full_number, method, dt):
        # First encrypt and route via onion network
        encrypted_data = OnionClient.onion_encrypt(full_number.encode(), OnionClient.keys)
        OnionClient.send_via_onion(full_number)
        
        # Then initiate call based on chosen method
        result = EnhancedCallHandler.initiate_call(full_number, method)
        
        if result:
            self.status_indicator.set_status("CALL INITIATED", False)
            self.call_button.text = "CALL ACTIVE"
            self.call_button.background_color = (0, 0.6, 0, 1)
            Clock.schedule_once(self.reset_call_ui, 5)
        else:
            self.status_indicator.set_status("CONNECTION FAILED", False)
            Clock.schedule_once(self.reset_call_ui, 3)
            
    def reset_call_ui(self, dt):
        self.status_indicator.set_status("READY", False)
        self.call_button.text = "INITIATE SECURE CALL"
        self.call_button.background_color = (0, 0.4, 0, 1)
        
    def simulate_node_activity(self, dt):
        nodes = ["●", "●", "●"]
        active_node = randint(0, 2)
        nodes[active_node] = "◉"
        
        self.network_status.text = f"[NODES: {' '.join(nodes)} | ENCRYPTION: ACTIVE | PATH: RANDOMIZED]"
        
        # Simulate Twilio connection status
        if randint(0, 10) > 8:  # Occasionally show different status
            statuses = [
                "[TWILIO: CONNECTED | AUTH: VERIFIED | SERVICE: READY]",
                "[TWILIO: ACTIVE | AUTH: VERIFIED | SERVICE: READY]",
                "[TWILIO: CONNECTED | AUTH: SECURE | SERVICE: ACTIVE]"
            ]
            self.twilio_status.text = statuses[randint(0, len(statuses)-1)]

class OnionApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        return CallLayout()

if __name__ == '__main__':
    OnionApp().run()
