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
    tarikha = Tarikhcha.query.order_by(Tarikhcha.tarikh.desc()).all()
    darsad = 0
    if m.majmua_amad > 0:
        darsad = min(int((m.mojoudi / m.majmua_amad) * 100), 100)
    return render_template('index.html',
        mojoudi=m.mojoudi,
        majmua_amad=m.majmua_amad,
        majmua_masraf=m.majmua_masraf,
        darsad=darsad,
        tarikha=tarikha
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


@app.route('/delete/<int:rid>', methods=['POST'])
def delete(rid):
    row = Tarikhcha.query.get_or_404(rid)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)