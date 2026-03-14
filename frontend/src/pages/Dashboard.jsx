import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  TrendingUp,
  TrendingDown,
  ArrowRight,
  BarChart3,
  Activity,
  Zap,
} from "lucide-react";
import { stockApi, predictionApi, newsApi } from "../services/api";
import StockCard from "../components/stocks/StockCard";
import PredictionCard from "../components/predictions/PredictionCard";
import NewsCard from "../components/news/NewsCard";

// Popular stocks to display
const POPULAR_STOCKS = [
  { symbol: "RELIANCE.NS", name: "Reliance Industries" },
  { symbol: "TCS.NS", name: "Tata Consultancy Services" },
  { symbol: "INFY.NS", name: "Infosys" },
  { symbol: "HDFCBANK.NS", name: "HDFC Bank" },
  { symbol: "ICICIBANK.NS", name: "ICICI Bank" },
  { symbol: "SBIN.NS", name: "State Bank of India" },
];

export default function Dashboard() {
  const [stocks, setStocks] = useState([]);
  const [signals, setSignals] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch data in parallel
      const [stocksRes, signalsRes, newsRes] = await Promise.all([
        stockApi.getStocks().catch(() => ({ data: POPULAR_STOCKS })),
        predictionApi.getDailySignals().catch(() => ({ data: [] })),
        newsApi.getLatestNews(5).catch(() => ({ data: [] })),
      ]);

      setStocks(stocksRes.data?.slice(0, 6) || POPULAR_STOCKS);
      setSignals(signalsRes.data || []);
      setNews(newsRes.data || []);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  // Simulated market data (replace with actual API data)
  const marketData = {
    nifty50: { value: 22147.5, change: 0.82 },
    sensex: { value: 72831.94, change: 0.76 },
  };

  return (
    <div className="mt-16 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">
            Welcome to Stock Saarthi - Your AI investment guide
          </p>
        </div>
        <Link to="/predictions" className="btn-primary flex items-center gap-2">
          <Zap className="w-4 h-4" />
          View AI Predictions
        </Link>
      </div>

      {/* Market Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Nifty 50 */}
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">NIFTY 50</p>
              <p className="text-2xl font-bold mt-1">
                {marketData.nifty50.value.toLocaleString()}
              </p>
            </div>
            <div
              className={`flex items-center gap-1 ${marketData.nifty50.change >= 0 ? "text-profit" : "text-loss"}`}
            >
              {marketData.nifty50.change >= 0 ? (
                <TrendingUp className="w-5 h-5" />
              ) : (
                <TrendingDown className="w-5 h-5" />
              )}
              <span className="font-medium">
                {marketData.nifty50.change >= 0 ? "+" : ""}
                {marketData.nifty50.change}%
              </span>
            </div>
          </div>
        </div>

        {/* Sensex */}
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">SENSEX</p>
              <p className="text-2xl font-bold mt-1">
                {marketData.sensex.value.toLocaleString()}
              </p>
            </div>
            <div
              className={`flex items-center gap-1 ${marketData.sensex.change >= 0 ? "text-profit" : "text-loss"}`}
            >
              {marketData.sensex.change >= 0 ? (
                <TrendingUp className="w-5 h-5" />
              ) : (
                <TrendingDown className="w-5 h-5" />
              )}
              <span className="font-medium">
                {marketData.sensex.change >= 0 ? "+" : ""}
                {marketData.sensex.change}%
              </span>
            </div>
          </div>
        </div>

        {/* AI Signals */}
        <div className="card bg-gradient-to-br from-primary-500 to-primary-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100 text-sm">AI Signals Today</p>
              <p className="text-2xl font-bold mt-1">{signals.length}</p>
            </div>
            <Activity className="w-8 h-8 text-primary-200" />
          </div>
        </div>

        {/* Accuracy */}
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Model Accuracy</p>
              <p className="text-2xl font-bold mt-1">78.5%</p>
            </div>
            <BarChart3 className="w-8 h-8 text-success-500" />
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Popular Stocks */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Popular Stocks</h2>
              <Link
                to="/stocks"
                className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1"
              >
                View All <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {loading ? (
              <div className="space-y-3">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className="h-16 bg-gray-100 rounded-lg animate-pulse"
                  />
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                {stocks.map((stock) => (
                  <StockCard key={stock.symbol} stock={stock} />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* AI Predictions Sidebar */}
        <div className="space-y-6">
          {/* Today's Signals */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-500" />
                AI Signals
              </h2>
            </div>

            {signals.length > 0 ? (
              <div className="space-y-3">
                {signals.slice(0, 5).map((signal) => (
                  <PredictionCard
                    key={signal.symbol}
                    prediction={signal}
                    compact
                  />
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">
                No signals yet. Check back later!
              </p>
            )}
          </div>

          {/* Latest News */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Latest News</h2>
              <Link
                to="/news"
                className="text-primary-600 hover:text-primary-700 text-sm"
              >
                More
              </Link>
            </div>

            {news.length > 0 ? (
              <div className="space-y-3">
                {news.slice(0, 3).map((item, index) => (
                  <NewsCard key={index} news={item} compact />
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Loading news...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
