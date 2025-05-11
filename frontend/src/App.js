import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Login from './components/Login';
import Register from './components/Register';
import WeatherForm from './components/WeatherForm';
import WeatherDisplay from './components/WeatherDisplay';

function App() {
  const [weatherData, setWeatherData] = useState(null);
  const [error, setError] = useState(null);

  const handleWeatherSubmit = async (formData) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Please login first');
        return;
      }

      const response = await fetch('http://localhost:5000/api/weather/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get prediction');
      }

      const data = await response.json();
      setWeatherData(data);
      setError(null);
    } catch (error) {
      console.error('Error fetching weather data:', error);
      setError(error.message);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <NavBar />
        <div className="container mx-auto px-4 py-8">
          {error && (
            <div className="max-w-md mx-auto mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={
              <>
                <WeatherForm onSubmit={handleWeatherSubmit} />
                {weatherData && <WeatherDisplay weatherData={weatherData} />}
              </>
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;