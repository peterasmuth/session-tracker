DROP DATABASE IF EXISTS session_tracker;
CREATE DATABASE session_tracker;
USE session_tracker;

-- Create Card Table and insert rows for each of 52 cards
CREATE TABLE Card (
	CardID INT IDENTITY(1,1)
	,Suit VARCHAR(10)
	,Rank VARCHAR(10)
	,PRIMARY KEY (CardID)
);

INSERT INTO Card (Suit, Rank)
VALUES ('Spade','Ace')
	   ,('Spade','Two')
	   ,('Spade','Three')
	   ,('Spade','Four')
	   ,('Spade','Five')
	   ,('Spade','Six')
	   ,('Spade','Seven')
	   ,('Spade','Eight')
	   ,('Spade','Nine')
	   ,('Spade','Ten')
	   ,('Spade','Jack')
	   ,('Spade','Queen')
	   ,('Spade','King')
	   ,('Heart','Ace')
	   ,('Heart','Two')
	   ,('Heart','Three')
	   ,('Heart','Four')
	   ,('Heart','Five')
	   ,('Heart','Six')
	   ,('Heart','Seven')
	   ,('Heart','Eight')
	   ,('Heart','Nine')
	   ,('Heart','Ten')
	   ,('Heart','Jack')
	   ,('Heart','Queen')
	   ,('Heart','King')
	   ,('Diamond','Ace')
	   ,('Diamond','Two')
	   ,('Diamond','Three')
	   ,('Diamond','Four')
	   ,('Diamond','Five')
	   ,('Diamond','Six')
	   ,('Diamond','Seven')
	   ,('Diamond','Eight')
	   ,('Diamond','Nine')
	   ,('Diamond','Ten')
	   ,('Diamond','Jack')
	   ,('Diamond','Queen')
	   ,('Diamond','King')
	   ,('Club','Ace')
	   ,('Club','Two')
	   ,('Club','Three')
	   ,('Club','Four')
	   ,('Club','Five')
	   ,('Club','Six')
	   ,('Club','Seven')
	   ,('Club','Eight')
	   ,('Club','Nine')
	   ,('Club','Ten')
	   ,('Club','Jack')
	   ,('Club','Queen')
	   ,('Club','King')

-- Create table for different game formats and insert a few initial values
CREATE TABLE Game (
	GameID int IDENTITY (1,1),
	Format VARCHAR(25),
	Limit VARCHAR(25),
	SmallBlind int,
	BigBlind int,
	Ante int,
	Straddle int,
	PRIMARY KEY (GameID)
);

INSERT INTO Game (Format, Limit, SmallBlind, BigBlind, Ante, Straddle)
VALUES ('Hold''em','No-Limit',1,2,0,0)
	   ,('Hold''em','No-Limit',2,5,0,0)
	   ,('Hold''em','No-Limit',1,2,0,5);

-- Create table for different card rooms and insert a few initial values
CREATE TABLE Location (
	LocationID int IDENTITY (1,1),
	LocationName VARCHAR(255),
	PRIMARY KEY (LocationID)
);

INSERT INTO Location (LocationName)
VALUES ('Cat''s Paw')
	  ,('Molly Brown');

-- Create the Session table. This will be the main table for the tracker
CREATE TABLE Session (
	SessionID int IDENTITY(1,1),
	BuyIn int,
	CashOut int,
	StartTime datetime,
	EndTime datetime,
	PRIMARY KEY (SessionID),
	Location int FOREIGN KEY REFERENCES Location(LocationID),
	GameID int FOREIGN KEY REFERENCES Game(GameID)
);

/*
CREATE TABLE Hand (
	HandID int IDENTITY(1,1),
	SessionID int FOREIGN KEY REFERENCES Session(SessionID),
	HoleCardOne int FOREIGN KEY REFERENCES Card(CardID),
	HoleCardTwo int FOREIGN KEY REFERENCES Card(CardID),
	BoardCardOne int FOREIGN KEY REFERENCES Card(CardID),
	BoardCardTwo int FOREIGN KEY REFERENCES Card(CardID),
	BoardCardThree int FOREIGN KEY REFERENCES Card(CardID),
	BoardCardFour int FOREIGN KEY REFERENCES Card(CardID),
	BoardCardFive int FOREIGN KEY REFERENCES Card(CardID),
);
*/