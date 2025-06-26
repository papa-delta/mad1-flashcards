from models import *


x=decks.query.filter_by(did=1).update(dict(deck_score=2))

db.session.commit()
