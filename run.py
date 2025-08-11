import os
from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, request, abort, send_from_directory, flash
from app.database import db
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime
from app.utils.transcribe import transcribe_audio



load_dotenv()

# Database instance imported from app.database
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devkey")
    
    # where to store recordings
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "audios")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB, adjust if needed

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.route("/")
    def home():
        return "<a href='/login'>Login</a> | <a href='/register'>Register</a>"
    
    # ---- helper: require login ----
    from app.auth_helpers import login_required

    # ---- upload endpoint for audio blobs ----
    @app.post("/api/upload")
    @login_required
    def upload_audio():
        file = request.files.get("audio")
        if not file:
            abort(400, "no file part 'audio'")
        # save as: <userId>_<timestamp>.webm
        user_id = session["user_id"]
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        # Most browsers record WebM/Opus; keep .webm
        filename = secure_filename(f"{user_id}_{ts}.webm")
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        
        # Call our transcriber
        transcript_text = transcribe_audio(path)

        rec = Recording(user_id=user_id, filename=filename, transcript=transcript_text)
        db.session.add(rec)
        db.session.commit()
        
        return {"ok": True, "filename": filename, "transcript": transcript_text}

    # (Optional) serve back a file for testing
    @app.get("/recordings/<name>")
    @login_required
    def get_recording(name):
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)

    # Import models after app creation to avoid circular imports
    from app.models import User, Recording   # noqa: F401

    # Context processor to add current year to all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
