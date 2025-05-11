import React, { useState } from 'react';

const WeatherForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    humidity: '',
    wind_speed: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      humidity: parseFloat(formData.humidity),
      wind_speed: parseFloat(formData.wind_speed)
    });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Weather Prediction</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="humidity" className="block text-sm font-medium text-gray-700">
            Humidity (%)
          </label>
          <input
            type="number"
            id="humidity"
            name="humidity"
            min="0"
            max="100"
            value={formData.humidity}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm 
                     focus:border-blue-500 focus:ring-blue-500"
            placeholder="Enter humidity percentage"
            required
          />
        </div>
        <div>
          <label htmlFor="wind_speed" className="block text-sm font-medium text-gray-700">
            Wind Speed (m/s)
          </label>
          <input
            type="number"
            id="wind_speed"
            name="wind_speed"
            min="0"
            step="0.01"
            value={formData.wind_speed}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm 
                     focus:border-blue-500 focus:ring-blue-500"
            placeholder="Enter wind speed"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full flex justify-center py-2 px-4 border border-transparent 
                   rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 
                   hover:bg-blue-700 focus:outline-none focus:ring-2 
                   focus:ring-offset-2 focus:ring-blue-500"
        >
          Get Temperature Prediction
        </button>
      </form>
    </div>
  );
};

export default WeatherForm;