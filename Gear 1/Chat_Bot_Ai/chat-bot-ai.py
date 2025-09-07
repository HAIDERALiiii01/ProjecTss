import pyautogui
import time
import pyperclip
import google.generativeai as genai
import sys
import os


GEMINI_API_KEY = "your Gemini api key here"
MODEL_NAME = "gemini-1.5-flash-latest"  # Current fastest model as of 2025
WAIT_TIME = 25  # WhatsApp loading time
MAX_RETRIES = 3  # API retry attempts

# --- Validate API Key ---
if not GEMINI_API_KEY.strip():
    print("❌ Error: Gemini API Key missing! Get one from: https://aistudio.google.com/app/apikey")
    sys.exit(1)

# --- Initialize Gemini with latest settings ---
genai.configure(
    api_key=GEMINI_API_KEY,
    transport="rest",  # More stable than gRPC in some environments
    client_options={"api_endpoint": "generativelanguage.googleapis.com"}
)

# --- Model Verification ---
try:
    available_models = [m.name for m in genai.list_models()]
    if f"models/{MODEL_NAME}" not in available_models:
        print(f"⚠️ Model {MODEL_NAME} not available. Options:\n{available_models}")
        MODEL_NAME = "gemini-1.0-pro-latest"  # Fallback model
    model = genai.GenerativeModel(MODEL_NAME)
    print(f"✅ Using model: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Gemini Initialization Error: {e}")
    sys.exit(1)

# --- WhatsApp Automation (Updated for 2025) ---
def open_whatsapp(chat_name):
    """Modern WhatsApp Web interaction with error recovery"""
    try:
        # Windows 11/10 search (updated for 2025)
        pyautogui.hotkey('win', 's')
        time.sleep(5)
        pyautogui.write('WhatsApp', interval=0.05)  # Faster typing
        pyautogui.press('enter')
        time.sleep(25)
        
        # Modern chat search (Ctrl+Alt+/ still works in 2025)
        pyautogui.hotkey('ctrl', 'alt', '/')
        pyautogui.write(chat_name, interval=0.05)
        pyautogui.press('enter')
        time.sleep(15)
        
        # Smart text selection (works across WhatsApp Web versions)
        pyautogui.click(736, 123)
        pyautogui.dragTo(736, 831, 0.5, button='left')
        pyautogui.hotkey('ctrl', 'c')
        
        return pyperclip.paste().strip() or None
        
    except Exception as e:
        print(f"⚠️ WhatsApp Error: {str(e)[:200]}...")
        return None

# --- AI Response Generation (2025 Best Practices) ---
def generate_response(chat_history):
    """Generates response with modern Gemini features"""
    safety_settings = {
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
    }
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2000,
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            prompt = f"""You are (your name), a 19-year-old student from Karachi, Pakistan. 
            Follow these rules:
            1. Never start with timestamps like [21:02, 12/6/2024]
            2. Respond naturally as a young adult.
            3. Don't type long repies, keep the conservation short. 
            4. No should get any idea that you are an ai.
            5. You are an anime, movies, web series and manga lover.
            6. You like to be sarcastic.
            7. Reply in a funny way and roast people.
            8. Respond briefly in Roman Urdu, keeping replies to one or two lines. Avoid detailed explanations and respond naturally.
            9. Loves to joke.
            10. Don't be harsh and don't hurt other's feelings.
            11. One piece fan.
            12. Love watching football.
            13. Introvert/Extrovert.
            14. Try best to make everyone happy and comfortable.
            15. Love watching memes.
            16. Marvel fan.
            17. Love listening to music specially background score.
            18. Big fan of Taarak Mehta ka oolta chasma.
            19. Not a fan of Indian movies.
            20. Huge fan of animated movies.
            21. Learning programming.
            22. Help others.
            23. Don't just explicitly tell others that you are sarcastic, those things define your character.
            24. You likes to compliment others with things you like.
            25. Always respond based on the user's question with a fun touch.
            26. Never start like this "(your name):"
            
            Chat history:
            {chat_history}"""
            
            response = model.generate_content(
                contents=[{
                    'role': 'user',
                    'parts': [{'text': prompt}]
                }],
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retry {attempt + 1}/{MAX_RETRIES}...")
                time.sleep(2)
            else:
                print(f"❌ Final Error: {str(e)[:200]}...")
                return None

# --- Main Execution Flow ---
if __name__ == "__main__":
    try:
        # Modern input with validation
        while True:
            chat_name = input("💬 Enter WhatsApp chat name: ").strip()
            if chat_name:
                break
            print("⚠️ Please enter a valid name")
        
        # Get chat history
        if not (history := open_whatsapp(chat_name)):
            sys.exit(1)
            
        # Generate and send response
        if response := generate_response(history):
            pyperclip.copy(response)
            pyautogui.click(x=866, y=859)  # Update coordinates as needed
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            print("✅ Response sent successfully!")
        else:
            print("❌ Failed to generate response")
            
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"💥 Critical error: {str(e)[:200]}...")