CREATE DATABASE RUCtronic;

USE RUCtronic;

CREATE TABLE Customer #买家
	(CustomerID VARCHAR(50) PRIMARY KEY,
	CustomerName VARCHAR(20),
	CustomerProfilePhoto VARCHAR(200),
	CustomerLV TINYINT,
	CustomerAddress VARCHAR(100),
	Province VARCHAR(20),
	CustomerBalance float(10,2),
	CustomerPassword VARCHAR(200),
	CustomerTELE VARCHAR(20),
	CustomerEmail VARCHAR(30)
	);

CREATE TABLE Seller #卖家
	(SellerID VARCHAR(20) PRIMARY KEY,
	SellerName VARCHAR(20),
	SellerLV TINYINT,
	SellerAddress VARCHAR(100),
	SellerTELE VARCHAR(20),
	SellerPassword VARCHAR(200)
	);

CREATE TABLE SalesPromotion #活动
	(SalesPromotionID VARCHAR(50) PRIMARY KEY,
	SalesPromotionName VARCHAR(20) ,
	SellerID VARCHAR(20),
	startdate DATE,
	enddate DATE,
	discount float(10,2),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
	);

CREATE TABLE Commodity  #商品
	(CommodityID VARCHAR(50) PRIMARY KEY,
	CommodityName VARCHAR(500),
	CommodityProfilePhoto VARCHAR(300),
	SellerID VARCHAR(20),
	SalesPromotionID VARCHAR(50),
	Commodity_description TEXT,
	CommodityInventory INTEGER,
	CommodityOriginalPrice float(10,2),
	CommodityPrice float(10,2),
	CommoditySalesVolume INTEGER,
	CommodityType TINYINT,
    Maxbuy int ,
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
	FOREIGN KEY (SalesPromotionID) REFERENCES SalesPromotion(SalesPromotionID)
	);

CREATE TABLE Orderform #订单
	(OrderID VARCHAR(200) PRIMARY KEY,
	SellerID VARCHAR(20),
	CommodityID VARCHAR(50),
	CustomerID VARCHAR(20),
	Quantity INTEGER,
	UnitPrice float(10,2),
	OrderDate DATE,
	OrderExpressNO VARCHAR(200),
	OrderState TINYINT,
	IsRating TINYINT,
	Rating TINYINT,
	Comment LONGTEXT,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
	FOREIGN KEY (CommodityID) REFERENCES Commodity(CommodityID)
	);

CREATE TABLE Visitor #游客
	(VisitorID VARCHAR(20) PRIMARY KEY
	);

CREATE TABLE Shoppingcart #购物车
	(CustomerID VARCHAR(20),
	CommodityID VARCHAR(50),
	CommodityQuantity INTEGER,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (CommodityID) REFERENCES Commodity(CommodityID),
	PRIMARY KEY(CustomerID,CommodityID)
	);

CREATE TABLE Favorites #收藏
	(CustomerID VARCHAR(20),
	CommodityID VARCHAR(50),
	FavoritesDate DATE,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (CommodityID) REFERENCES Commodity(CommodityID),
	PRIMARY KEY(CustomerID,CommodityID)
	);


CREATE TABLE Chats #聊天记录
	(CustomerID VARCHAR(20),
	SellerID VARCHAR(20),
	TextTime DATETIME,
	Content VARCHAR(2000),
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
	PRIMARY KEY(CustomerID,SellerID,TextTime)
	);
