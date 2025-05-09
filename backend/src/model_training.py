import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import time
import matplotlib.pyplot as plt
import seaborn as sns

class WeatherModel:
    def __init__(self, experiment_name="weather_prediction"):
        """Initialize the model with MLflow experiment tracking."""
        self.model = LinearRegression()
        mlflow.set_experiment(experiment_name)
        self.experiment = mlflow.get_experiment_by_name(experiment_name)

    def create_evaluation_plots(self, y_true, y_pred, X_test):
        """Create and save evaluation plots for MLflow artifacts."""
        # Residual plot
        plt.figure(figsize=(10, 6))
        plt.scatter(y_pred, y_true - y_pred)
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.savefig('residual_plot.png')
        plt.close()

        # Feature importance plot
        plt.figure(figsize=(8, 6))
        feature_importance = pd.DataFrame({
            'feature': X_test.columns,
            'importance': np.abs(self.model.coef_)
        })
        sns.barplot(data=feature_importance, x='importance', y='feature')
        plt.title('Feature Importance')
        plt.savefig('feature_importance.png')
        plt.close()

    def log_model_explanation(self, X):
        """Log model coefficients and intercept explanation."""
        explanation = "Model Coefficients Explanation:\n\n"
        for feature, coef in zip(X.columns, self.model.coef_):
            explanation += f"{feature}: {coef:.4f} - For each unit increase in {feature}, "
            explanation += f"temperature changes by {coef:.4f} units\n"
        explanation += f"\nIntercept: {self.model.intercept_:.4f}"
        
        with open("model_explanation.txt", "w") as f:
            f.write(explanation)

    def train_model(self, data_path, model_path, test_size=0.2):
        """Train the weather prediction model with enhanced MLflow tracking."""
        with mlflow.start_run() as run:
            print(f"MLflow Run ID: {run.info.run_id}")
            
            # Load and validate data
            df = pd.read_csv(data_path)
            if df.isnull().sum().any():
                raise ValueError("Dataset contains missing values")

            # Split features and target
            X = df[['humidity', 'wind_speed']]
            y = df['temperature']
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )

            # Train model and measure time
            start_time = time.time()
            self.model.fit(X_train, y_train)
            training_duration = time.time() - start_time

            # Generate predictions
            y_pred_train = self.model.predict(X_train)
            y_pred_test = self.model.predict(X_test)

            # Calculate metrics
            metrics = {
                'training_mse': mean_squared_error(y_train, y_pred_train),
                'test_mse': mean_squared_error(y_test, y_pred_test),
                'training_r2': r2_score(y_train, y_pred_train),
                'test_r2': r2_score(y_test, y_pred_test),
                'training_mae': mean_absolute_error(y_train, y_pred_train),
                'test_mae': mean_absolute_error(y_test, y_pred_test),
                'training_duration': training_duration
            }

            # Log parameters
            mlflow.log_params({
                'model_type': 'LinearRegression',
                'features': X.columns.tolist(),
                'test_size': test_size
            })

            # Log metrics
            mlflow.log_metrics(metrics)

            # Create and log visualization artifacts
            self.create_evaluation_plots(y_test, y_pred_test, X_test)
            mlflow.log_artifact('residual_plot.png')
            mlflow.log_artifact('feature_importance.png')

            # Log model explanation
            self.log_model_explanation(X)
            mlflow.log_artifact('model_explanation.txt')

            # Save and log model
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)

            # Log model with signature
            signature = infer_signature(X_train, y_pred_train)
            mlflow.sklearn.log_model(
                self.model,
                "weather_model",
                signature=signature,
                input_example=X_train.iloc[0].to_dict()
            )

            print(f"""
Training completed successfully:
- Training R² score: {metrics['training_r2']:.4f}
- Test R² score: {metrics['test_r2']:.4f}
- Training MSE: {metrics['training_mse']:.4f}
- Test MSE: {metrics['test_mse']:.4f}
- Training Duration: {metrics['training_duration']:.2f} seconds
""")

def main():
    try:
        model = WeatherModel(experiment_name="weather_prediction_v2")
        model.train_model(
            data_path='data/processed/processed_data.csv',
            model_path='models/model.pkl'
        )
    except Exception as e:
        print(f"Error in model training: {str(e)}")
        raise e

if __name__ == "__main__":
    main()