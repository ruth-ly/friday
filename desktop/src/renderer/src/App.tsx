import { useState, useEffect, useCallback, useRef } from 'react'
import './App.css'
import VoiceOrb from './components/VoiceOrb'
import ResponsePanel from './components/ResponsePanel'
import TrendTicker from './components/TrendTicker'
import { useVoiceRecognition } from './hooks/useVoiceRecognition'

export type AppState = 'idle' | 'listening' | 'thinking' | 'speaking'

export default function App() {
  const [appState, setAppState]       = useState<AppState>('idle')
  const [transcript, setTranscript]   = useState('')
  const [response, setResponse]       = useState<FridayResponse | null>(null)
  const [trends, setTrends]           = useState<string[]>([])
  const [bootText, setBootText]       = useState('INITIALIZING...')
  const audioRef = useRef<HTMLAudioElement | null>(null)

  // Boot sequence greeting
  useEffect(() => {
    const lines = ['SYSTEMS ONLINE', 'NEURAL LINK ACTIVE', 'READY']
    let i = 0
    const t = setInterval(() => {
      setBootText(lines[i++])
      if (i >= lines.length) clearInterval(t)
    }, 700)
    return () => clearInterval(t)
  }, [])

  // Load trends every 5 min
  useEffect(() => {
    const load = async () => {
      try {
        const data = await window.friday.getTrends()
        if (Array.isArray(data))
          setTrends(data.map((t) => (typeof t === 'string' ? t : t.topic)).filter(Boolean).slice(0, 12))
      } catch { /* silent */ }
    }
    load()
    const id = setInterval(load, 5 * 60 * 1000)
    return () => clearInterval(id)
  }, [])

  const handleVoiceResult = useCallback(async (text: string) => {
    setTranscript(text)
    setAppState('thinking')
    setResponse(null)

    try {
      const result = await window.friday.ask(text, true)
      setResponse(result)

      if (result.trending?.length) setTrends(result.trending)

      if (result.audio_b64) {
        const audio = new Audio(`data:audio/mpeg;base64,${result.audio_b64}`)
        audioRef.current = audio
        setAppState('speaking')
        audio.onended = () => setAppState('idle')
        audio.onerror = () => setAppState('idle')
        audio.play().catch(() => setAppState('idle'))
      } else {
        // Browser TTS fallback
        const utt = new SpeechSynthesisUtterance(result.answer)
        utt.rate = 0.88
        utt.pitch = 1.1
        utt.volume = 1
        setAppState('speaking')
        utt.onend = () => setAppState('idle')
        speechSynthesis.cancel()
        speechSynthesis.speak(utt)
      }
    } catch {
      setResponse({
        answer: 'Connection error. Ensure the Friday server is running.',
        sources: [],
        trending: [],
        audio_b64: null,
      })
      setAppState('idle')
    }
  }, [])

  const { recognitionState, interimTranscript, startListening, stopListening } =
    useVoiceRecognition(handleVoiceResult)

  useEffect(() => {
    if (recognitionState === 'listening') setAppState('listening')
  }, [recognitionState])

  const handleOrbClick = () => {
    if (appState === 'idle')      { startListening() }
    else if (appState === 'listening') { stopListening() }
    else if (appState === 'speaking') {
      speechSynthesis.cancel()
      audioRef.current?.pause()
      setAppState('idle')
    }
  }

  const hintText: Record<AppState, string> = {
    idle:      'TAP ORB TO SPEAK',
    listening: interimTranscript || 'LISTENING...',
    thinking:  'ANALYZING SOURCES...',
    speaking:  'FRIDAY SPEAKING — TAP TO STOP',
  }

  return (
    <div className="app">
      <div className="scanline" />

      {/* Corner brackets */}
      <span className="corner tl" /><span className="corner tr" />
      <span className="corner bl" /><span className="corner br" />

      {/* ── Header ── */}
      <header className="hud-header" style={{ WebkitAppRegion: 'drag' } as React.CSSProperties}>
        <div className="brand">
          <span className="brand-diamond">◈</span>
          <span className="brand-name">F.R.I.D.A.Y.</span>
        </div>
        <div className="status-strip">
          <span className={`status-dot s-${appState}`} />
          <span className="status-text">{appState.toUpperCase()}</span>
        </div>
        <div className="hdr-btns" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
          <button className="hdr-btn" onClick={() => window.friday.hide()} title="Hide to tray">─</button>
        </div>
      </header>

      {/* ── System info bar ── */}
      <div className="sys-bar">
        <span>SYS <em>ONLINE</em></span>
        <span className="divider">│</span>
        <span>NET <em>ACTIVE</em></span>
        <span className="divider">│</span>
        <span>AI <em>{bootText}</em></span>
      </div>

      {/* ── Main body ── */}
      <main className="hud-body">
        <VoiceOrb state={appState} onClick={handleOrbClick} />

        <p className="orb-hint">{hintText[appState]}</p>

        {transcript && (
          <div className="transcript-panel">
            <div className="plabel">YOU</div>
            <p className="transcript-text">{transcript}</p>
          </div>
        )}

        {response && <ResponsePanel response={response} isActive={appState === 'speaking'} />}

        {!transcript && !response && (
          <div className="idle-grid">
            {['WEB ANALYSIS', 'NEWS FEED', 'TREND DETECTION', 'AI SYNTHESIS'].map((t) => (
              <div key={t} className="idle-chip">{t}</div>
            ))}
          </div>
        )}
      </main>

      {/* ── Trend ticker ── */}
      <TrendTicker trends={trends} />
    </div>
  )
}
