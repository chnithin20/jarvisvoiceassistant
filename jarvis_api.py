from flask import Flask, request, jsonify, render_template
import pyttsx3
from jarvism import handle_conversation, get_time, get_date, search_wikipedia, play_media, system_controls, advanced_computations, send_communication, security_operations, open_website, jarvis

app = Flask(__name__)

# Initialize TTS engine for API
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

def process_command_api(user_message):
    # Try to handle as a conversation first
    conv_response = handle_conversation(user_message)
    if conv_response:
        # handle_conversation already speaks, but we want to return the same text
        return conv_response if isinstance(conv_response, str) else f"{jarvis.name}: (Conversational response sent)"
    # App/website opening
    if any(site in user_message for site in ["github", "youtube", "spotify", "chatgpt", "google", "whatsapp", "weather", "calculator", "gmail", "stackoverflow"]):
        opened = open_website(user_message)
        if opened:
            return f"Opening {user_message} for you."
        else:
            return "Sorry, I couldn't recognize that site."
    # Time/date
    if "time" in user_message:
        import io
        import sys
        buf = io.StringIO()
        sys.stdout = buf
        get_time()
        sys.stdout = sys.__stdout__
        return buf.getvalue().strip() or "Told the time."
    if "date" in user_message:
        import io
        import sys
        buf = io.StringIO()
        sys.stdout = buf
        get_date()
        sys.stdout = sys.__stdout__
        return buf.getvalue().strip() or "Told the date."
    # Wikipedia
    if "wikipedia" in user_message:
        search_term = user_message.replace("wikipedia", "").strip()
        if search_term:
            import io
            import sys
            buf = io.StringIO()
            sys.stdout = buf
            search_wikipedia(search_term)
            sys.stdout = sys.__stdout__
            return buf.getvalue().strip() or f"Searched Wikipedia for {search_term}."
        else:
            return "What would you like me to search on Wikipedia?"
    # Play media
    if "play" in user_message and ("song" in user_message or "music" in user_message or "video" in user_message):
        media_type = "song" if "song" in user_message or "music" in user_message else "video"
        media_name = user_message.replace("play", "").replace("song", "").replace("music", "").replace("video", "").strip()
        import io
        import sys
        buf = io.StringIO()
        sys.stdout = buf
        play_media(media_name, media_type)
        sys.stdout = sys.__stdout__
        return buf.getvalue().strip() or f"Playing {media_name}."
    # Search web
    if "search" in user_message:
        import pywhatkit
        search_query = user_message.replace("search", "").strip()
        if search_query:
            pywhatkit.search(search_query)
            return f"Searching the web for {search_query}."
        else:
            return "What would you like me to search for?"
    # System controls
    if any(word in user_message for word in ["brightness", "volume", "screenshot"]):
        import io
        import sys
        buf = io.StringIO()
        sys.stdout = buf
        system_controls(user_message)
        sys.stdout = sys.__stdout__
        return buf.getvalue().strip() or "System control executed."
    # Calculations
    if "calculate" in user_message or "compute" in user_message:
        math_query = user_message.replace("calculate", "").replace("compute", "").strip()
        if math_query:
            import io
            import sys
            buf = io.StringIO()
            sys.stdout = buf
            advanced_computations(math_query)
            sys.stdout = sys.__stdout__
            return buf.getvalue().strip() or f"Computed: {math_query}"
        else:
            return "What would you like me to calculate?"
    # Communication
    if "send" in user_message and ("email" in user_message or "message" in user_message or "whatsapp" in user_message):
        message_type = "email" if "email" in user_message else "whatsapp" if "whatsapp" in user_message else "sms"
        import io
        import sys
        buf = io.StringIO()
        sys.stdout = buf
        send_communication(message_type)
        sys.stdout = sys.__stdout__
        return buf.getvalue().strip() or f"Sent {message_type}."
    # Security
    if any(word in user_message for word in ["security", "lock", "secure"]):
        import io
        import sys
        buf = io.StringIO()
        sys.stdout = buf
        security_operations(user_message)
        sys.stdout = sys.__stdout__
        return buf.getvalue().strip() or "Security operation executed."
    # Jokes
    if "joke" in user_message:
        import pyjokes
        joke = pyjokes.get_joke()
        return joke
    # Exit
    if any(word in user_message for word in ["offline", "exit", "goodbye"]):
        return jarvis.random_response("farewell")
    # Help
    if "help" in user_message:
        return "You can ask me to open sites, tell time/date, search Wikipedia, play music, control system, send messages, and more!"
    # Fallback
    return f"I'm not sure I understand that command."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    response = process_command_api(user_message)
    return jsonify({'response': response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
