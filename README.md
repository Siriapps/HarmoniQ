
A web-based reading practice application designed for children with dyslexia, featuring eye tracking, voice recognition, and AI-powered content generation.

## 🎯 Features

- **Eye Tracking**: Uses WebGazer.js to monitor reading patterns
- **Voice Recognition**: Records and analyzes reading performance
- **AI-Powered Content**: Generates personalized practice content
- **Progressive Learning**: Three-stage practice system (Paragraph → Sentence → Word)
- **User Authentication**: Secure login with Auth0
- **Progress Tracking**: Monitor reading improvements over time

## 📋 Dependencies

### Frontend Dependencies (CDN - Already Included)

All frontend dependencies are loaded via CDN in the HTML files:

1. **Font Awesome 6.4.0** - Icons
   - `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`

2. **Auth0 SPA JS 2.0** - Authentication
   - `https://cdn.auth0.com/js/auth0-spa-js/2.0/auth0-spa-js.production.js`

3. **WebGazer.js** - Eye Tracking
   - `https://webgazer.cs.brown.edu/webgazer.js`

4. **Google Fonts - Atkinson Hyperlegible** - Dyslexia-friendly font
   - `https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700`

### Backend Dependencies (Required)

The application requires a Python backend server running at `http://127.0.0.1:5001` with the following endpoints:

- `POST /generate?q=paragraph` - Generate practice paragraphs
- `POST /generate?q=sentence` - Generate practice sentences
- `POST /generate?q=word` - Generate practice words
- `POST /stt` - Speech-to-text conversion
- `POST /tts` - Text-to-speech conversion

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** (for running the local server)
- **Modern web browser** with:
  - Microphone access support
  - Camera access support (for eye tracking)
  - JavaScript enabled

### Installation

1. **Clone or download the project**
   ```bash
   cd c:\Users\aaroh\HackUTD_frontend
   ```

2. **No additional installation needed!**
   All frontend dependencies are loaded via CDN.

### Running the Application

#### Option 1: Using Python Script (Recommended)

```bash
python start_server.py
```

This will:
- Start a local web server on port 8000
- Automatically open your browser to http://localhost:8000/index.html
- Enable CORS for local development

#### Option 2: Using Batch File (Windows)

Double-click `start_server.bat` or run:
```bash
start_server.bat
```

#### Option 3: Manual Python Server

```bash
python -m http.server 8000
```

Then open your browser to: http://localhost:8000/index.html

### Backend Setup (Required for Full Functionality)

⚠️ **Important**: The practice features require a backend server running at `http://127.0.0.1:5001`

Make sure your backend server is running with the following API endpoints:
- `/generate` - Content generation
- `/stt` - Speech-to-text
- `/tts` - Text-to-speech

Without the backend, you can still:
- Navigate the UI
- View the landing page
- Access profile pages
- Start calibration

But the following features won't work:
- Dynamic content generation
- Voice recording analysis
- Text-to-speech feedback

## 🔧 Configuration

### Auth0 Setup (Optional)

To enable full authentication features:

1. Create an Auth0 account at https://auth0.com
2. Create a new application (Single Page Application)
3. Update `auth_config.json` with your credentials:

```json
{
  "domain": "your-domain.auth0.com",
  "clientId": "your-client-id"
}
```

4. Configure callback URLs in Auth0:
   - Allowed Callback URLs: `http://localhost:8000/profile.html`
   - Allowed Logout URLs: `http://localhost:8000/index.html`
   - Allowed Web Origins: `http://localhost:8000`

## 📁 Project Structure

```
HackUTD_frontend/
├── index.html              # Landing page
├── style.css              # Landing page styles
├── script.js              # Landing page scripts
├── practice.html          # Practice interface
├── practicestyle.css      # Practice styles
├── practicescript.js      # Practice logic + eye tracking
├── profile.html           # User profile dashboard
├── profilescript.js       # Profile scripts
├── struggle.html          # Struggle words practice
├── strugglescript.js      # Struggle words logic
├── HarmoniQ.html          # Parent resources page
├── HarmonyiQscripts.js    # Parent page scripts
├── HarmonyiQstyle.css     # Parent page styles
├── auth_config.json       # Auth0 configuration
├── start_server.py        # Development server script
├── start_server.bat       # Windows batch file
├── README.md              # This file
└── Assets/                # Images and GIFs
    ├── Fat.png
    ├── Title.svg
    ├── Background.gif
    ├── celebrate.gif
    └── (various icon images)
```

## 🎮 Usage

### First Time Setup

1. **Start the frontend server** (port 8000)
2. **Start the backend server** (port 5001) - if available
3. Open http://localhost:8000/index.html
4. Click "Login" to authenticate (or skip if not configured)

### Practice Session

1. Click "Start Reading" on the landing page
2. Allow camera access for eye tracking
3. Complete the calibration process (9 points)
4. Click "Start Reading Practice" to begin
5. Follow the three-stage practice:
   - **Paragraph**: Read the full story
   - **Sentence**: Practice individual sentences
   - **Word**: Focus on challenging words

### Eye Tracking Calibration

- Click each red dot that appears
- Stare at each dot for 2 seconds
- Keep your head still, only move your eyes
- Make sure your face is visible in the video preview
- 9 calibration points total (3x3 grid)

## 🔍 Troubleshooting

### Camera Not Working
- Check browser permissions
- Make sure no other app is using the camera
- Try refreshing the page

### Microphone Not Working
- Allow microphone access when prompted
- Check browser settings
- Ensure microphone is not muted

### Backend Connection Failed
- Verify backend server is running at http://127.0.0.1:5001
- Check console for error messages
- Backend is optional for UI testing but required for full features

### CSS Not Loading
- Make sure you're accessing via http://localhost:8000 (not file://)
- Clear browser cache
- Check for CORS errors in console

## 🛠️ Development

### Making Changes

1. Edit HTML/CSS/JS files
2. Refresh browser to see changes
3. Check browser console (F12) for errors

### Adding New Features

- Frontend logic: Edit respective `.js` files
- Styling: Edit respective `.css` files
- New pages: Create new HTML file with corresponding CSS/JS

## 📝 Browser Support

- ✅ Chrome 90+ (Recommended)
- ✅ Edge 90+
- ✅ Firefox 88+
- ⚠️ Safari 14+ (Limited WebGazer support)

## 🔒 Privacy & Security

- Eye tracking data stays local (not sent to servers)
- Voice recordings are processed server-side but not stored
- Auth0 handles authentication securely
- No third-party analytics or tracking

## 📞 Support

For issues or questions:
1. Check the browser console for errors (F12)
2. Verify all dependencies are loaded (Network tab)
3. Ensure backend server is running (if using practice features)

## 🎓 Educational Resources

This application is built with research-backed principles:
- Multisensory learning approach
- Dyslexia-friendly typography (Atkinson Hyperlegible)
- Positive reinforcement
- Progressive difficulty scaling

## 📄 License

This project is part of HackUTD and is for educational purposes.

---

**Made with ❤️ for awesome readers**
