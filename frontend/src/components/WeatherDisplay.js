import React from 'react';

const WeatherDisplay = ({ weatherData }) => {
  if (!weatherData) return null;

  return (
    <div className="max-w-md mx-auto mt-6 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Weather Prediction Results</h2>
      <div className="space-y-3">
        <div className="flex justify-between items-center border-b pb-2">
          <span className="text-gray-600">Temperature</span>
          <span className="font-medium">{weatherData.temperature}°C</span>
        </div>
        <div className="flex justify-between items-center border-b pb-2">
          <span className="text-gray-600">Humidity</span>
          <span className="font-medium">{weatherData.humidity}%</span>
        </div>
        <div className="flex justify-between items-center border-b pb-2">
          <span className="text-gray-600">Wind Speed</span>
          <span className="font-medium">{weatherData.wind_speed} m/s</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Condition</span>
          <span className="font-medium">{weatherData.weather_condition}</span>
        </div>
      </div>
    </div>
  );
};

export default WeatherDisplay;