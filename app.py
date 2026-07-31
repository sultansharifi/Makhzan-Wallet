from flask import Flask, render_template, request, redirect, url_for
from models import db, Makhzan, Tarikhcha

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///makhzan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    m = Makhzan()
    rows = Tarikhcha.query.all()
    pipes_in = {}
    pipes_out = {}
    for r in rows:
        if r.nawu == 'amad':
            pipes_in[r.tawzih] = pipes_in.get(r.tawzih, 0) + r.maqdar
        else:
            pipes_out[r.tawzih] = pipes_out.get(r.tawzih, 0) + r.maqdar
    darsad = 0
    if m.majmua_amad > 0:
        darsad = min(int((m.mojoudi / m.majmua_amad) * 100), 100)
    return render_template('index.html',
        mojoudi=m.mojoudi,
        majmua_amad=m.majmua_amad,
        majmua_masraf=m.majmua_masraf,
        darsad=darsad,
        pipes_in=[{'name':k,'amt':v,'period':'monthly'} for k,v in pipes_in.items()],
        pipes_out=[{'name':k,'amt':v,'period':'monthly'} for k,v in pipes_out.items()]
    )


@app.route('/sabt', methods=['POST'])
def sabt():
    nawu   = request.form.get('nawu')
    maqdar = float(request.form.get('maqdar', 0))
    tawzih = request.form.get('tawzih', '')
    m = Makhzan()
    if nawu == 'amad':
        m.amad(maqdar, tawzih)
    elif nawu == 'masraf':
        m.masraf(maqdar, tawzih)
    return redirect(url_for('index'))


@app.route('/delete_pipe', methods=['POST'])
def delete_pipe():
    nawu_type = request.form.get('type')
    name = request.form.get('name')
    nawu = 'amad' if nawu_type == 'in' else 'masraf'
    rows = Tarikhcha.query.filter_by(nawu=nawu, tawzih=name).all()
    for r in rows:
        db.session.delete(r)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset_game():
    Tarikhcha.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
