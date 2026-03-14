import { useState, useEffect } from "react";
import { Star, Plus, Trash2, Bell } from "lucide-react";
import { watchlistApi, stockApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Watchlist() {
  const { isAuthenticated } = useAuth();
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newStock, setNewStock] = useState({ symbol: "", targetPrice: "" });

  useEffect(() => {
    if (isAuthenticated) {
      fetchWatchlist();
    } else {
      setLoading(false);
    }
  }, [isAuthenticated]);

  const fetchWatchlist = async () => {
    try {
      const response = await watchlistApi.getWatchlist();
      setWatchlist(response.data?.stocks || []);
    } catch (error) {
      console.error("Error fetching watchlist:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddStock = async (e) => {
    e.preventDefault();
    try {
      await watchlistApi.addStock(
        newStock.symbol.toUpperCase() + ".NS",
        newStock.targetPrice || null,
        "",
      );
      fetchWatchlist();
      setShowAddModal(false);
      setNewStock({ symbol: "", targetPrice: "" });
    } catch (error) {
      alert(
        "Error adding stock: " +
          (error.response?.data?.detail || error.message),
      );
    }
  };

  const handleRemoveStock = async (symbol) => {
    if (!confirm("Remove this stock from watchlist?")) return;

    try {
      await watchlistApi.removeStock(symbol);
      setWatchlist(watchlist.filter((s) => s.symbol !== symbol));
    } catch (error) {
      alert("Error removing stock");
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="mt-16 flex flex-col items-center justify-center py-20">
        <Star className="w-16 h-16 text-gray-300 mb-4" />
        <h2 className="text-xl font-semibold text-gray-900">
          Login to view your watchlist
        </h2>
        <p className="text-gray-500 mt-2">
          Track your favorite stocks and get alerts
        </p>
        <Link to="/login" className="btn-primary mt-4">
          Login
        </Link>
      </div>
    );
  }

  return (
    <div className="mt-16 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Star className="w-6 h-6 text-yellow-500" />
            My Watchlist
          </h1>
          <p className="text-gray-500 mt-1">Track your favorite stocks</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Add Stock
        </button>
      </div>

      {/* Watchlist */}
      <div className="card">
        {loading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div
                key={i}
                className="h-16 bg-gray-100 rounded-lg animate-pulse"
              />
            ))}
          </div>
        ) : watchlist.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-sm text-gray-500 border-b">
                  <th className="pb-3 font-medium">Stock</th>
                  <th className="pb-3 font-medium">Current Price</th>
                  <th className="pb-3 font-medium">Change</th>
                  <th className="pb-3 font-medium">Target Price</th>
                  <th className="pb-3 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {watchlist.map((stock) => (
                  <tr
                    key={stock.symbol}
                    className="border-b last:border-0 hover:bg-gray-50"
                  >
                    <td className="py-4">
                      <Link
                        to={`/stock/${stock.symbol}`}
                        className="font-medium text-gray-900 hover:text-primary-600"
                      >
                        {stock.symbol.replace(".NS", "")}
                      </Link>
                    </td>
                    <td className="py-4">
                      <span className="font-medium">
                        ₹{stock.live_price?.toLocaleString() || "N/A"}
                      </span>
                    </td>
                    <td className="py-4">
                      <span
                        className={`font-medium ${
                          (stock.change_percent || 0) >= 0
                            ? "text-profit"
                            : "text-loss"
                        }`}
                      >
                        {stock.change_percent
                          ? `${stock.change_percent >= 0 ? "+" : ""}${stock.change_percent.toFixed(2)}%`
                          : "N/A"}
                      </span>
                    </td>
                    <td className="py-4">
                      {stock.target_price ? (
                        <span className="text-gray-600">
                          ₹{stock.target_price.toLocaleString()}
                        </span>
                      ) : (
                        <span className="text-gray-400">Not set</span>
                      )}
                    </td>
                    <td className="py-4">
                      <div className="flex items-center gap-2">
                        <button
                          className="p-2 hover:bg-gray-100 rounded-lg text-gray-500"
                          title="Set alert"
                        >
                          <Bell className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleRemoveStock(stock.symbol)}
                          className="p-2 hover:bg-red-50 rounded-lg text-red-500"
                          title="Remove"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <Star className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900">
              Your watchlist is empty
            </h3>
            <p className="text-gray-500 mt-1">
              Add stocks to track their performance
            </p>
            <button
              onClick={() => setShowAddModal(true)}
              className="btn-primary mt-4"
            >
              Add Your First Stock
            </button>
          </div>
        )}
      </div>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-bold mb-4">Add Stock to Watchlist</h2>
            <form onSubmit={handleAddStock}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Stock Symbol
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., RELIANCE, TCS, INFY"
                    value={newStock.symbol}
                    onChange={(e) =>
                      setNewStock({ ...newStock, symbol: e.target.value })
                    }
                    className="input-field"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Enter without .NS suffix
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Target Price (Optional)
                  </label>
                  <input
                    type="number"
                    placeholder="e.g., 2500"
                    value={newStock.targetPrice}
                    onChange={(e) =>
                      setNewStock({ ...newStock, targetPrice: e.target.value })
                    }
                    className="input-field"
                  />
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary flex-1">
                  Add Stock
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
