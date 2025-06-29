# SQL CODE


- CREATE TABLE "decks" (
	"did"	INTEGER NOT NULL,
	"deck_name"	VARCHAR(100) NOT NULL,
	"cid"	VARCHAR(100),
	"deck_score"	INTEGER,
	"deck_description"	VARCHAR(100),
	"last_reviewed"	VARCHAR(10),
	UNIQUE("deck_name"),
	PRIMARY KEY("did")
);


- CREATE TABLE "cards" (
	"cid"	INTEGER NOT NULL,
	"obverse"	VARCHAR(100) NOT NULL,
	"reverse"	VARCHAR(100) NOT NULL,
	"score"	INTEGER DEFAULT 1,
	PRIMARY KEY("cid")
);


- CREATE TABLE "users" (
	"uid"	INTEGER NOT NULL,
	"decks_owned"	INTEGER,
	"username"	VARCHAR(10) NOT NULL,
	FOREIGN KEY("decks_owned") REFERENCES "decks"("did"),
	PRIMARY KEY("uid")
);

# SQLAlchemy Code

- class cards(db.Model):
    cid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    obverse=db.Column(db.String(100), nullable=False)
    reverse=db.Column(db.String(100), nullable=False)
    score=db.Column(db.Integer,default=1)


- class decks(db.Model):
	did=db.Column(db.Integer,primary_key=True,autoincrement=True)
	deck_name=db.Column(db.String(100), nullable=False, unique=True)
	cid=db.Column(db.String(100), nullable=True)
	deck_score=db.Column(db.Integer)
	deck_description=db.Column(db.String(100))
	last_reviewed=db.Column(db.String(10))


- class users(db.Model):
    uid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    decks_owned=db.Column(db.Integer, db.ForeignKey('decks.did'),nullable=True)
    username=db.Column(db.String(10),nullable=False)
    name=db.Column(db.String(100))