const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('node:path')

function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
            preload: path.join(__dirname, 'preload.js')
        }
    })

    ipcMain.on('set-title', (event, arg) => {
        const webContents = event.sender    
        const win = BrowserWindow.fromWebContents(webContents)
        win.setTitle(arg)
    })

    win.loadFile('electron/index.html')
    win.webContents.openDevTools()
}

app.whenReady().then(() => {
    createWindow()
    
    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow()
        }
    })
})


app.on('ready', () => {
    console.log('ready')
    ipcMain.on('message', (event, arg) => {
        console.log(arg)
        //event.reply('reply', 'pong')
        event.returnValue = 'pong'
    })
    
    ipcMain.on('message2', (event, arg) => {
        console.log(arg)
        event.reply('reply', 'ping')
    })
})

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})