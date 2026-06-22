import { contextBridge, ipcRenderer } from 'electron'

const friday = {
  ask: (query: string, includeVoice = true) =>
    ipcRenderer.invoke('friday:ask', query, includeVoice),
  getTrends: () =>
    ipcRenderer.invoke('friday:trends'),
  hide: () =>
    ipcRenderer.invoke('friday:hide'),
}

contextBridge.exposeInMainWorld('friday', friday)
