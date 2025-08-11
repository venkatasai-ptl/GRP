from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped
