import { useState, useEffect } from "react";
import { Newspaper, Calendar, TrendingUp, AlertCircle } from "lucide-react";
import { newsApi } from "../services/api";
import NewsCard from "../components/news/NewsCard";

export default function News() {
  const [news, setNews] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("news");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [newsRes, eventsRes] = await Promise.all([
        newsApi.getLatestNews(20),
        newsApi.getUpcomingEvents(30),
      ]);

      setNews(newsRes.data || []);
      setEvents(eventsRes.data || []);
    } catch (error) {
      console.error("Error fetching news:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-16 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Newspaper className="w-6 h-6" />
          News & Events
        </h1>
        <p className="text-gray-500 mt-1">
          Stay updated with market news and upcoming events
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-gray-200">
        <button
          onClick={() => setActiveTab("news")}
          className={`pb-3 px-1 font-medium transition-colors relative ${
            activeTab === "news"
              ? "text-primary-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          <div className="flex items-center gap-2">
            <Newspaper className="w-4 h-4" />
            Latest News
          </div>
          {activeTab === "news" && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600" />
          )}
        </button>

        <button
          onClick={() => setActiveTab("events")}
          className={`pb-3 px-1 font-medium transition-colors relative ${
            activeTab === "events"
              ? "text-primary-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Upcoming Events
          </div>
          {activeTab === "events" && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600" />
          )}
        </button>
      </div>

      {/* Content */}
      {activeTab === "news" ? (
        <div className="card">
          {loading ? (
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="h-24 bg-gray-100 rounded-lg animate-pulse"
                />
              ))}
            </div>
          ) : news.length > 0 ? (
            <div className="space-y-4">
              {news.map((item, index) => (
                <NewsCard key={index} news={item} />
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              No news available at the moment
            </p>
          )}
        </div>
      ) : (
        <div className="card">
          {loading ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div
                  key={i}
                  className="h-32 bg-gray-100 rounded-lg animate-pulse"
                />
              ))}
            </div>
          ) : events.length > 0 ? (
            <div className="space-y-4">
              {events.map((event) => (
                <div
                  key={event.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      <div
                        className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                          event.expected_impact === "high"
                            ? "bg-red-100"
                            : event.expected_impact === "medium"
                              ? "bg-yellow-100"
                              : "bg-gray-100"
                        }`}
                      >
                        <Calendar
                          className={`w-5 h-5 ${
                            event.expected_impact === "high"
                              ? "text-red-600"
                              : event.expected_impact === "medium"
                                ? "text-yellow-600"
                                : "text-gray-600"
                          }`}
                        />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">
                          {event.title}
                        </h3>
                        <p className="text-sm text-gray-500 mt-1">
                          {event.description}
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <span
                            className={`badge ${
                              event.expected_impact === "high"
                                ? "badge-danger"
                                : event.expected_impact === "medium"
                                  ? "badge-warning"
                                  : "badge-neutral"
                            }`}
                          >
                            {event.expected_impact?.toUpperCase()} IMPACT
                          </span>
                          <span className="badge badge-neutral">
                            {event.event_type?.replace("_", " ").toUpperCase()}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-500">
                        {new Date(event.date).toLocaleDateString("en-IN", {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        })}
                      </p>
                    </div>
                  </div>

                  {event.affected_sectors && (
                    <div className="mt-3 pt-3 border-t border-gray-100">
                      <p className="text-sm text-gray-600">
                        <span className="font-medium">Affected Sectors:</span>{" "}
                        {event.affected_sectors.join(", ")}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No upcoming events</p>
          )}
        </div>
      )}
    </div>
  );
}
