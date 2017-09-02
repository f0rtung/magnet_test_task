CREATE TABLE CommentInfo (
	CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
	LastName text NOT NULL,
	FirstName text NOT NULL,
	MiddleName text,
	RCRelation integer,
	Phone text NOT NULL,
	Email text NOT NULL,
	Comment text NOT NULL,
	FOREIGN KEY (RCRelation) REFERENCES RegionCityRelations(RelationID)
);

CREATE TABLE Regions (
	RegionID INTEGER PRIMARY KEY AUTOINCREMENT,
	RegionName text NOT NULL UNIQUE ON CONFLICT FAIL
);

CREATE TABLE Cities (
	CityID INTEGER PRIMARY KEY AUTOINCREMENT,
	CityName text NOT NULL UNIQUE ON CONFLICT FAIL
);

CREATE TABLE RegionCityRelations (
	RelationID INTEGER PRIMARY KEY AUTOINCREMENT,
	RegionID integer,
	CityID integer,
	FOREIGN KEY (RegionID) REFERENCES Regions(RegionID),
	FOREIGN KEY (CityID) REFERENCES Cities(CityID),
	UNIQUE(RegionID, CityID) ON CONFLICT FAIL
);

INSERT INTO Regions (RegionName) VALUES("Краснодарский край");
INSERT INTO Regions (RegionName) VALUES("Ростовская область");
INSERT INTO Regions (RegionName) VALUES("Ставропольский край");

INSERT INTO Cities (CityName) VALUES("Краснодар");
INSERT INTO Cities (CityName) VALUES("Кропоткин");
INSERT INTO Cities (CityName) VALUES("Славянск");
INSERT INTO Cities (CityName) VALUES("Ростов");
INSERT INTO Cities (CityName) VALUES("Шахты");
INSERT INTO Cities (CityName) VALUES("Батайск");
INSERT INTO Cities (CityName) VALUES("Ставрополь");
INSERT INTO Cities (CityName) VALUES("Пятигорск");
INSERT INTO Cities (CityName) VALUES("Кисловодск");

INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(1, 1);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(1, 2);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(1, 3);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(2, 4);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(2, 5);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(2, 6);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(3, 7);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(3, 8);
INSERT INTO RegionCityRelations (RegionID, CityID) VALUES(3, 9);