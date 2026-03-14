import { Link } from "react-router-dom";
import { TrendingUp, TrendingDown, ChevronRight } from "lucide-react";

export default function StockCard({ stock }) {
  // Mock price data (replace with actual data from API)
  const mockPrice = Math.floor(Math.random() * 3000) + 500;
  const mockChange = (Math.random() * 6 - 3).toFixed(2);

  return (
    <Link
      to={`/stock/${stock.symbol}`}
      className="flex items-center justify-between p-4 rounded-lg border border-gray-100 hover:border-primary-200 hover:bg-primary-50/30 transition-all group"
    >
      <div className="flex items-center gap-4">
        <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center font-semibold text-gray-600">
          {stock.symbol?.charAt(0) || stock.name?.charAt(0)}
        </div>
        <div>
          <h3 className="font-semibold text-gray-900 group-hover:text-primary-700">
            {stock.symbol?.replace(".NS", "")}
          </h3>
          <p className="text-sm text-gray-500 truncate max-w-[200px]">
            {stock.name}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="text-right">
          <p className="font-semibold">₹{mockPrice.toLocaleString()}</p>
          <div
            className={`flex items-center justify-end gap-1 text-sm ${
              parseFloat(mockChange) >= 0 ? "text-profit" : "text-loss"
            }`}
          >
            {parseFloat(mockChange) >= 0 ? (
              <TrendingUp className="w-3 h-3" />
            ) : (
              <TrendingDown className="w-3 h-3" />
            )}
            <span>{mockChange}%</span>
          </div>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-300 group-hover:text-primary-500" />
      </div>
    </Link>
  );
}
