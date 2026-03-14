import { Link } from "react-router-dom";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";

export default function PredictionCard({ prediction, compact = false }) {
  const getSignalColor = (signal) => {
    switch (signal?.toUpperCase()) {
      case "BUY":
        return "text-green-600 bg-green-50";
      case "SELL":
        return "text-red-600 bg-red-50";
      default:
        return "text-yellow-600 bg-yellow-50";
    }
  };

  const getSignalIcon = (signal) => {
    switch (signal?.toUpperCase()) {
      case "BUY":
        return <TrendingUp className="w-4 h-4" />;
      case "SELL":
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  if (compact) {
    return (
      <Link
        to={`/stock/${prediction.symbol}`}
        className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div
            className={`p-2 rounded-lg ${getSignalColor(prediction.signal)}`}
          >
            {getSignalIcon(prediction.signal)}
          </div>
          <div>
            <p className="font-medium text-sm">
              {prediction.symbol?.replace(".NS", "")}
            </p>
            <p className="text-xs text-gray-500">
              Confidence: {((prediction.confidence || 0) * 100).toFixed(0)}%
            </p>
          </div>
        </div>
        <span
          className={`px-2 py-1 rounded text-xs font-semibold ${getSignalColor(prediction.signal)}`}
        >
          {prediction.signal}
        </span>
      </Link>
    );
  }

  return (
    <Link
      to={`/stock/${prediction.symbol}`}
      className="flex items-center justify-between p-4 rounded-lg border border-gray-100 hover:border-primary-200 hover:shadow-sm transition-all"
    >
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-xl ${getSignalColor(prediction.signal)}`}>
          {getSignalIcon(prediction.signal)}
        </div>
        <div>
          <h3 className="font-semibold text-gray-900">
            {prediction.symbol?.replace(".NS", "")}
          </h3>
          <p className="text-sm text-gray-500">
            {prediction.name || "View Analysis"}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="text-right">
          <p className="text-sm text-gray-500">Expected Change</p>
          <p
            className={`font-semibold ${
              (prediction.price_change_percent || 0) >= 0
                ? "text-profit"
                : "text-loss"
            }`}
          >
            {prediction.price_change_percent >= 0 ? "+" : ""}
            {prediction.price_change_percent?.toFixed(2)}%
          </p>
        </div>

        <div className="text-right">
          <p className="text-sm text-gray-500">Confidence</p>
          <p className="font-semibold">
            {((prediction.confidence || 0) * 100).toFixed(0)}%
          </p>
        </div>

        <span
          className={`px-4 py-2 rounded-lg font-semibold ${getSignalColor(prediction.signal)}`}
        >
          {prediction.signal}
        </span>
      </div>
    </Link>
  );
}
