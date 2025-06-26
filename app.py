from flask import *
from flask_sqlalchemy import *
from datetime import *
from time import *
from models import *
from helper import *


#print("DONE")
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
		print(uname)
		#uid=users.query.filter_by(username=uname).first()
		#curruid=uid.uid
		#print(curruid)
		global curruser
		curruser = uname
		return redirect(url_for('dash', uname=curruser))


@app.route('/user/<uname>', methods=["GET", "POST"])
def dash(uname):
	#print("dash",uname)
	name = users.query.filter_by(username=uname).first()
	dks = decks.query.all()

	
	for deck in dks:
		#lrt(deck.did)
		if deck.cid != '':
			scores(deck.did)
		
	return render_template('dashboard.html', username=name.name, decks=dks)


@app.route("/deck/<int:id>/edit", methods=["GET", "POST"])
def deck_update(id):
	if request.method == "GET":

		dks = decks.query.filter_by(did=id).first()
		cds = cards.query.all()
		#print(id)
		return render_template('editdeck.html', deck=dks, cards=cds)

	if request.method == "POST":
		global curruser
		#d_id=request.form["did"]
		dname = request.form["dname"]
		ddesc = request.form["ddesc"]
		cardlist = request.form.getlist("cardselect")
		x = ''
		for i in cardlist:
			x = x + str(i) + ','
		x = x[:-1]
		#print(x)
		#print(dname,ddesc)
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
		#global curruser
		cds = cards.query.all()
		return render_template('newdeck.html', cards=cds)

	if request.method == "POST":
		#global curruser
		d_id = request.form["did"]
		dname = request.form["dname"]
		ddesc = request.form["ddesc"]
		cardlist = request.form.getlist("cardselect")
		#cardlist = request.args.get('cardselect')
		print(cardlist, type(cardlist))
		x = ''
		for i in cardlist:
			x = x + str(i) + ','
		x = x[:-1]
		print(x)
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
		#cardlist = request.args.get('cardselect')
		#print(cardlist,type(cardlist))
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
		print(did, cl)
		clist = convint(cl)
		print('did:', did, 'clist:', clist)
		clist.reverse()
		vcl = clist
		vcll=vcl[-1]
		cdi = did

		return redirect('/deck/review/start')
@app.route('/deck/review/start', methods=["GET", "POST"])
def reviewproc():
	global curruser
	global vcl
	global vcll
	global cdi

	if request.method == "GET":
		if len(vcl) > 1:
      
			cl = request.args.get("diff", type=int)
			
			print('cl:',type(cl))
			print('vcl:',vcl)
			print('vcll:',vcll)
			x = vcl.pop()
			
			w = decks.query.filter_by(did=cdi).first()
			q = cards.query.filter_by(cid=x).first()

			print('x:',x,'w.deckname:', w.deck_name,'obverse:',q.obverse,'reverse:',q.reverse)
			print('vcl',vcl)
			
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
	#random mumbo jumbo about updating last reviewed time
	return redirect(url_for('dash',uname=curruser))


@app.route('/deletecard',methods=["GET","POST"])
def deletecard():
	global curruser
	if request.method == "GET":
		cds = cards.query.all()
		return render_template('delcard.html', cards=cds)

	if request.method == "POST":
		cardlist = request.form.getlist("cardselect")
		#cardlist = request.args.get('cardselect')
		print(cardlist, type(cardlist))
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
	app.run(debug=True, host='0.0.0.0', port='80')
