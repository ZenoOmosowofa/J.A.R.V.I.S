"""
==============================================================================
JARVIS - AI VOICE ASSISTANT MAIN MODULE
==============================================================================

DESCRIPTION:
    Main entry point for JARVIS voice assistant. Handles voice recognition,
    AI conversation, and voice synthesis in a continuous listening loop.
    
INSTALLATION REQUIREMENTS:
    Run these commands in your terminal to install all dependencies:
    
    pip install SpeechRecognition
    pip install gtts
    pip install pygame
    pip install groq
    pip install requests
    
    Or install all at once:
    pip install SpeechRecognition gtts pygame groq requests

DEPENDENCIES:
    - SpeechRecognition: Google Speech-to-Text recognition
    - speech_recognition (sr): Audio capture and recognition engine
    - groq: AI API for intelligent responses (genAI.py)
    - gtts/pygame: Text-to-Speech and audio playback (voice.py)
    - ui: Custom UI module for status display
    - threading: Parallel execution of UI and voice processing

USAGE:
    python Jarvis.py
    
    The program will:
    1. Start the UI interface
    2. Listen continuously for the wake word "Jarvis"
    3. Once activated, process voice commands
    4. Respond with AI-generated answers
    5. Exit when user says "that is all", "goodbye", "shut down", or "exit"

WAKE WORDS & STOP PHRASES:
    Wake word: "jarvis"
    Stop phrases: "that is all", "goodbye", "shut down", "exit"
==============================================================================
Other options:
    - Use a different AI model or API (e.g., OpenAI, Azure, Amazon Polly)
    - Implement custom voice models with Tacotron2 or WaveNet   
    - Add more complex command parsing and execution (e.g., smart home control)
    - Integrate with external APIs for weather, news, calendar, etc.
    - Use a more advanced TTS engine for higher quality voices (e.g., ElevenLabs)
    - Implement a more sophisticated UI with additional status indicators and controls
    - Add error handling and fallback responses for better user experience
    - Use a hotword detection library (e.g., Snowboy) for more efficient wake word recognition
    - Implement multi-language support for both recognition and synthesis
==============================================================================
"""

# Import threading for parallel UI execution
import threading
# Import UI components for status display (speaking, listening indicators)
from ui import launch_ui, set_speaking, set_listening
# Import speech recognition library for microphone input
import speech_recognition as sr
# Import time utilities for delays
import time
# Import custom AI response function from genAI module
from genAI import ask_jarvis
# Import custom voice synthesis function from voice module
from voice import speak

# Initialize speech recognizer with optimal settings for voice commands
r = sr.Recognizer()
r.energy_threshold = 300  # Adjust sensitivity to ambient noise
r.dynamic_energy_threshold = False  # Keep threshold consistent
r.pause_threshold = 0.6  # Pause duration before considering speech complete
mic = sr.Microphone()

# Calibrate microphone for ambient noise at startup
with mic as source:
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=0.6)

# Start UI interface in background thread
threading.Thread(target=launch_ui, daemon=True).start()
print("Listening for 'Jarvis'...")

# Main continuous listening loop - always listening for wake word
while True:
    try:
        # Listen for audio from microphone (max 10 seconds, 8 second phrase limit)
        with mic as source:
            audio = r.listen(source, timeout=10, phrase_time_limit=8)

        # Convert audio to text using Google Speech Recognition API
        text = r.recognize_google(audio).lower().strip()
        print(f"Heard: {text}")

        # Check if wake word "jarvis" is mentioned in the recognized text
        if "jarvis" in text:
        # Jarvis was activated - respond and enter command processing loop
            if "jarvis" in text:
            # Indicate that Jarvis is speaking on UI
             set_speaking(True)
            # Greet the user with initial response
            speak("What can I do for you, sir?")
            set_speaking(False)

            # Inner loop for follow-up commands after activation
            while True:
                try:
                    # Update UI to show listening state
                    set_listening(True)
                    with mic as source:
                        print("Listening for command...")
                        # Listen for command (7 second timeout, 11 second phrase limit)
                        audio = r.listen(source, timeout=7, phrase_time_limit=11)
                    set_listening(False)

                    # Recognize spoken command
                    text = r.recognize_google(audio).lower().strip()

                    # Check if user said a stop phrase to exit
                    if any(phrase in text for phrase in ["that is all", "goodbye", "shut down", "exit"]):
                        # Say goodbye and shutdown
                        set_speaking(True)
                        speak("Goodbye sir, have a good day.")
                        set_speaking(False)
                        print("Shutting down...")
                        exit()

                    # Send user command to AI and get response
                    response = ask_jarvis(text)
                    print(f"Jarvis: {response}")
                    # Speak the AI response to the user
                    set_speaking(True)
                    speak(response)
                    set_speaking(False)

                # Handle timeout (no speech detected)
                except sr.WaitTimeoutError:
                    pass
                # Handle unrecognized speech
                except sr.UnknownValueError:
                    pass
                # Handle any other errors
                except Exception as e:
                    print(f"Error: {e}")

    # Handle timeout in main loop (no speech detected in waiting period)
    except sr.WaitTimeoutError:
        pass
    # Handle unrecognized speech in main loop
    except sr.UnknownValueError:
        pass
    # Handle any other errors in main loop
    except Exception as e:
        print(f"Error: {e}")
