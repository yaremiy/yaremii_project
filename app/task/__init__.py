from flask import Blueprint

task_bp = Blueprint('task', __name__,
                        template_folder='templates/task')

from . import views