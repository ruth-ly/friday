import { useEffect, useState } from 'react'
import './ResponsePanel.css'

interface Source { title: string; url: string; snippet: string }
interface Props {
  response: { answer: string; sources: Source[] }
  isActive: boolean
}

export default function ResponsePanel({ response, isActive }: Props) {
  const [displayed, setDisplayed] = useState('')

  // Typewriter effect — reruns whenever the answer changes
  useEffect(() => {
    setDisplayed('')
    let i = 0
    const id = setInterval(() => {
      i++
      setDisplayed(response.answer.slice(0, i))
      if (i >= response.answer.length) clearInterval(id)
    }, 16)
    return () => clearInterval(id)
  }, [response.answer])

  return (
    <div className={`resp-panel ${isActive ? 'active' : ''}`}>
      <div className="plabel resp-label">F.R.I.D.A.Y.</div>

      <p className="resp-text">
        {displayed}
        {displayed.length < response.answer.length && (
          <span className="cursor">▌</span>
        )}
      </p>

      {response.sources?.length > 0 && (
        <div className="sources">
          <div className="src-label">SOURCES</div>
          {response.sources.slice(0, 3).map((s, i) => (
            <div key={i} className="src-item">
              <span className="src-num">[{i + 1}]</span>
              <span className="src-title" title={s.url}>{s.title || s.url}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
