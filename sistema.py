import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Initialize text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Recognize speech and convert to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please try again.")
            return None
        except sr.RequestError:
            speak("Service is unavailable right now.")
            return None

# Handle user commands
def handle_command(command):
    if "wikipedia" in command:
        speak("What should I search on Wikipedia?")
        query = recognize_speech()
        if query:
            url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
            speak(f"Opening Wikipedia for {query}")
            webbrowser.open(url)

    elif "youtube" in command:
        speak("What should I search on YouTube?")
        query = recognize_speech()
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            speak(f"Opening YouTube for {query}")
            webbrowser.open(url)

    elif "pharmacy" in command or "pharmacy near me" in command:
        speak("Let me find the nearest pharmacy for you.")
        geolocator = Nominatim(user_agent="virtual_assistant")
        location = geolocator.geocode("Your location here")  # Replace with specific address or dynamic user input
        if location:
            pharmacies = [
                ("Pharmacy A", (40.748817, -73.985428)),  # Example coordinates
                ("Pharmacy B", (40.749817, -73.987428)),
            ]
            user_coords = (location.latitude, location.longitude)
            closest_pharmacy = min(pharmacies, key=lambda x: geodesic(user_coords, x[1]).km)
            speak(f"The closest pharmacy is {closest_pharmacy[0]} at a distance of {geodesic(user_coords, closest_pharmacy[1]).km:.2f} kilometers.")

    elif "exit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    while True:
        command = recognize_speech()
        if command:
            handle_command(command)