import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

// Create axios instance with base configuration
const api = axios.create({
  baseURL,
  timeout: 10000,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export default api;

// ============== Stock API Functions ==============
export const stockApi = {
  // Get all available stocks
  getStocks: () => api.get("/stocks/"),

  // Search stocks
  searchStocks: (query) => api.get(`/stocks/search?query=${query}`),

  // Get stock details
  getStockDetails: (symbol) => api.get(`/stocks/${symbol}`),

  // Get historical data
  getHistory: (symbol, period = "1mo", interval = "1d") =>
    api.get(`/stocks/${symbol}/history?period=${period}&interval=${interval}`),

  // Get live price
  getLivePrice: (symbol) => api.get(`/stocks/${symbol}/live`),

  // Get technical indicators
  getIndicators: (symbol) => api.get(`/stocks/${symbol}/indicators`),

  // Get market overview
  getMarketOverview: () => api.get("/stocks/market/overview"),

  // Get sector performance
  getSectorPerformance: () => api.get("/stocks/sectors/performance"),
};

// ============== Prediction API Functions ==============
export const predictionApi = {
  // Get prediction for a stock
  getPrediction: (symbol, days = 7) =>
    api.get(`/predictions/${symbol}?days=${days}`),

  // Get detailed prediction
  getDetailedPrediction: (symbol) => api.get(`/predictions/${symbol}/detailed`),

  // Get prediction factors
  getPredictionFactors: (symbol) => api.get(`/predictions/${symbol}/factors`),

  // Get daily signals
  getDailySignals: () => api.get("/predictions/signals/today"),

  // Generate new prediction
  generatePrediction: (symbol) => api.post(`/predictions/${symbol}/generate`),
};

// ============== News API Functions ==============
export const newsApi = {
  // Get latest news
  getLatestNews: (limit = 20) => api.get(`/news/?limit=${limit}`),

  // Get news for a stock
  getStockNews: (symbol) => api.get(`/news/stock/${symbol}`),

  // Get sentiment analysis
  getSentiment: (symbol) => api.get(`/news/sentiment/${symbol}`),

  // Get upcoming events
  getUpcomingEvents: (days = 30) => api.get(`/news/events?days=${days}`),

  // Get event impact analysis
  getEventImpact: (eventType) => api.get(`/news/events/impact/${eventType}`),
};

// ============== Watchlist API Functions ==============
export const watchlistApi = {
  // Get user's watchlist
  getWatchlist: () => api.get("/watchlist/"),

  // Add stock to watchlist
  addStock: (symbol, targetPrice, notes) =>
    api.post(
      `/watchlist/add?symbol=${symbol}&target_price=${targetPrice}&notes=${notes}`,
    ),

  // Remove stock from watchlist
  removeStock: (symbol) => api.delete(`/watchlist/remove/${symbol}`),

  // Update watchlist item
  updateItem: (symbol, data) => api.put(`/watchlist/update/${symbol}`, data),

  // Get alerts
  getAlerts: () => api.get("/watchlist/alerts"),
};
