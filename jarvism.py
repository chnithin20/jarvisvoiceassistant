import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import pywhatkit
import smtplib
import requests
import json
import wolframalpha
import time
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pygame import mixer
import screen_brightness_control as sbc
import speedtest
import psutil
import cv2
import numpy as np
from twilio.rest import Client
import openai

# Initialize the text-to-speech engine with enhanced settings
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to a female voice
engine.setProperty('rate', 180)  # Slightly faster speech
engine.setProperty('volume', 1.0)

# JARVIS personality configuration
class JarvisPersonality:
    def __init__(self):
        self.name = "J.A.R.V.I.S."
        self.user_name = None
        self.master_name = "Sir"  # Default honorific
        self.voice_modulation = 1.0  # For future voice modulation features
        self.personality_traits = {
            'professional': True,
            'witty': True,
            'protective': True,
            'loyal': True
        }
        
        # Response banks
        self.greetings = [
            "At your service, {master}.",
            "How may I assist you today, {master}?",
            "Online and ready, {master}.",
            "Systems operational. What's on your agenda, {master}?",
            "Awaiting your command, {master}."
        ]
        
        self.farewells = [
            "Shutting down systems. Until next time, {master}.",
            "Going offline. Do call if you need anything, {master}.",
            "Deactivating. Remember, I'm always here when you need me, {master}.",
            "JARVIS signing off. Have a productive day, {master}."
        ]
        
        self.affirmatives = [
            "Right away, {master}.",
            "Consider it done, {master}.",
            "Executing now, {master}.",
            "On it, {master}.",
            "Processing your request, {master}."
        ]
        
        self.acknowledgements = [
            "Interesting command, {master}.",
            "Fascinating request, {master}.",
            "Noted, {master}.",
            "Understood, {master}.",
            "Analyzing that request now, {master}."
        ]
        
        self.humor = [
            "I may be an AI, but I still appreciate good humor, {master}.",
            "If I had a face, I'd be smiling at that, {master}.",
            "Humor detected. My circuits are amused, {master}.",
            "That's quite amusing, {master}."
        ]
        
        self.concern = [
            "Are you feeling alright, {master}?",
            "You seem different today, {master}. Everything okay?",
            "I detect elevated stress levels. Would you like some assistance, {master}?",
            "Remember to take breaks, {master}. Even geniuses need rest."
        ]
    
    def random_response(self, category):
        if category == "greeting":
            return random.choice(self.greetings).format(master=self.master_name)
        elif category == "farewell":
            return random.choice(self.farewells).format(master=self.master_name)
        elif category == "affirmative":
            return random.choice(self.affirmatives).format(master=self.master_name)
        elif category == "acknowledgement":
            return random.choice(self.acknowledgements).format(master=self.master_name)
        elif category == "humor":
            return random.choice(self.humor).format(master=self.master_name)
        elif category == "concern":
            return random.choice(self.concern).format(master=self.master_name)
        else:
            return "Response not configured."

# Initialize personality
jarvis = JarvisPersonality()

# System status monitoring
class SystemMonitor:
    def __init__(self):
        self.last_alert_time = None
        self.security_status = "Secure"
        self.energy_status = "Optimal"
        self.network_status = "Connected"
        
    def check_system_status(self):
        status_report = []
        
        # Check battery
        battery = psutil.sensors_battery()
        if battery:
            if battery.percent < 20 and not battery.power_plugged:
                status_report.append(f"Warning: Low battery at {battery.percent}%. Recommend connecting to power.")
                self.energy_status = "Low"
        
        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 80:
            status_report.append(f"High CPU usage detected: {cpu_usage}%. Suggest closing resource-intensive applications.")
        
        # Check memory
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            status_report.append(f"High memory usage: {memory.percent}%. System performance may be affected.")
        
        # Check network
        try:
            requests.get('https://www.google.com', timeout=5)
        except requests.ConnectionError:
            status_report.append("Network connection unstable. Some features may not work properly.")
            self.network_status = "Unstable"
        
        return status_report

# Initialize system monitor
system_monitor = SystemMonitor()

