from flask import Blueprint, session, redirect, request, url_for

lang_bp = Blueprint("lang", __name__)

@lang_bp.route("/set_language/<lang_code>")
def set_language(lang_code):
    if lang_code in ["en", "ar"]:
        session["lang"] = lang_code

    # try to go back where user was
    ref = request.referrer
    if ref and "/set_language/" not in ref:
        return redirect(ref)

    # fallback
    return redirect(url_for("dashboard"))
