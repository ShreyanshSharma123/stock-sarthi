import { Routes, Route } from "react-router-dom";
import { useState } from "react";

// Layout
import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";

// Pages
import Dashboard from "./pages/Dashboard";
import StockAnalysis from "./pages/StockAnalysis";
import Predictions from "./pages/Predictions";
import News from "./pages/News";
import Watchlist from "./pages/Watchlist";
import Login from "./pages/Login";
import Register from "./pages/Register";

// Context
import { AuthProvider } from "./context/AuthContext";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

        <div className="flex">
          {/* Sidebar */}
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

          {/* Main Content */}
          <main className="flex-1 p-6 lg:ml-64">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/stock/:symbol" element={<StockAnalysis />} />
              <Route path="/predictions" element={<Predictions />} />
              <Route path="/news" element={<News />} />
              <Route path="/watchlist" element={<Watchlist />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Routes>
          </main>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
