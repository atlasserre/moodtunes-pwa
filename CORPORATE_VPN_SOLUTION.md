# MoodTunes with ngrok - Corporate VPN Solution

## 🚀 Quick Setup with ngrok

### Step 1: Download ngrok
1. Go to https://ngrok.com/download
2. Create free account (GitHub login works)
3. Download Windows version
4. Extract ngrok.exe to your MoodTunes folder

### Step 2: Get Auth Token
1. In ngrok dashboard, copy your auth token
2. Run in PowerShell:
   ```
   .\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
   ```

### Step 3: Start MoodTunes + ngrok
```powershell
# Terminal 1 - Start MoodTunes server
py app.py

# Terminal 2 - Start ngrok tunnel
.\ngrok.exe http 5000
```

### Step 4: Get Public URL
ngrok will show something like:
```
Forwarding    https://abc123-def456.ngrok.io -> http://localhost:5000
```

### Step 5: Access from Any Device
- **Android**: Open Chrome, go to `https://abc123-def456.ngrok.io`
- **iPad**: Open Safari, go to `https://abc123-def456.ngrok.io` 
- **Any device with internet**: Works worldwide!

## ✅ Benefits of ngrok:
- ✅ **Bypasses corporate VPN** restrictions
- ✅ **HTTPS security** (required for PWA features)
- ✅ **Works from anywhere** with internet
- ✅ **No configuration** needed
- ✅ **Free tier available**

## 🎯 Alternative: Deploy to Cloud

If ngrok doesn't work, try:
1. **Render.com** - Free Python app hosting
2. **Railway.app** - Simple deployment
3. **Replit.com** - Code and host in browser
4. **Heroku** - Classic free hosting (requires credit card)

## 📱 Installation After Setup
Once you have a working URL (ngrok or cloud):
1. **Open URL** on each device
2. **Install PWA** using browser install prompts
3. **Enjoy** your cross-device music app!