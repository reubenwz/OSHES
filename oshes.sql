DROP SCHEMA IF EXISTS oshes;

CREATE DATABASE oshes;

USE `oshes`;

/*Table structure for table Customer */

DROP TABLE IF EXISTS Customer;
CREATE TABLE Customer(  
     customerID    	INT    		NOT NULL UNIQUE,
     name      		VARCHAR(50)   	NOT NULL,
     gender        	VARCHAR(50)   	NOT NULL,
     emailAddress   	VARCHAR(50) NOT NULL,
     phoneNumber    	VARCHAR(50)    	NOT NULL,
     address      	VARCHAR(50)   	NOT NULL,
     password    	VARCHAR(50) NOT NULL,
     CHECK(gender IN ('Male','Female')),
     PRIMARY KEY (customerID)); 

/*Table structure for table Administrators */

DROP TABLE IF EXISTS Administrator;
CREATE TABLE Administrator(  
     adminID            INT    		NOT NULL UNIQUE,
     name      		VARCHAR(50)   	NOT NULL,
     gender        	VARCHAR(50)   	NOT NULL,
     phoneNumber    	VARCHAR(50)    	NOT NULL,
     password    	VARCHAR(50)     NOT NULL,
     CHECK(gender IN ('Male','Female')),
     PRIMARY KEY (adminID)); 

/*Table structure for table Purchases */

DROP TABLE IF EXISTS Purchase;
CREATE TABLE Purchase(
     purchaseID 		INT 	NOT NULL UNIQUE,
     purchaseDate 	DATE 	NOT NULL,
     customerID 		INT 	NOT NULL,
     PRIMARY KEY(purchaseID),
     FOREIGN KEY(customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE
                                                               ON DELETE CASCADE);
    
/*Table structure for table Products */

DROP TABLE IF EXISTS Product;
CREATE TABLE Product(
     productID 	    	INT  	UNIQUE NOT NULL,
     category      	VARCHAR(50)	NOT NULL,    
     model          	VARCHAR(50) 	NOT NULL,
     cost    	    	INT	 	NOT NULL,
     price          	INT		NOT NULL,
     warranty       	INT	NOT NULL,
       
     CHECK(category IN ('Lights', 'Locks')) ,
     CHECK((model IN ('Light1', 'Light2', 'SmartHome1') AND category = 'Lights') OR 
	   (model IN ('Safe1', 'Safe2', 'Safe3', 'SmartHome1') AND category = 'Locks')),
     PRIMARY KEY (productID));
     
/*Table structure for table Items */

DROP TABLE IF EXISTS Item;
CREATE TABLE Item(  
     itemID    		CHAR(4)    	        NOT NULL UNIQUE,
     color        	VARCHAR(50)    		NOT NULL,
     factory    	VARCHAR(50)     	NOT NULL,
     powerSupply    	VARCHAR(50)  		NOT NULL,
     productionYear 	CHAR(4) 		        NOT NULL,
     model 		VARCHAR(50)  		NOT NULL,
     serviceStatus 	VARCHAR(50) 	    	,
     productID      	INT        NOT NULL,
     purchaseID     	INT            NOT NULL,
     CHECK(serviceStatus IN ("","Waiting for approval","In progress","Completed")),
	 PRIMARY KEY (itemID),
     FOREIGN KEY (productID) REFERENCES Product(productID) ON UPDATE CASCADE
                                                            ON DELETE CASCADE,
     FOREIGN KEY (purchaseID) REFERENCES Purchase(purchaseID) ON UPDATE CASCADE
							       ON DELETE CASCADE);

        
/*Table structure for table Requests */

DROP TABLE IF EXISTS Request;
CREATE TABLE Request(
     requestID	        INT       NOT NULL UNIQUE,
     requestFee         DOUBLE    NOT NULL,
     requestDate 	DATE      NOT NULL,
     requestStatus 	VARCHAR(50)   NOT NULL, 
     customerID 	INT       NOT NULL,
     adminID 		INT       NOT NULL,
     itemID 		CHAR(4)    NOT NULL,
     CHECK(requestStatus IN ('Submitted', 'Submitted and Waiting for payment', 'In progress', 'Approved' , 'Canceled','Completed')),
     PRIMARY KEY(requestID),
     FOREIGN KEY(customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE
                                                              ON DELETE CASCADE,
     FOREIGN KEY(adminID) REFERENCES Administrator(adminID) ON UPDATE CASCADE
                                                             ON DELETE CASCADE,
     FOREIGN KEY(itemID) REFERENCES Item(itemID) ON UPDATE CASCADE
						  ON DELETE CASCADE);

/*Table structure for table Payments */

DROP TABLE IF EXISTS Payment;
CREATE TABLE Payment(
    requestID 		INT 	NOT NULL UNIQUE,
    paymentDate 	DATE 	NOT NULL,
    paymentAmount 	DOUBLE 	NOT NULL,
    PRIMARY KEY(requestID),
    FOREIGN KEY(requestID) REFERENCES Request(requestID) ON UPDATE CASCADE
                                                           ON DELETE CASCADE);

