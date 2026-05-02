"""
Fetch current weather for Tokyo using wttr.in API.
"""

import requests
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_tokyo_weather():
    """Fetch and display current weather for Tokyo."""
    try:
        # wttr.in API endpoint for Tokyo
        url = "https://wttr.in/Tokyo?format=3"
        
        print("Fetching weather for Tokyo...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Print the weather
        print("\n" + "="*50)
        print("TOKYO WEATHER")
        print("="*50)
        print(response.text.strip())
        print("="*50 + "\n")
        
        # Get more detailed weather
        url_detailed = "https://wttr.in/Tokyo?format=%l:+%C+%t+%h+%w"
        response_detailed = requests.get(url_detailed, timeout=10)
        
        if response_detailed.status_code == 200:
            print("Detailed Information:")
            print(response_detailed.text.strip())
            print()
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    get_tokyo_weather()

# Made with Bob
