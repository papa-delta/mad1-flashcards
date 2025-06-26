
from models import *
from helper import *

'''name=users.query.filter_by(username='user1').first()

print(name.name)

for i in name:
  x.append(i[0])  
print(x)'''

def scores(id):
  l=decks.query.filter_by(did=id).first()
  a=l.cid
  cardslist=convint(a)
  #print('clist:',cardslist)


  numcards=len(cardslist)
  score=0

  for i in cardslist:
    c=cards.query.filter_by(cid=i).first()
    #print(i,c)
    score=score+c.score

  deckscore=score/numcards

  if deckscore>=1.66:
    deckadjscore=2
  elif deckscore<1.66:
    deckadjscore=1
  
  x=decks.query.filter_by(did=id).update(dict(deck_score=deckadjscore))
  db.session.commit()


#scores(5)
#scores(4)

scores(6)






