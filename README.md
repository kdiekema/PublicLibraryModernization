# f19-msci3300-g3
Group 3 repository for South Liberty Public Library project

Developers: Alexis Overstreet, Karina Diekema, & Isaac Perrilles

Patrons Create Table:
CREATE TABLE `group3_patrons` (
  `patronID` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(225) NOT NULL,
  `last_name` varchar(225) NOT NULL,
  `birthdate` date NOT NULL,
  `address1` varchar(225) NOT NULL,
  `address2` varchar(225) DEFAULT NULL,
  `city` varchar(225) NOT NULL,
  `state` char(2) NOT NULL,
  `zip` char(5) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `phone2` varchar(20) DEFAULT NULL,
  `email` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`patronID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

USE f19_msci3300;

Materials Create Table:
CREATE TABLE `g3_materials` (
  `ID` int(45) NOT NULL AUTO_INCREMENT,
  `materialType` varchar(50) NOT NULL,
  `callNumber` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) NOT NULL,
  `copyright` int(4) DEFAULT NULL,
  `ISBN` varchar(13) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

Example of an insert query for Materials Table:
INSERT INTO `g3_materials`(`materialType`,`callNumber`,`title`,`author`,`publisher`,`copyright`,`ISBN`, `description` )
VALUES('Book','005.133/PERL/Oualline','Wicked cool Perl scripts : useful Perl scripts that solve difficult problems', 'Steve Oualline', 'No Starch Press','2006', '9781593270629', '' );


Circulation Create Table:
CREATE TABLE `g3_circulation` (
  `circulationID` int(11) NOT NULL AUTO_INCREMENT,
  `patronsID` int(11) NOT NULL,
  `materialsID` int(11) NOT NULL,
  `checkoutDate` date NOT NULL,
  `dueDate` date NOT NULL,
  PRIMARY KEY (`circulationID`),
  KEY `fk_patron` (`patronsID`),
  KEY `fk_material` (`materialsID`),
  CONSTRAINT `fkmaterial` FOREIGN KEY (`materialsID`) REFERENCES `g3_materials` (`ID`),
  CONSTRAINT `fkpatron` FOREIGN KEY (`patronsID`) REFERENCES `group3_patrons` (`patronID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

