import { useState, useEffect, useRef, useCallback } from 'react'

type RecognitionState = 'idle' | 'listening' | 'processing'

export function useVoiceRecognition(onResult: (transcript: string) => void) {
  const [recognitionState, setRecognitionState] = useState<RecognitionState>('idle')
  const [interimTranscript, setInterimTranscript] = useState('')
  const recRef   = useRef<any>(null)
  const cbRef    = useRef(onResult)
  cbRef.current  = onResult

  useEffect(() => {
    const SR = (window as any).SpeechRecognition ?? (window as any).webkitSpeechRecognition
    if (!SR) {
      console.warn('SpeechRecognition not supported in this environment.')
      return
    }

    const rec = new SR()
    rec.continuous      = false
    rec.interimResults  = true
    rec.lang            = 'en-US'
    rec.maxAlternatives = 1

    rec.onstart = () => setRecognitionState('listening')
    rec.onend   = () => {
      setRecognitionState('idle')
      setInterimTranscript('')
    }
    rec.onerror = (e: any) => {
      if (e.error !== 'aborted') console.warn('Speech recognition error:', e.error)
      setRecognitionState('idle')
      setInterimTranscript('')
    }
    rec.onresult = (event: any) => {
      let interim = ''
      let final   = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const t = event.results[i][0].transcript
        if (event.results[i].isFinal) final += t
        else interim += t
      }
      setInterimTranscript(interim)
      if (final.trim()) {
        setRecognitionState('processing')
        cbRef.current(final.trim())
      }
    }

    recRef.current = rec
  }, [])

  const startListening = useCallback(() => {
    if (!recRef.current) return
    try { recRef.current.start() } catch { /* already started */ }
  }, [])

  const stopListening = useCallback(() => {
    try { recRef.current?.stop() } catch { /* already stopped */ }
  }, [])

  return { recognitionState, interimTranscript, startListening, stopListening }
}