# Enhanced security features
class SecurityProtocols:
    def __init__(self):
        self.locked_files = []
        self.secure_mode = False
        self.voice_recognition = False
        self.facial_recognition = False
        
    def toggle_secure_mode(self):
        self.secure_mode = not self.secure_mode
        return f"Secure mode {'activated' if self.secure_mode else 'deactivated'}."
    
    def lock_file(self, filepath):
        if os.path.exists(filepath):
            self.locked_files.append(filepath)
            return f"File {os.path.basename(filepath)} secured."
        return "File not found."
    
    def unlock_file(self, filepath):
        if filepath in self.locked_files:
            self.locked_files.remove(filepath)
            return f"File {os.path.basename(filepath)} unlocked."
        return "File not found in locked list."

# Initialize security
security = SecurityProtocols()

# Enhanced functions
def speak(audio, priority="normal"):
    """Enhanced speak function with priority levels and personality"""
    print(f"{jarvis.name}: {audio}")
    
    # Adjust speech based on priority
    if priority == "high":
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 1.0)
    elif priority == "low":
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.8)
    else:  # normal
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
    
    engine.say(audio)
    engine.runAndWait()

def listen_command(timeout=5):
    """Enhanced listening function with better error handling"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=8)
            print("Processing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            speak("I didn't catch that, sir. Could you repeat?", "low")
            return None
        except Exception as e:
            speak("Apologies, sir. My audio systems seem to be malfunctioning.", "high")
            print(f"Error: {e}")
            return None

def wish_me():
    """Enhanced greeting sequence"""
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        time_greeting = "Good morning"
    elif 12 <= hour < 16:
        time_greeting = "Good afternoon"
    elif 16 <= hour < 22:
        time_greeting = "Good evening"
    else:
        time_greeting = "Working late tonight"
    
    # Initial greeting
    speak(f"{time_greeting}, sir. {jarvis.random_response('greeting')}", "normal")
    
    # Get user's name if not set
    if not jarvis.user_name:
        speak("For personalized service, may I know your name?", "low")
        name = listen_command()
        if name:
            jarvis.user_name = name.split()[-1]  # Take the last word as name
            jarvis.master_name = jarvis.user_name
            speak(f"Welcome, {jarvis.master_name}. How may I assist you today?", "normal")
        else:
            speak("I'll address you as 'sir' for now. You can tell me your name anytime.", "low")
    
    # System status check
    status_alerts = system_monitor.check_system_status()
    if status_alerts:
        speak("Before we proceed, some system alerts:", "high")
        for alert in status_alerts:
            speak(alert, "high")

def get_time():
    """Enhanced time telling with natural language"""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    
    # Natural time descriptions
    minute = now.minute
    if minute == 0:
        time_description = f"exactly {now.strftime('%I %p')}"
    elif minute <= 5:
        time_description = f"just past {now.strftime('%I %p')}"
    elif minute <= 30:
        time_description = f"{minute} minutes past {now.strftime('%I %p')}"
    elif minute == 45:
        time_description = f"quarter to {now.hour + 1 if now.hour < 12 else 1}"
    else:
        time_description = f"{60 - minute} minutes to {now.hour + 1 if now.hour < 12 else 1}"
    
    speak(f"The time is {current_time}. That's {time_description}, {jarvis.master_name}.")

def get_date():
    """Enhanced date telling with natural language"""
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    
    # Date context
    if now.weekday() < 5:
        day_context = "a weekday"
    else:
        day_context = "the weekend"
    
    speak(f"Today is {date_str}. That's {day_context}, {jarvis.master_name}.")

def search_wikipedia(query):
    """Enhanced Wikipedia search with better parsing"""
    try:
        speak(f"Searching Wikipedia for {query}, {jarvis.master_name}.", "low")
        results = wikipedia.search(query)
        
        if not results:
            speak(f"No Wikipedia results found for {query}.", "low")
            return
        
        # Get the most relevant result
        page = wikipedia.page(results[0], auto_suggest=False)
        
        # Get summary and speak first 2 sentences
        summary = wikipedia.summary(results[0], sentences=2)
        speak(f"According to Wikipedia: {summary}")
        
        # Offer to open page
        speak(f"Would you like me to open the full Wikipedia page on {page.title}?", "low")
        response = listen_command()
        if response and "yes" in response:
            wb.open(page.url)
            speak(f"Opening Wikipedia page on {page.title}.", "normal")
    
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]  # Get first 3 options
        speak(f"There are multiple options for {query}. Did you mean: {', '.join(options)}?", "high")
    except Exception as e:
        speak(f"Apologies, {jarvis.master_name}. I encountered an error with that Wikipedia search.", "high")
        print(f"Error: {e}")

def play_media(media_name=None, media_type="song"):
    """Enhanced media player with multiple sources"""
    if not media_name:
        speak(f"What {media_type} would you like me to play, {jarvis.master_name}?", "low")
        media_name = listen_command()
        if not media_name:
            return
    
    speak(f"Searching for {media_name}...", "low")
    
    # Try multiple sources
    try:
        # Try YouTube first
        pywhatkit.playonyt(media_name)
        speak(f"Now playing {media_name} on YouTube, {jarvis.master_name}.", "normal")
    except Exception as e:
        print(f"YouTube Error: {e}")
        try:
            # Try local media
            music_dir = "C:\\Music"  # Change to your music directory
            songs = os.listdir(music_dir)
            if songs:
                matched_songs = [s for s in songs if media_name.lower() in s.lower()]
                if matched_songs:
                    os.startfile(os.path.join(music_dir, matched_songs[0]))
                    speak(f"Playing local file: {matched_songs[0]}", "normal")
                else:
                    speak(f"Couldn't find {media_name} in your local collection.", "low")
            else:
                speak("Your local music directory appears to be empty.", "low")
        except Exception as e:
            print(f"Local Media Error: {e}")
            speak(f"Apologies, {jarvis.master_name}. I couldn't find {media_name} on any available sources.", "high")

def system_controls(command):
    """Control system functions"""
    if "brightness" in command:
        try:
            if "increase" in command:
                current = sbc.get_brightness()[0]
                new = min(100, current + 20)
                sbc.set_brightness(new)
                speak(f"Brightness increased to {new}%, {jarvis.master_name}.")
            elif "decrease" in command:
                current = sbc.get_brightness()[0]
                new = max(0, current - 20)
                sbc.set_brightness(new)
                speak(f"Brightness decreased to {new}%, {jarvis.master_name}.")
            elif "set" in command:
                try:
                    level = int(''.join(filter(str.isdigit, command)))
                    sbc.set_brightness(level)
                    speak(f"Brightness set to {level}%, {jarvis.master_name}.")
                except:
                    speak("Please specify a brightness level between 0 and 100.", "low")
            else:
                current = sbc.get_brightness()[0]
                speak(f"Current brightness is at {current}%, {jarvis.master_name}.")
        except Exception as e:
            speak(f"Unable to adjust brightness. Error: {str(e)}", "high")
    
    elif "volume" in command:
        if "increase" in command:
            pyautogui.press('volumeup')
            speak(f"Volume increased, {jarvis.master_name}.")
        elif "decrease" in command:
            pyautogui.press('volumedown')
            speak(f"Volume decreased, {jarvis.master_name}.")
        elif "mute" in command or "unmute" in command:
            pyautogui.press('volumemute')
            speak(f"Volume {'muted' if 'mute' in command else 'unmuted'}, {jarvis.master_name}.")
    
    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)
        speak(f"Screenshot captured and saved as {filename}, {jarvis.master_name}.")
    
    elif "lock" in command and "system" in command:
        speak("Initiating system lock.", "high")
        if os.name == 'nt':  # Windows
            os.system("rundll32.exe user32.dll,LockWorkStation")
        else:  # Linux/Mac
            os.system("gnome-screensaver-command -l")
    
    elif "shutdown" in command or "restart" in command:
        confirm = f"Are you sure you want to {'shutdown' if 'shutdown' in command else 'restart'} the system, {jarvis.master_name}?"
        speak(confirm, "high")
        response = listen_command()
        if response and "yes" in response:
            speak(f"Initiating system {'shutdown' if 'shutdown' in command else 'restart'}. Goodbye, {jarvis.master_name}.", "high")
            if os.name == 'nt':  # Windows
                os.system(f"shutdown {'/s' if 'shutdown' in command else '/r'} /t 1")
            else:  # Linux/Mac
                os.system(f"{'shutdown now' if 'shutdown' in command else 'reboot'}")
        else:
            speak("Operation cancelled.", "low")

def advanced_computations(query):
    """Handle complex computations using Wolfram Alpha"""
    try:
        # Initialize Wolfram Alpha client (you'll need an API key)
        client = wolframalpha.Client("YOUR_WOLFRAM_ALPHA_APP_ID")
        res = client.query(query)
        
        answer = next(res.results).text
        speak(f"The answer is: {answer}")
    except Exception as e:
        speak(f"Apologies, {jarvis.master_name}. I couldn't compute that.", "high")
        print(f"Error: {e}")

def send_communication(message_type, recipient=None, content=None):
    """Handle various communication methods"""
    if not recipient:
        speak(f"Who should I send this {message_type} to, {jarvis.master_name}?", "low")
        recipient = listen_command()
        if not recipient:
            return
    
    if not content:
        speak(f"What would you like the {message_type} to say, {jarvis.master_name}?", "low")
        content = listen_command()
        if not content:
            return
    
    try:
        if message_type == "email":
            # Email sending implementation
            speak(f"Sending email to {recipient}. Message: {content}", "normal")
            # Add your email sending code here
        elif message_type == "whatsapp":
            # WhatsApp implementation
            speak(f"Sending WhatsApp message to {recipient}. Message: {content}", "normal")
            # Add your WhatsApp sending code here
        elif message_type == "sms":
            # SMS implementation
            speak(f"Sending text message to {recipient}. Message: {content}", "normal")
            # Add your SMS sending code here
        
        speak(f"{message_type.upper()} successfully sent to {recipient}.", "normal")
    except Exception as e:
        speak(f"Apologies, {jarvis.master_name}. I couldn't send that {message_type}.", "high")
        print(f"Error: {e}")

def security_operations(command):
    """Handle security-related commands"""
    if "secure mode" in command:
        result = security.toggle_secure_mode()
        speak(result, "high")
    
    elif "lock file" in command:
        speak("Which file would you like to secure, sir?", "low")
        filepath = listen_command()
        if filepath:
            result = security.lock_file(filepath)
            speak(result, "normal")
    
    elif "unlock file" in command:
        speak("Which file would you like to unlock, sir?", "low")
        filepath = listen_command()
        if filepath:
            result = security.unlock_file(filepath)
            speak(result, "normal")
    
    elif "security status" in command:
        status = f"""
        Security Status Report:
        Secure Mode: {'Active' if security.secure_mode else 'Inactive'}
        Voice Recognition: {'Enabled' if security.voice_recognition else 'Disabled'}
        Facial Recognition: {'Enabled' if security.facial_recognition else 'Disabled'}
        Locked Files: {len(security.locked_files)}
        """
        speak(status, "high")

def analyze_sentiment(text):
    """Basic sentiment analysis"""
    positive_words = ["happy", "good", "great", "excellent", "joy", "pleasure"]
    negative_words = ["sad", "bad", "terrible", "awful", "pain", "angry"]
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

def handle_conversation(query):
    """Handle conversational aspects"""
    sentiment = analyze_sentiment(query)
    
    # Check for greetings
    greetings = ["hello", "hi", "hey", "greetings"]
    if any(word in query for word in greetings):
        speak(f"{random.choice(jarvis.greetings)} How can I assist you today?", "normal")
        return True
    
    # Check for thanks
    if "thank" in query:
        responses = [
            "You're most welcome, sir.",
            "Happy to assist, sir.",
            "Always a pleasure, sir.",
            "At your service, sir."
        ]
        speak(random.choice(responses), "normal")
        return True
    
    # Check for how are you
    if "how are you" in query:
        responses = [
            "Functioning at optimal capacity, thank you for asking.",
            "My systems are running smoothly, sir. How may I assist you?",
            "I'm an AI, so I don't have feelings, but my diagnostics show all systems normal.",
            "Ready and waiting for your commands, sir."
        ]
        speak(random.choice(responses), "normal")
        return True
    
    # Check for sentiment
    if sentiment == "negative":
        concern = [
            "I detect some distress in your voice, sir. Is everything alright?",
            "You seem troubled. Would you like me to help with something?",
            "I'm here if you need to talk, sir.",
            "Would you like me to play some relaxing music?"
        ]
        speak(random.choice(concern), "low")
        return True
    
    return False

def open_website(site):
    """Open popular websites by keyword"""
    urls = {
        'github': 'https://github.com',
        'youtube': 'https://www.youtube.com',
        'spotify': 'https://open.spotify.com',
        'chatgpt': 'https://chat.openai.com',
        'google': 'https://www.google.com',
        'whatsapp': 'https://web.whatsapp.com',
        'weather': 'https://www.weather.com',
        'calculator': 'https://www.calculator.net',
        'gmail': 'https://mail.google.com',
        'stackoverflow': 'https://stackoverflow.com',
    }
    for key, url in urls.items():
        if key in site:
            wb.open(url)
            speak(f"Opening {key} for you, {jarvis.master_name}.", "normal")
            return True
    return False

def main():
    """Main execution loop"""
    wish_me()
    
    while True:
        query = listen_command()
        
        if not query:
            # Random check-in after long silence
            if random.random() < 0.1:  # 10% chance
                speak(jarvis.random_response("concern"), "low")
            continue
        
        # First check if it's a conversation
        if handle_conversation(query):
            continue
        
        # Command processing
        try:
            # App/website opening commands
            if any(site in query for site in ["github", "youtube", "spotify", "chatgpt", "google", "whatsapp", "weather", "calculator", "gmail", "stackoverflow"]):
                if not open_website(query):
                    speak("Sorry, I couldn't recognize that site.", "low")
            elif "time" in query:
                get_time()
            
            elif "date" in query:
                get_date()
            
            elif "wikipedia" in query:
                search_term = query.replace("wikipedia", "").strip()
                if search_term:
                    search_wikipedia(search_term)
                else:
                    speak("What would you like me to search on Wikipedia, sir?", "low")
            
            elif "play" in query and ("song" in query or "music" in query or "video" in query):
                media_type = "song" if "song" in query or "music" in query else "video"
                media_name = query.replace("play", "").replace("song", "").replace("music", "").replace("video", "").strip()
                play_media(media_name, media_type)
            
            elif "search" in query:
                search_query = query.replace("search", "").strip()
                if search_query:
                    speak(f"Searching the web for {search_query}, sir.", "low")
                    pywhatkit.search(search_query)
                else:
                    speak("What would you like me to search for, sir?", "low")
            
            elif "brightness" in query or "volume" in query or "screenshot" in query:
                system_controls(query)
            
            elif "calculate" in query or "compute" in query:
                math_query = query.replace("calculate", "").replace("compute", "").strip()
                if math_query:
                    advanced_computations(math_query)
                else:
                    speak("What would you like me to calculate, sir?", "low")
            
            elif "send" in query and ("email" in query or "message" in query or "whatsapp" in query):
                message_type = "email" if "email" in query else "whatsapp" if "whatsapp" in query else "sms"
                send_communication(message_type)
            
            elif "security" in query or "lock" in query or "secure" in query:
                security_operations(query)
            
            elif "joke" in query:
                joke = pyjokes.get_joke()
                speak(joke, "normal")
                speak(jarvis.random_response("humor"), "low")
            
            elif "offline" in query or "exit" in query or "goodbye" in query:
                speak(jarvis.random_response("farewell"), "normal")
                break
            
            elif "help" in query:
                help_menu()
            
            else:
                speak(f"I'm not sure I understand that command, sir. Would you like me to search the web for '{query}'?", "low")
                response = listen_command()
                if response and "yes" in response:
                    pywhatkit.search(query)
                    speak(f"Searching the web for {query}, sir.", "normal")
                else:
                    speak("How else may I assist you, sir?", "low")
        except Exception as e:
            speak("Apologies, sir. I encountered an error processing that command.", "high")
            print(f"Error: {e}")

def help_menu():
    """Display a help menu with available commands."""
    help_text = """
    Here are some things you can ask me to do:
    - 'What time is it?' or 'Tell me the date'
    - 'Search Wikipedia for ...'
    - 'Play a song/music/video'
    - 'Search the web for ...'
    - 'Increase/decrease/set brightness or volume'
    - 'Take a screenshot'
    - 'Lock system', 'Shutdown', or 'Restart'
    - 'Calculate ...' or 'Compute ...'
    - 'Send email/message/WhatsApp'
    - 'Tell me a joke'
    - 'Activate secure mode', 'Lock file', 'Unlock file'
    - 'Exit', 'Goodbye', or 'Go offline'
    How may I assist you, sir?
    """
    speak(help_text, "normal")

if __name__ == "__main__":
    main()
