import os
from dotenv import load_dotenv
from src.data_collection import WeatherDataCollector
from src.data_preprocessing import DataPreprocessor
from src.model_training import WeatherModel

def main():
    # Load environment variables
    load_dotenv()
    
    # 1. Collect Data
    print("Starting data collection...")
    collector = WeatherDataCollector(os.getenv('WEATHER_API_KEY'))
    collector.collect_weather_data(
        cities=["London", "New York", "Tokyo", "Paris", "Sydney"],
        interval_seconds=2,  # 2 seconds interval
        samples_per_city=3   # 3 samples per city
    )
    print("Data collection completed!")
    
    # 2. Preprocess Data
    print("\nStarting data preprocessing...")
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_data(
        input_path='data/raw/raw_data.csv',
        output_path='data/processed/processed_data.csv'
    )
    print("Data preprocessing completed!")
    
    # 3. Train Model
    print("\nStarting model training...")
    model = WeatherModel()
    model.train_model(
        data_path='data/processed/processed_data.csv',
        model_path='models/model.pkl'
    )
    print("Model training completed!")

if __name__ == "__main__":
    main()