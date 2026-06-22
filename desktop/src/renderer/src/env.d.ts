/// <reference types="vite/client" />

interface FridayResponse {
  answer: string
  sources: Array<{ title: string; url: string; snippet: string; published_at?: string }>
  trending: string[]
  audio_b64?: string | null
}

interface Window {
  friday: {
    ask: (query: string, includeVoice?: boolean) => Promise<FridayResponse>
    getTrends: () => Promise<Array<{ topic: string }>>
    hide: () => void
  }
}
