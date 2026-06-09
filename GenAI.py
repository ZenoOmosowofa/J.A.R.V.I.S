"""
==============================================================================
JARVIS AI ENGINE - GROQ API INTEGRATION MODULE
==============================================================================

DESCRIPTION:
    Handles AI-powered conversations and weather queries for JARVIS.
    Uses Groq's LLaMA 3.3-70b model for intelligent responses with
    optional real-time weather integration.

INSTALLATION REQUIREMENTS:
    Run these commands in your terminal:
    
    pip install groq
    pip install requests
    
    Or install both at once:
    pip install groq requests

DEPENDENCIES:
    - groq: Fast AI inference API for LLaMA models
    - requests: HTTP library for weather API calls
    - re: Regular expressions for parsing city names
    - datetime: Current date/time information

ENVIRONMENT VARIABLES:
    - GROQ_API_KEY: Set your Groq API key here
    - OPENWEATHER_API_KEY: Set your OpenWeather API key (weather.get_weather only)

USAGE:
    from genAI import ask_jarvis, get_weather
    
    response = ask_jarvis("What is the weather like?")
    print(response)
    
    weather = get_weather("London")
    print(weather)

FEATURES:
    - Groq LLaMA 3.3 70B model for responses
    - Real-time weather data integration
    - City extraction from natural language
    - Current date/time context in responses
    - British gentleman personality and tone
==============================================================================
Other options:
    - Use a different AI model or API (e.g., OpenAI, Azure, Amazon Polly)
    - Implement custom voice models with Tacotron2 or WaveNet   
    - Add more complex command parsing and execution (e.g., smart home control)
    - Integrate with external APIs for news, calendar, etc.
    - Use a more advanced TTS engine for higher quality voices (e.g., ElevenLabs)
    - Implement a more sophisticated UI with additional status indicators and controls
    - Add error handling and fallback responses for better user experience
    - Use a hotword detection library (e.g., Snowboy) for more efficient wake word recognition
    - Implement multi-language support for both recognition and synthesis
==============================================================================
"""

import re
from datetime import datetime
from groq import Groq
import requests  # For making HTTP requests to weather API

# Initialize Groq client with API authentication
client = Groq(api_key="")


def get_weather(city="San Antonio"):
    """
    Fetch current weather for a specified city using OpenWeatherMap API.
    
    Args:
        city (str): City name (default: "San Antonio")
    
    Returns:
        str: Weather information "temp°F with description" or None if failed
    """
    # OpenWeatherMap API credentials and endpoint
    api_key = "OpenWeather A.P.I"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    try:
        # Fetch weather data from API
        data = requests.get(url).json()
        # Check if API response was successful (code 200 means success)
        if data.get('cod') != 200:
            return None
        # Extract temperature and weather description from response
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"{temp}°F with {desc}"
    except:
        # Return None if any error occurs (network error, invalid city, etc.)
        return None
    

def extract_city(text):
    """
    Extract city name from user text using regex pattern matching.
    Looks for patterns like "in London" or "in Paris, France"
    
    Args:
        text (str): User input text
    
    Returns:
        str: Extracted city name or default "San Antonio"
    """
    # Regex pattern: looks for "in [city]" or "in [city], [state]"
    match = re.search(r'\bin\s+([A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Return default city if pattern not found
    return "San Antonio"
    

def ask_jarvis(text):
    """
    Send a user query to JARVIS AI and get a response from Groq's LLaMA model.
    Includes current time and date context in the system prompt.
    
    Args:
        text (str): User's question or command
    
    Returns:
        str: JARVIS's response
    """
    # Get current time and date for context in responses
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    # Send request to Groq API with system prompt and user message
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Use LLaMA 3.3 70B model
        messages=[
            {
                "role": "system", 
                "content": f"You are JARVIS, a highly intelligent AI assistant. You are formal, \
             precise, and occasionally witty in a dry British manner. \
             Always address the user as 'sir'. Keep responses concise. \
             The current time is {current_time} and today is {current_date}."
            },
            {"role": "user", "content": text}
        ]
    )
    # Extract and return the AI's response text
    result = response.choices[0].message.content
    return result
