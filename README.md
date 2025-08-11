# GRP - Speech to Text Transcription

GRP is a Flask web application that provides browser-based audio recording and speech-to-text transcription functionality.

![Application Screenshot](screenshot.png)

## Features

- 🎤 Browser-based audio recording
- ✍️ Speech-to-text transcription
- 👤 User authentication (login/register)
- 💾 Save and manage transcriptions
- 📱 Responsive design with Bootstrap 5
- 📊 Dashboard with recent recordings

## Technology Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (with migrations)
- **Audio Processing**: Web Audio API

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/venkatasai-ptl/GRP.git
cd GRP
```

2. **Create virtual environment**:
```bash
python -m venv .venv
```

3. **Activate virtual environment**:
```bash
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Set environment variables**:
Create a `.env` file with:
```env
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key
```

## Running the Application

```bash
python run.py
```

Visit http://127.0.0.1:5000 in your browser.

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `sqlite:///app.db` |
| `SECRET_KEY` | Flask session secret | Randomly generated |

### File Structure
```
GRP/
├── app/              # Application package
│   ├── routes/       # Blueprint-based routes
│   ├── static/       # CSS, JS assets
│   ├── templates/    # HTML templates
│   ├── utils/        # Utilities
│   ├── __init__.py   # Package initialization
│   ├── database.py   # Database configuration
│   └── models.py     # Data models
├── migrations/       # Database migrations
├── .env              # Environment configuration
├── .flaskenv         # Flask environment settings
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py            # Application entry point
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
