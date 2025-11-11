import speech_recognition as sr
import pyttsx3
import wikipedia
import re
from sympy import sympify
from datetime import datetime

recognizer = sr.Recognizer()

def speak(text):
    """Force speech each time"""
    print("Assistant:", text)
    try:
        engine = pyttsx3.init()  # reinitialize every call
        voices = engine.getProperty("voices")
        if voices:  # pick first available voice
            engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()  # flush engine
    except Exception as e:
        print("[TTS ERROR]", e)

def simple_answer(question):
    q = question.lower().strip()

    # Date and Time
    if "time" in q:
        return f"The time is {datetime.now().strftime('%H:%M %p')}"
    if "date" in q:
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}"

    # Predefined
    short_answers = {
        "what is the capital of india": "The capital of India is New Delhi.",
        "who is the prime minister of india": "The Prime Minister of India is Narendra Modi.",
        "what color is the sky": "The sky is usually blue during the day and dark at night.",
        "who are you": "I am your AI voice assistant.",
        "how are you": "I am doing great, thank you!",
        "what is your name": "You can call me your assistant."
    }
    if q in short_answers:
        return short_answers[q]

    # Math (sympy)
    try:
        expr = sympify(q)
        return f"The answer is {expr.evalf()}"
    except:
        pass

    # Math regex
    match = re.search(r'(\d+)\s*(\+|plus|\-|minus|\*|x|times|/|divided by)\s*(\d+)', q)
    if match:
        a, op, b = match.groups()
        a, b = float(a), float(b)
        if op in ["+", "plus"]:
            return f"The answer is {a+b}"
        elif op in ["-", "minus"]:
            return f"The answer is {a-b}"
        elif op in ["*", "x", "times"]:
            return f"The answer is {a*b}"
        elif op in ["/", "divided by"]:
            return f"The answer is {a/b}"

    # Wikipedia fallback
    try:
        return wikipedia.summary(q, sentences=2)
    except:
        return "Sorry, I don't know that yet."

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("\n🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return None

def main():
    speak("Hello, I am your assistant. Ask me anything.")
    while True:
        query = listen()

        if not query:
            speak("I didn't catch that, please say again.")
            continue

        if any(word in query for word in ["bye", "exit", "quit"]):
            speak("Goodbye! Have a great day.")
            break

        answer = simple_answer(query)
        speak(answer)

if __name__ == "__main__":
    main()




































