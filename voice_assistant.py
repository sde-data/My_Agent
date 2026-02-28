import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# ---------------- SETTINGS ----------------
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

conversation_history = []

# ---------------- SPEAK ----------------
def speak(text):
    print("\nAI:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
def listen():
    try:
        print("Using PulseAudio device...")
        with sr.Microphone(device_index=5) as source:  # pulse
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source)

        print("Recognizing...")
        command = recognizer.recognize_google(audio, language="en-IN")
        print("You said:", command)
        return command.lower()

    except Exception as e:
        print("Error:", e)
        return ""

# ---------------- CHATGPT ----------------
def chat_with_gpt(user_input):
    global conversation_history

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})

    return reply

# ---------------- MAIN ----------------
def main():
    speak("Hello Suresh. Chat GPT voice assistant is ready.")

    while True:
        user_input = listen()

        if user_input == "":
            continue

        if "exit" in user_input or "stop" in user_input:
            speak("Goodbye Suresh")
            break

        reply = chat_with_gpt(user_input)
        speak(reply)

if __name__ == "__main__":
    main()