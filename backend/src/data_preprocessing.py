import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def validate_data(self, df, stage=""):
        """Validate data and print statistics"""
        print(f"\n{stage} Data Statistics:")
        print(f"Shape: {df.shape}")
        print("\nNumerical columns statistics:")
        print(df.describe())
        
        # Check for constant columns
        constant_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                        if df[col].nunique() == 1]
        if constant_cols:
            print(f"\nWarning: These columns have constant values: {constant_cols}")
            
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"\nWarning: Found {duplicates} duplicate rows")
    
    def preprocess_data(self, input_path, output_path):
        """Preprocess weather data with validation checks"""
        # Read data
        print(f"Reading data from: {input_path}")
        df = pd.read_csv(input_path)
        
        # Validate input data
        self.validate_data(df, "Input")
        
        # Remove duplicate rows
        df = df.drop_duplicates()
        print(f"\nShape after removing duplicates: {df.shape}")
        
        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))
        
        # Only normalize if there's variance in the data
        numerical_cols = ['temperature', 'humidity', 'wind_speed']
        
        for col in numerical_cols:
            if df[col].std() == 0:
                print(f"\nWarning: Column '{col}' has no variance. Skipping normalization.")
            else:
                # Normalize only columns with variance
                df[col] = self.scaler.fit_transform(df[[col]])
        
        # Validate output data
        self.validate_data(df, "Output")
        
        # Save preprocessed data
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nPreprocessed data saved to: {output_path}")
        
        return df

def main():
    try:
        preprocessor = DataPreprocessor()
        preprocessor.preprocess_data(
            input_path='data/raw/raw_data.csv',
            output_path='data/processed/processed_data.csv'
        )
    except Exception as e:
        print(f"Error in preprocessing: {str(e)}")
        raise e

if __name__ == "__main__":
    main()