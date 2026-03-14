import { useState, useEffect } from "react";
import { Zap, TrendingUp, TrendingDown, Filter } from "lucide-react";
import { predictionApi } from "../services/api";
import PredictionCard from "../components/predictions/PredictionCard";

export default function Predictions() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchSignals();
  }, []);

  const fetchSignals = async () => {
    try {
      const response = await predictionApi.getDailySignals();
      setSignals(response.data || []);
    } catch (error) {
      console.error("Error fetching signals:", error);
      // Demo data
      setSignals([
        {
          symbol: "RELIANCE.NS",
          name: "Reliance Industries",
          signal: "BUY",
          confidence: 0.78,
          price_change_percent: 3.2,
        },
        {
          symbol: "TCS.NS",
          name: "TCS",
          signal: "HOLD",
          confidence: 0.65,
          price_change_percent: 0.5,
        },
        {
          symbol: "INFY.NS",
          name: "Infosys",
          signal: "BUY",
          confidence: 0.72,
          price_change_percent: 2.1,
        },
        {
          symbol: "HDFCBANK.NS",
          name: "HDFC Bank",
          signal: "SELL",
          confidence: 0.68,
          price_change_percent: -1.8,
        },
        {
          symbol: "ICICIBANK.NS",
          name: "ICICI Bank",
          signal: "BUY",
          confidence: 0.81,
          price_change_percent: 2.5,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const filteredSignals = signals.filter((s) => {
    if (filter === "all") return true;
    return s.signal.toLowerCase() === filter;
  });

  const signalCounts = {
    buy: signals.filter((s) => s.signal === "BUY").length,
    hold: signals.filter((s) => s.signal === "HOLD").length,
    sell: signals.filter((s) => s.signal === "SELL").length,
  };

  return (
    <div className="mt-16 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Zap className="w-6 h-6 text-yellow-500" />
          AI Predictions
        </h1>
        <p className="text-gray-500 mt-1">
          Machine learning powered stock recommendations updated daily
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-green-50 border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-600 text-sm font-medium">Buy Signals</p>
              <p className="text-3xl font-bold text-green-700">
                {signalCounts.buy}
              </p>
            </div>
            <TrendingUp className="w-10 h-10 text-green-500" />
          </div>
        </div>

        <div className="card bg-yellow-50 border-yellow-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-600 text-sm font-medium">
                Hold Signals
              </p>
              <p className="text-3xl font-bold text-yellow-700">
                {signalCounts.hold}
              </p>
            </div>
            <div className="w-10 h-10 bg-yellow-200 rounded-full flex items-center justify-center">
              <span className="text-xl">⏸️</span>
            </div>
          </div>
        </div>

        <div className="card bg-red-50 border-red-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-red-600 text-sm font-medium">Sell Signals</p>
              <p className="text-3xl font-bold text-red-700">
                {signalCounts.sell}
              </p>
            </div>
            <TrendingDown className="w-10 h-10 text-red-500" />
          </div>
        </div>
      </div>

      {/* Filter */}
      <div className="flex items-center gap-2">
        <Filter className="w-4 h-4 text-gray-500" />
        <span className="text-sm text-gray-500">Filter:</span>
        {["all", "buy", "hold", "sell"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 text-sm rounded-full transition-colors ${
              filter === f
                ? "bg-primary-600 text-white"
                : "bg-gray-100 hover:bg-gray-200 text-gray-700"
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Predictions List */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Today's Signals</h2>

        {loading ? (
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="h-20 bg-gray-100 rounded-lg animate-pulse"
              />
            ))}
          </div>
        ) : filteredSignals.length > 0 ? (
          <div className="space-y-3">
            {filteredSignals.map((signal) => (
              <PredictionCard key={signal.symbol} prediction={signal} />
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            No signals found for the selected filter
          </p>
        )}
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-sm text-yellow-800">
          <strong>Disclaimer:</strong> These predictions are generated by
          machine learning models and should not be considered as financial
          advice. Always do your own research and consult a financial advisor
          before making investment decisions.
        </p>
      </div>
    </div>
  );
}
