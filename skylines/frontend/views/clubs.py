from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import func

from skylines.model import Club
from skylines.lib.vary import vary

clubs_blueprint = Blueprint('clubs', 'skylines')


@clubs_blueprint.route('/')
@vary('accept')
def index():
    if 'application/json' not in request.headers.get('Accept', ''):
        return render_template('ember-page.jinja', active_page='settings')

    clubs = Club.query().order_by(func.lower(Club.name))

    json = []
    for c in clubs:
        json.append({
            'id': c.id,
            'name': unicode(c),
        })

    return jsonify(clubs=json)
