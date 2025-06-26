CREATE TABLE "decks" (
	"did"	INTEGER NOT NULL,
	"deck_name"	VARCHAR(100) NOT NULL,
	"cid"	VARCHAR(100),
	"deck_score"	INTEGER,
	"deck_description"	VARCHAR(100),
	"last_reviewed"	VARCHAR(10),
	UNIQUE("deck_name"),
	PRIMARY KEY("did")
);

CREATE TABLE "cards" (
	"cid"	INTEGER NOT NULL,
	"obverse"	VARCHAR(100) NOT NULL,
	"reverse"	VARCHAR(100) NOT NULL,
	"score"	INTEGER DEFAULT 1,
	PRIMARY KEY("cid")
);

CREATE TABLE "users" (
	"uid"	INTEGER NOT NULL,
	"decks_owned"	INTEGER,
	"username"	VARCHAR(10) NOT NULL,
	FOREIGN KEY("decks_owned") REFERENCES "decks"("did"),
	PRIMARY KEY("uid")
);