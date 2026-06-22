import './VoiceOrb.css'
import type { AppState } from '../App'

interface Props {
  state: AppState
  onClick: () => void
}

export default function VoiceOrb({ state, onClick }: Props) {
  return (
    <div className={`orb-wrap orb-${state}`} onClick={onClick} role="button" aria-label="Voice input">
      {/* Outer rings */}
      <div className="ring r3" />
      <div className="ring r2" />
      <div className="ring r1" />

      {/* Core */}
      <div className="orb-core">
        {state === 'idle' && <span className="orb-icon idle-icon">◉</span>}

        {state === 'listening' && (
          <div className="wave-bars">
            {[0, 1, 2, 3, 4].map((i) => (
              <div key={i} className="bar" style={{ animationDelay: `${i * 0.1}s` }} />
            ))}
          </div>
        )}

        {state === 'thinking' && <div className="think-spinner" />}

        {state === 'speaking' && <span className="orb-icon speak-icon">◎</span>}
      </div>

      {/* Arc reactor ring */}
      <div className="arc-ring" />
    </div>
  )
}
