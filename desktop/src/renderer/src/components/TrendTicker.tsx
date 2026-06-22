import './TrendTicker.css'

interface Props { trends: string[] }

export default function TrendTicker({ trends }: Props) {
  if (!trends.length) return (
    <div className="ticker">
      <span className="ticker-label">TRENDS</span>
      <span className="ticker-empty">— fetching live signals...</span>
    </div>
  )

  // Duplicate for seamless infinite scroll
  const items = [...trends, ...trends]

  return (
    <div className="ticker">
      <span className="ticker-label">TRENDS</span>
      <div className="ticker-track">
        <div className="ticker-scroll" style={{ animationDuration: `${items.length * 2}s` }}>
          {items.map((t, i) => (
            <span key={i} className="ticker-item">
              <span className="ticker-bullet">▸</span>{t}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
