// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // ✅ your base URL
  headers: {
    'Content-Type': 'application/json',
    // Add any default headers if needed
  },
  // You can also set timeout, auth, etc. here
  timeout: 5000,
});

export default api;
