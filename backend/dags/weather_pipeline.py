from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_mlops_pipeline',
    default_args=default_args,
    description='Weather data MLOps pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def collect_weather_data():
    from src.data_collection import WeatherDataCollector
    load_dotenv()
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise ValueError("No API key found!")
    collector = WeatherDataCollector(api_key)
    collector.collect_weather_data()
    print("Weather data collection completed")

def preprocess_data():
    from src.data_preprocessing import DataPreprocessor
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_data(
        input_path='/opt/airflow/data/raw/raw_data.csv',
        output_path='/opt/airflow/data/processed/processed_data.csv'
    )
    print("Data preprocessing completed")

def train_model():
    from src.model_training import WeatherModel
    model = WeatherModel()
    model.train_model(
        data_path='/opt/airflow/data/processed/processed_data.csv',
        model_path='/opt/airflow/models/model.pkl'
    )
    print("Model training completed")

# Define tasks
collect_task = PythonOperator(
    task_id='collect_weather_data',
    python_callable=collect_weather_data,
    dag=dag
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

# Set task dependencies
collect_task >> preprocess_task >> train_task