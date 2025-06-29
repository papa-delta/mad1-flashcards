from flask import *
from flask_sqlalchemy import *
from datetime import *
from time import *
from models import *
from helper import *

curruser = ''
vcl=[]  #VariableCardList
vcll=-1  #VariableCardList-Last
cdi=-1   #CurrentDeckIndex


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template('index.html')
	elif request.method == "POST":
		uname = request.form["uid"]
		global curruser
		curruser = uname
		return redirect(url_for('dash', uname=curruser))


@app.route('/user/<uname>', methods=["GET", "POST"])
def dash(uname):
	name = users.query.filter_by(username=uname).first()
	dks = decks.query.all()

	
	for deck in dks:
		if deck.cid != '':
			scores(deck.did)
		
	return render_template('dashboard.html', username=name.name, decks=dks)


@app.route("/deck/<int:id>/edit", methods=["GET", "POST"])
def deck_update(id):
	if request.method == "GET":

		dks = decks.query.filter_by(did=id).first()
		cds = cards.query.all()
		return render_template('editdeck.html', deck=dks, cards=cds)

	if request.method == "POST":
		global curruser
		dname = request.form["dname"]
		ddesc = request.form["ddesc"]
		cardlist = request.form.getlist("cardselect")

		if len(cardlist)<=0:
			return redirect('/deckemptyerror')  


		x = ''
		for i in cardlist:
			x = x + str(i) + ','
		x = x[:-1]
		x = decks.query.filter_by(did=id).update(
		    dict(deck_name=dname, deck_description=ddesc, cid=x))
		db.session.commit()
		return redirect(url_for('dash', uname=curruser))


@app.route("/deck/<int:id>/delete", methods=["GET", "POST"])
def deck_delete(id):

	x = decks.query.filter_by(did=id).first()
	db.session.delete(x)
	db.session.commit()
	return redirect(url_for('dash', uname=curruser))


@app.route("/newdeck", methods=["GET", "POST"])
def deck_create():
	global curruser
	if request.method == "GET":
		cds = cards.query.all()
		return render_template('newdeck.html', cards=cds)

	if request.method == "POST":
		d_id = request.form["did"]
		dname = request.form["dname"]
		ddesc = request.form["ddesc"]
		cardlist = request.form.getlist("cardselect")
		x = ''
		for i in cardlist:
			x = x + str(i) + ','
		x = x[:-1]
		z = decks(did=d_id, deck_name=dname, deck_description=ddesc, cid=x)
		db.session.add(z)
		db.session.commit()
		return redirect(url_for('dash', uname=curruser))


@app.route("/logout", methods=["GET"])
def logout():
	if request.method == "GET":
		global curruser
		curruser = ''
		return redirect("/")


@app.route("/newcard", methods=["GET", "POST"])
def newcard():
	global curruser
	if request.method == "GET":
		dks = decks.query.all()
		return render_template('newcard.html', decks=dks)
	if request.method == "POST":
		c_id = request.form["cid"]
		cobv = request.form["cobv"]
		crev = request.form["crev"]
		decklist = request.form.getlist("deckselect")
		if len(decklist)>0: 
			x = ''
			for i in decklist:
				x = x + str(i) + ','
			x = x[:-1]
			q = convint(x)
			for i in q:
				w = decks.query.filter_by(did=i).first()
				dold = w.cid
				if dold == '':
					dold = dold + str(c_id)
				else:
					dold = dold + ',' + str(c_id)
				c = decks.query.filter_by(did=i).update(dict(cid=dold))
				db.session.commit()
				scores(i)
		z = cards(cid=c_id, obverse=cobv, reverse=crev)
		db.session.add(z)
		db.session.commit()
		return redirect(url_for('dash', uname=curruser))


@app.route('/deck/review/', methods=["GET", "POST"])
def test():
	global curruser
	global vcl
	global vcll
	global cdi

	if request.method == "GET":
		did = request.args.get("did", type=int)
		cl = request.args.get("cid", type=str)

		if len(cl)<=0:
			return redirect('/deckerror')  

		clist = convint(cl)
		clist.reverse()
		vcl = clist
		vcll=vcl[-1]
		cdi = did

		return redirect('/deck/review/start')

@app.route('/deckerror', methods=["GET", "POST"])
def deckerror():
	if request.method=="GET":
		return render_template('deckerror.html')
	if request.method=="POST":
		return redirect(url_for('dash',uname=curruser))


@app.route('/deckemptyerror', methods=["GET", "POST"])
def deckemptyerror():
	if request.method=="GET":
		return render_template('deckemptyerror.html')
	if request.method=="POST":
		return redirect(url_for('dash',uname=curruser))

@app.route('/deck/review/start', methods=["GET", "POST"])
def reviewproc():
	global curruser
	global vcl
	global vcll
	global cdi

	if request.method == "GET":
		if len(vcl) > 1:
      
			cl = request.args.get("diff", type=int)
			
			x = vcl.pop()
			
			w = decks.query.filter_by(did=cdi).first()
			q = cards.query.filter_by(cid=x).first()

			if cl is not None:
				c=cards.query.filter_by(cid=vcll).update(dict(score=cl))
				db.session.commit()
				vcll=x


			return render_template('review.html',dname=w.deck_name,cid=x,cname=q.obverse,reverse=q.reverse)

		elif len(vcl) == 1:

			cl = request.args.get("diff", type=int)
			
			x = vcl.pop()
			w = decks.query.filter_by(did=cdi).first()
			q = cards.query.filter_by(cid=x).first()

			c=cards.query.filter_by(cid=vcll).update(dict(score=cl))
			db.session.commit()
			vcll=x

			return render_template('review.html',dname=w.deck_name,cid=x,cname=q.obverse,reverse=q.reverse)
    
		else:

			cl = request.args.get("diff", type=int)
			
			c=cards.query.filter_by(cid=vcll).update(dict(score=cl))
			db.session.commit()

			lrt(cdi) #updating last reviewed time
			scores(cdi)
			#resetting variables
			vcl=[]
			vcll=-1
			cdi=-1
			return redirect(url_for('dash',uname=curruser))


@app.route('/exitdeck',methods=["GET"])
def exitdeck():
	return redirect(url_for('dash',uname=curruser))


@app.route('/deletecard',methods=["GET","POST"])
def deletecard():
	global curruser
	if request.method == "GET":
		cds = cards.query.all()
		return render_template('delcard.html', cards=cds)

	if request.method == "POST":
		cardlist = request.form.getlist("cardselect")
		x = ''
		for i in cardlist:
			x = x + str(i) + ','
		x = x[:-1]
		a=convint(x)

		for i in a:
			z = cards.query.filter_by(cid=i).first()
			db.session.delete(z)
			db.session.commit()
	
	return redirect(url_for('dash', uname=curruser))

	
if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port='80')
