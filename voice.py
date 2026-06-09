"""
==============================================================================
VOICE SYNTHESIS MODULE - JARVIS Text-to-Speech
==============================================================================

DESCRIPTION:
    Converts text to speech using Google Text-to-Speech (gTTS) with British
    English pronunciation and plays it through the system audio using pygame.

INSTALLATION REQUIREMENTS:
    Run these commands in your terminal to install dependencies:
    
    pip install gtts
    pip install pygame
    
    Or install both at once:
    pip install gtts pygame

DEPENDENCIES:
    - gtts: Google Text-to-Speech conversion library
    - pygame: Audio playback and mixing engine

USAGE:
    from Voice import speak
    
    speak("Hello, this is JARVIS speaking")
    speak("The temperature is 72°F")  # Temperature symbols are handled automatically

FEATURES:
    - Converts °F and °C symbols to readable text for natural speech
    - Uses British English accent (co.uk)
    - Streams audio directly to memory (no disk writes)
    - Waits for playback to complete before returning
==============================================================================

Other Options:
    - pyttsx3: Offline TTS engine, but less natural voices
    - gTTS with different accents (e.g., 'en-us' for American English)
    - Amazon Polly or Microsoft Azure TTS for higher quality but require API keys
    - ElevenLabs API for ultra-realistic voices (also requires API key) 
    - Custom voice models using Tacotron2 or WaveNet (complex to set up)
    - Festival TTS (open-source, but less natural sounding)
    - ResponsiveVoice (web-based, requires internet connection)
"""

import io
import pygame
from gtts import gTTS

def speak(text):
    """
    Converts text to speech using Google Text-to-Speech (gTTS) and plays it.
    Handles temperature symbols by converting them to readable text.
    
    Args:
        text (str): The text to convert to speech
    """
    # Replace temperature symbols with readable text for natural speech
    text = text.replace("°F", " degrees Fahrenheit")
    text = text.replace("°C", " degrees Celsius")
    
    # Generate speech audio from text using Google Text-to-Speech (British English)
    tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
    
    # Write audio to a BytesIO buffer (in-memory file) instead of saving to disk
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)  # Reset file pointer to the beginning for reading

    # Initialize pygame mixer and load the audio file
    pygame.mixer.init(frequency=25000)
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing before returning
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Check playback status 10 times per second
