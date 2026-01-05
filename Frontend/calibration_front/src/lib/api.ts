import axios from 'axios';

// Use VITE_API_BASE_URL environment variable for production deployment
// Falls back to production URL if environment variable is not set
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://sensorcalibrationplatform.onrender.com';

// Validate that we have a proper API URL in production
if (import.meta.env.PROD && !import.meta.env.VITE_API_BASE_URL) {
  console.warn('Production warning: VITE_API_BASE_URL not set. Using default production URL.');
}

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Log API configuration in development for debugging
if (import.meta.env.DEV) {
  console.log('API Base URL:', API_BASE_URL);
}

export default API_BASE_URL;

