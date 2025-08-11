import os
from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, request, abort, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime
from transcribe import transcribe_audio



load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devkey")
    
    # where to store recordings
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "audios")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB, adjust if needed

    db.init_app(app)
    migrate.init_app(app, db)

    from auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return "<a href='/login'>Login</a> | <a href='/register'>Register</a>"
    
        # ---- helper: require login ----
    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please log in first", "error")
                return redirect(url_for("auth.login"))
            return view(*args, **kwargs)
        return wrapped

    # ---- dashboard page (protected) ----
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

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

    return app

app = create_app()

# so alembic/flask-migrate sees models
from models import User,Recording   # noqa: E402,F401
