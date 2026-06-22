import {
  app, BrowserWindow, Tray, Menu, nativeImage,
  ipcMain, screen, session
} from 'electron'
import { join } from 'path'

let mainWindow: BrowserWindow | null = null
let tray: Tray | null = null

function getWindowPosition(): { x: number; y: number } {
  const { workArea } = screen.getPrimaryDisplay()
  const winBounds = mainWindow!.getBounds()
  return {
    x: workArea.x + workArea.width - winBounds.width - 16,
    y: workArea.y + workArea.height - winBounds.height - 16,
  }
}

function showWindow(): void {
  if (!mainWindow) return
  const pos = getWindowPosition()
  mainWindow.setBounds({ ...mainWindow.getBounds(), ...pos })
  mainWindow.show()
  mainWindow.focus()
}

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 380,
    height: 680,
    show: false,
    frame: false,
    transparent: true,
    resizable: false,
    skipTaskbar: true,
    alwaysOnTop: true,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
      contextIsolation: true,
    },
  })

  // Close button hides to tray, never quits
  mainWindow.on('close', (e) => {
    e.preventDefault()
    mainWindow?.hide()
  })

  if (process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

function createTray(): void {
  let icon: Electron.NativeImage
  try {
    icon = nativeImage.createFromPath(join(__dirname, '../../resources/icon.png'))
    if (icon.isEmpty()) throw new Error('empty icon')
  } catch {
    icon = nativeImage.createEmpty()
  }

  tray = new Tray(icon)
  tray.setToolTip('F.R.I.D.A.Y — AI Assistant')

  tray.on('click', () => {
    mainWindow?.isVisible() ? mainWindow?.hide() : showWindow()
  })

  tray.setContextMenu(
    Menu.buildFromTemplate([
      { label: 'Open Friday', click: showWindow },
      { label: 'Hide',        click: () => mainWindow?.hide() },
      { type: 'separator' },
      {
        label: 'Quit',
        click: () => {
          mainWindow?.removeAllListeners('close')
          app.quit()
        },
      },
    ])
  )
}

app.whenReady().then(() => {
  app.setAppUserModelId('com.friday.ai')

  // Grant microphone permission so Web Speech API works
  session.defaultSession.setPermissionRequestHandler((_, permission, cb) => {
    cb(permission === 'media' || permission === 'microphone')
  })

  createWindow()
  createTray()
  showWindow()
})

// Keep running in tray — never quit on all-windows-closed
app.on('window-all-closed', () => { /* intentionally empty */ })

// ─── IPC handlers ──────────────────────────────────────────────────────────

ipcMain.handle('friday:ask', async (_, query: string, includeVoice = true) => {
  try {
    const res = await fetch('http://localhost:8000/api/v1/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, include_voice: includeVoice }),
    })
    return await res.json()
  } catch {
    return {
      answer: 'Backend offline. Start the Friday server with: python scripts/run.py',
      sources: [],
      trending: [],
      audio_b64: null,
    }
  }
})

ipcMain.handle('friday:trends', async () => {
  try {
    const res = await fetch('http://localhost:8000/api/v1/trends')
    return await res.json()
  } catch {
    return []
  }
})

ipcMain.handle('friday:hide', () => mainWindow?.hide())
