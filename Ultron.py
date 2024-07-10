import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Convert text to speech and output it."""
    print(f"Man says: {text}")
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    """Capture and process the voice command."""
    try:
        with sr.Microphone() as origin:
            listener.adjust_for_ambient_noise(origin)
            print("Listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            print(f"Raw recognized instruction: {instruction}")  # Debug statement
            instruction = instruction.lower()
            if "man" in instruction:  # Updated to check for "man"
                instruction = instruction.replace('man', '')
                print(f"Processed instruction: {instruction}")  # Debug statement
                return instruction.strip()
            else:
                print("Man not mentioned in the instruction.")
                talk("You need to call me 'Man' for me to respond.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        talk("I didn't catch that. Please repeat.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        talk("There was an error with the speech recognition service.")
    except Exception as e:
        print(f"Exception: {e}")
        talk("I didn't catch that. Please repeat.")
    return ""

def execute_instruction(instruction):
    """Execute the given instruction."""
    if "play" in instruction:
        content = instruction.replace("play", "").strip()
        if "video" in content:
            video = content.replace("video", "").strip()
            talk("playing " + video + " on YouTube")
            pywhatkit.playonyt(video)
        else:
            talk("playing " + content + " on YouTube")
            pywhatkit.playonyt(content)
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + date)
    elif 'how are you' in instruction:
        talk('I am fine, how about you')
    elif 'what is your name' in instruction:
        talk('I am Man, what can I do for you?')  # Updated response
    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        info = wikipedia.summary(human, 1)
        print(info)
        talk(info)
    elif 'exit' in instruction or 'quit' in instruction:
        talk('Goodbye!')
        return False
    else:
        print(f"Instruction not recognized: {instruction}")
        talk('Please repeat')
    return True

def play_man():
    """Main function to run the Man assistant."""
    instruction = input_instruction()
    if instruction:
        print(f"Executing instruction: {instruction}")
        return execute_instruction(instruction)
    return True

while True:
    if not play_man():
        break
