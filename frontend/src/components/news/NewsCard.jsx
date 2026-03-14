import { ExternalLink } from "lucide-react";

export default function NewsCard({ news, compact = false }) {
  const getSentimentBadge = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case "positive":
        return <span className="badge badge-success">Positive</span>;
      case "negative":
        return <span className="badge badge-danger">Negative</span>;
      default:
        return <span className="badge badge-neutral">Neutral</span>;
    }
  };

  if (compact) {
    return (
      <a
        href={news.link || "#"}
        target="_blank"
        rel="noopener noreferrer"
        className="block p-3 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <h4 className="text-sm font-medium text-gray-900 line-clamp-2">
          {news.title}
        </h4>
        <div className="flex items-center gap-2 mt-2">
          {getSentimentBadge(news.sentiment)}
          <span className="text-xs text-gray-500">{news.source}</span>
        </div>
      </a>
    );
  }

  return (
    <a
      href={news.link || "#"}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 rounded-lg border border-gray-100 hover:border-primary-200 hover:shadow-sm transition-all group"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h3 className="font-medium text-gray-900 group-hover:text-primary-600 line-clamp-2">
            {news.title}
          </h3>
          <div className="flex items-center gap-3 mt-2">
            {getSentimentBadge(news.sentiment)}
            <span className="text-sm text-gray-500">{news.source}</span>
            {news.published && (
              <span className="text-sm text-gray-400">
                {new Date(news.published).toLocaleDateString("en-IN", {
                  month: "short",
                  day: "numeric",
                })}
              </span>
            )}
          </div>
          {news.event_type && (
            <div className="mt-2">
              <span className="badge badge-neutral">
                {news.event_type.replace("_", " ").toUpperCase()}
              </span>
            </div>
          )}
        </div>
        <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-primary-500 flex-shrink-0" />
      </div>
    </a>
  );
}
