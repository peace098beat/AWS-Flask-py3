from flask import Blueprint, render_template, current_app

# frontendのBlueprint
frontend = Blueprint('frontend', __name__, url_prefix='/frontend', template_folder="templates")


 
 
@frontend.route("/")
def frontend_root():
    logger = current_app.logger
    logger.debug('open frontend')
    return render_template("frontend/index.html")