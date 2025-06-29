#Helper functions go here
from models import *
from datetime import *
from time import *

#convert comma-separated string to list of integers
def convint(l):
  q=l.split(',')
  a=[]
  #print('l',l)
  #print('q',q)
  for i in q:
    a.append(int(i))
  return a

#function to update the deck score, the input is a deck ID
def scores(id):

	l=decks.query.filter_by(did=id).first()
	a=l.cid
	if a is not None:
		cardslist=convint(a)

		numcards=len(cardslist)
		score=0

		#print('cdl:',cardslist,'len:',len(cardslist))

		for i in cardslist:
			c=cards.query.filter_by(cid=i).first()
			#print(c.score)
			if c is not None:
				if c.score is not None:
					score=score+c.score

		deckscore=score/numcards

		if deckscore>=1.66:
			deckadjscore=2
		elif deckscore<1.66:
			deckadjscore=1

		x=decks.query.filter_by(did=id).update(dict(deck_score=deckadjscore))
		db.session.commit()
	
	else:
		return


#function to update date of last review of a deck
def lrt(id):
	x=str(date.today())
	c=decks.query.filter_by(did=id).update(dict(last_reviewed=x))
	db.session.commit()
	return


'''def fetchdiff(id):
  l=decks.query.filter_by(did=id).first()
  a=l.deck_score

  deckdiff=''

  if a==1:

#scores(4)

scores(1)
scores(2)
scores(3)
scores(4)


#convint('1,2,4,6,12,2342,45')
'''