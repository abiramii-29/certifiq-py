from flask import Blueprint, render_template # type: ignore

template_bp = Blueprint('template', __name__)

@template_bp.route('/template-selection', methods=['GET'])
def template_selection():
    # This page shows available templates
    return render_template('template_selection.html')

