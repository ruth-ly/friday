import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'

const friday = {
  ask: (query: string, includeVoice = true) =>
    ipcRenderer.invoke('friday:ask', query, includeVoice),
  getTrends: () =>
    ipcRenderer.invoke('friday:trends'),
  hide: () =>
    ipcRenderer.invoke('friday:hide'),
}

if (process.contextIsolated) {
  contextBridge.exposeInMainWorld('electron', electronAPI)
  contextBridge.exposeInMainWorld('friday', friday)
} else {
  // @ts-ignore
  window.electron = electronAPI
  // @ts-ignore
  window.friday = friday
}
