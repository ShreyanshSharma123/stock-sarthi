import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  TrendingUp,
  Newspaper,
  Star,
  BarChart3,
  X,
} from "lucide-react";
import clsx from "clsx";

const navItems = [
  { path: "/", icon: LayoutDashboard, label: "Dashboard" },
  { path: "/predictions", icon: TrendingUp, label: "AI Predictions" },
  { path: "/news", icon: Newspaper, label: "News & Events" },
  { path: "/watchlist", icon: Star, label: "Watchlist" },
];

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={clsx(
          "fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 bg-white border-r border-gray-200 z-40",
          "transform transition-transform duration-200 ease-in-out",
          "lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        {/* Close button (mobile) */}
        <button onClick={onClose} className="absolute top-4 right-4 lg:hidden">
          <X className="w-5 h-5 text-gray-500" />
        </button>

        {/* Navigation links */}
        <nav className="p-4 space-y-1 mt-8 lg:mt-0">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;

            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={clsx(
                  "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                  isActive
                    ? "bg-primary-50 text-primary-700 font-medium"
                    : "text-gray-600 hover:bg-gray-50",
                )}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Pro feature banner */}
        <div className="absolute bottom-4 left-4 right-4">
          <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg p-4 text-white">
            <h4 className="font-semibold">Upgrade to Pro</h4>
            <p className="text-sm text-primary-100 mt-1">
              Get advanced predictions and real-time alerts
            </p>
            <button className="mt-3 bg-white text-primary-600 px-4 py-1.5 rounded-md text-sm font-medium hover:bg-primary-50 transition-colors">
              Learn More
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
