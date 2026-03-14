import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  TrendingUp,
  TrendingDown,
  Star,
  Info,
  BarChart3,
  Activity,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";
import { stockApi, predictionApi, newsApi } from "../services/api";

export default function StockAnalysis() {
  const { symbol } = useParams();
  const [stock, setStock] = useState(null);
  const [history, setHistory] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [indicators, setIndicators] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState("1mo");

  useEffect(() => {
    if (symbol) {
      fetchStockData();
    }
  }, [symbol, period]);

  const fetchStockData = async () => {
    setLoading(true);
    try {
      const [stockRes, historyRes, predictionRes, indicatorsRes, sentimentRes] =
        await Promise.allSettled([
          stockApi.getStockDetails(symbol),
          stockApi.getHistory(symbol, period),
          predictionApi.getDetailedPrediction(symbol),
          stockApi.getIndicators(symbol),
          newsApi.getSentiment(symbol),
        ]);

      setStock(stockRes.status === "fulfilled" ? stockRes.value.data : null);
      setHistory(
        historyRes.status === "fulfilled"
          ? (historyRes.value.data?.data ?? [])
          : [],
      );
      setPrediction(
        predictionRes.status === "fulfilled" ? predictionRes.value.data : null,
      );
      setIndicators(
        indicatorsRes.status === "fulfilled" ? indicatorsRes.value.data : null,
      );
      setSentiment(
        sentimentRes.status === "fulfilled" ? sentimentRes.value.data : null,
      );
    } catch (error) {
      console.error("Error fetching stock data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="mt-16 space-y-6">
        <div className="h-8 w-64 bg-gray-200 rounded animate-pulse" />
        <div className="h-96 bg-gray-200 rounded-xl animate-pulse" />
      </div>
    );
  }

  const currentPrice =
    stock?.current_price ||
    indicators?.current_price ||
    prediction?.current_price ||
    0;
  const previousClose = stock?.previous_close || currentPrice;
  const priceChange =
    previousClose > 0
      ? ((currentPrice - previousClose) / previousClose) * 100
      : 0;

  return (
    <div className="mt-16 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-gray-900">
              {stock?.name || symbol}
            </h1>
            <span className="text-gray-500">{symbol}</span>
          </div>
          <div className="flex items-center gap-4 mt-2">
            <span className="text-3xl font-bold">
              ₹{currentPrice.toLocaleString()}
            </span>
            <span
              className={`flex items-center gap-1 font-medium ${priceChange >= 0 ? "text-profit" : "text-loss"}`}
            >
              {priceChange >= 0 ? (
                <TrendingUp className="w-5 h-5" />
              ) : (
                <TrendingDown className="w-5 h-5" />
              )}
              {priceChange >= 0 ? "+" : ""}
              {priceChange.toFixed(2)}%
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button className="btn-secondary flex items-center gap-2">
            <Star className="w-4 h-4" />
            Add to Watchlist
          </button>
        </div>
      </div>

      {/* AI Prediction Banner */}
      {prediction && (
        <div
          className={`card ${
            prediction.signal === "BUY"
              ? "bg-green-50 border-green-200"
              : prediction.signal === "SELL"
                ? "bg-red-50 border-red-200"
                : "bg-yellow-50 border-yellow-200"
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div
                className={`w-12 h-12 rounded-full flex items-center justify-center ${
                  prediction.signal === "BUY"
                    ? "bg-green-500"
                    : prediction.signal === "SELL"
                      ? "bg-red-500"
                      : "bg-yellow-500"
                }`}
              >
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-sm text-gray-600">AI Recommendation</p>
                <p
                  className={`text-xl font-bold ${
                    prediction.signal === "BUY"
                      ? "text-green-700"
                      : prediction.signal === "SELL"
                        ? "text-red-700"
                        : "text-yellow-700"
                  }`}
                >
                  {prediction.signal}
                </p>
              </div>
            </div>

            <div className="text-right">
              <p className="text-sm text-gray-600">Target Price</p>
              <p className="text-xl font-bold">
                ₹{prediction.predicted_price?.toLocaleString()}
              </p>
              <p
                className={`text-sm ${prediction.price_change_percent >= 0 ? "text-profit" : "text-loss"}`}
              >
                {prediction.price_change_percent >= 0 ? "+" : ""}
                {prediction.price_change_percent?.toFixed(2)}%
              </p>
            </div>

            <div className="text-right">
              <p className="text-sm text-gray-600">Confidence</p>
              <p className="text-xl font-bold">
                {(prediction.confidence * 100).toFixed(0)}%
              </p>
            </div>
          </div>

          {prediction.explanation && (
            <p className="mt-4 text-sm text-gray-700 border-t pt-3">
              <Info className="w-4 h-4 inline mr-1" />
              {prediction.explanation}
            </p>
          )}
        </div>
      )}

      {/* Chart & Info Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Price Chart */}
        <div className="lg:col-span-2 card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Price Chart</h2>
            <div className="flex gap-2">
              {["1d", "5d", "1mo", "3mo", "6mo", "1y"].map((p) => (
                <button
                  key={p}
                  onClick={() => setPeriod(p)}
                  className={`px-3 py-1 text-sm rounded-md transition-colors ${
                    period === p
                      ? "bg-primary-600 text-white"
                      : "bg-gray-100 hover:bg-gray-200 text-gray-700"
                  }`}
                >
                  {p.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          <div className="h-80">
            {history.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={history}>
                  <defs>
                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis
                    dataKey="date"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(val) => val.split(" ")[0]}
                  />
                  <YAxis
                    tick={{ fontSize: 12 }}
                    domain={["dataMin - 50", "dataMax + 50"]}
                    tickFormatter={(val) => `₹${val}`}
                  />
                  <Tooltip
                    formatter={(val) => [`₹${val}`, "Price"]}
                    labelFormatter={(label) => `Date: ${label}`}
                  />
                  <Area
                    type="monotone"
                    dataKey="close"
                    stroke="#6366f1"
                    fillOpacity={1}
                    fill="url(#colorPrice)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500">
                No chart data available
              </div>
            )}
          </div>
        </div>

        {/* Technical Indicators */}
        <div className="space-y-4">
          {/* Key Stats */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Key Statistics</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-500">Day High</span>
                <span className="font-medium">
                  ₹{stock?.day_high?.toLocaleString() || "N/A"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Day Low</span>
                <span className="font-medium">
                  ₹{stock?.day_low?.toLocaleString() || "N/A"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">52W High</span>
                <span className="font-medium">
                  ₹{stock?.["52_week_high"]?.toLocaleString() || "N/A"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">52W Low</span>
                <span className="font-medium">
                  ₹{stock?.["52_week_low"]?.toLocaleString() || "N/A"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">P/E Ratio</span>
                <span className="font-medium">
                  {stock?.pe_ratio?.toFixed(2) || "N/A"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Market Cap</span>
                <span className="font-medium">
                  {stock?.market_cap
                    ? `₹${(stock.market_cap / 10000000).toFixed(0)} Cr`
                    : "N/A"}
                </span>
              </div>
            </div>
          </div>

          {/* Technical Indicators */}
          {indicators && (
            <div className="card">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Technical Indicators
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-500">RSI (14)</span>
                  <span
                    className={`font-medium ${
                      indicators.rsi < 30
                        ? "text-green-600"
                        : indicators.rsi > 70
                          ? "text-red-600"
                          : ""
                    }`}
                  >
                    {indicators.rsi?.toFixed(2)}
                    {indicators.rsi < 30 && " (Oversold)"}
                    {indicators.rsi > 70 && " (Overbought)"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">SMA (10)</span>
                  <span className="font-medium">
                    ₹{indicators.sma_10?.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">SMA (50)</span>
                  <span className="font-medium">
                    ₹{indicators.sma_50?.toLocaleString() || "N/A"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">MACD</span>
                  <span
                    className={`font-medium ${indicators.macd_histogram > 0 ? "text-green-600" : "text-red-600"}`}
                  >
                    {indicators.macd?.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Sentiment */}
          {sentiment && (
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">News Sentiment</h3>
              <div className="flex items-center gap-3">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    sentiment.overall_sentiment === "positive"
                      ? "bg-green-100"
                      : sentiment.overall_sentiment === "negative"
                        ? "bg-red-100"
                        : "bg-gray-100"
                  }`}
                >
                  <span className="text-2xl">
                    {sentiment.overall_sentiment === "positive"
                      ? "😊"
                      : sentiment.overall_sentiment === "negative"
                        ? "😟"
                        : "😐"}
                  </span>
                </div>
                <div>
                  <p className="font-medium capitalize">
                    {sentiment.overall_sentiment}
                  </p>
                  <p className="text-sm text-gray-500">
                    Based on {sentiment.news_count} articles
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
