import os
import requests
import pandas as pd
from datetime import datetime
import time
from dotenv import load_dotenv

class WeatherDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def collect_weather_data(self, cities=None, interval_seconds=2, samples_per_city=3):
        """
        Collect weather data with shorter wait times between requests
        
        Args:
            cities (list): List of cities to collect data from
            interval_seconds (int): Seconds to wait between collections
            samples_per_city (int): Number of samples to collect per city
        """
        if cities is None:
            cities = ["London", "New York", "Tokyo", "Paris", "Sydney"]
            
        data_list = []
        
        print(f"Starting data collection for {len(cities)} cities...")
        
        for city in cities:
            print(f"\nCollecting data for {city}...")
            
            for i in range(samples_per_city):
                params = {
                    'q': city,
                    'appid': self.api_key,
                    'units': 'metric'
                }
                
                try:
                    response = requests.get(self.base_url, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    weather_data = {
                        'city': city,
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'weather_condition': data['weather'][0]['main'],
                        'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    data_list.append(weather_data)
                    print(f"Sample {i+1}/{samples_per_city} collected for {city}")
                    
                    # Don't wait after the last sample of the last city
                    if not (city == cities[-1] and i == samples_per_city - 1):
                        print(f"Waiting {interval_seconds} seconds before next collection...")
                        time.sleep(interval_seconds)
                        
                except requests.exceptions.RequestException as e:
                    print(f"Error collecting data for {city}: {str(e)}")
                    continue
        
        df = pd.DataFrame(data_list)
        os.makedirs('data/raw', exist_ok=True)
        output_path = 'data/raw/raw_data.csv'
        df.to_csv(output_path, index=False)
        
        print("\nData collection completed!")
        print(f"Total samples collected: {len(df)}")
        print(f"Data saved to: {output_path}")
        
        return df

def main():
    load_dotenv()
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set WEATHER_API_KEY in .env file")
    
    collector = WeatherDataCollector(api_key)
    collector.collect_weather_data(interval_seconds=2)

if __name__ == "__main__":
    main()