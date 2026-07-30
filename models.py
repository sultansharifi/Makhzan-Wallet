from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Tarikhcha(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    nawu     = db.Column(db.String(10))   # 'amad' یا 'masraf'
    maqdar   = db.Column(db.Float)
    tawzih   = db.Column(db.String(200))
    tarikh   = db.Column(db.DateTime, default=datetime.utcnow)


class Makhzan:
    def __init__(self):
        rows = Tarikhcha.query.all()
        self.mojoudi = sum(
            r.maqdar if r.nawu == 'amad' else -r.maqdar
            for r in rows
        )
        self.majmua_amad   = sum(r.maqdar for r in rows if r.nawu == 'amad')
        self.majmua_masraf = sum(r.maqdar for r in rows if r.nawu == 'masraf')

    def amad(self, maqdar, tawzih=""):
        row = Tarikhcha(nawu='amad', maqdar=maqdar, tawzih=tawzih)
        db.session.add(row)
        db.session.commit()

    def masraf(self, maqdar, tawzih=""):
        row = Tarikhcha(nawu='masraf', maqdar=maqdar, tawzih=tawzih)
        db.session.add(row)
        db.session.commit()