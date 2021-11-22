CREATE DATABASE onlineshoppingmall;

USE onlineshoppingmall;

CREATE TABLE Customer #买家
	(CustomerID VARCHAR(20) PRIMARY KEY,
	CustomerName VARCHAR(100) UNIQUE,
	CustomerProfilePhoto VARCHAR(100),
	CustomerLV VARCHAR(10),
	CustomerAddress VARCHAR(100),
	CustomerBalance INTEGER,
	CustomerPassword VARCHAR(100),
	CustomerTELE VARCHAR(100)
	);

CREATE TABLE Seller #卖家
	(SellerID VARCHAR(20) PRIMARY KEY,
	SellerName VARCHAR(100) UNIQUE,
	SellerLV VARCHAR(10),
	SellerAddress VARCHAR(100),
	SellerTELE VARCHAR(100),
	SellerPassword VARCHAR(100)
	);

CREATE TABLE SalesPromotion #活动
	(SalesPromotionID VARCHAR(20) PRIMARY KEY,
	SalesPromotionName VARCHAR(100) UNIQUE,
	SellerID VARCHAR(20),
	startdate DATE,
	enddate DATE,
	SalesPromotion_description VARCHAR(200),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
	);

CREATE TABLE Commodity  #商品
	(CommodityID VARCHAR(20) PRIMARY KEY,
	CommodityName VARCHAR(100) UNIQUE,
	CommodityProfilePhoto VARCHAR(100),
	SellerID VARCHAR(20),
	SalesPromotionID VARCHAR(20),
	Commodity_description VARCHAR(200),
	CommodityInventory INTEGER,
	CommodityOriginalPrice INTEGER,
	CommodityPrice INTEGER,
	CommoditySalesVolume INTEGER,
	CommodityType VARCHAR(20),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
	FOREIGN KEY (SalesPromotionID) REFERENCES SalesPromotion(SalesPromotionID)
	);

CREATE TABLE Orderform #订单
	(OrderID VARCHAR(20) PRIMARY KEY,
	SellerID VARCHAR(20),
	CommodityID VARCHAR(20),
	CustomerID VARCHAR(20),
	Quantity INTEGER,
	UnitPrice DOUBLE,
	OrderDate DATE,
	OrderExpressNO VARCHAR(20),
	OrderState VARCHAR(20),
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
	FOREIGN KEY (CommodityID) REFERENCES Commodity(CommodityID)
	);

CREATE TABLE Visitor #游客
	(VisitorID VARCHAR(20) PRIMARY KEY
	);

CREATE TABLE Shoppingcart #购物车
	(CustomerID VARCHAR(20),
	CommodityID VARCHAR(20),
	CommodityQuantity INTEGER,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (CommodityID) REFERENCES Commodity(CommodityID),
	PRIMARY KEY(CustomerID,CommodityID)
	);

CREATE TABLE Favorites #收藏
	(CustomerID VARCHAR(20),
	CommodityID VARCHAR(20),
	FavoritesDate DATE,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (CommodityID) REFERENCES Commodity(CommodityID),
	PRIMARY KEY(CustomerID,CommodityID)
	);

CREATE TABLE Purchased #购买历史
	(OrderID VARCHAR(20) PRIMARY KEY,
	Comment VARCHAR(200),
	Rating VARCHAR(10),
	PurchasedState VARCHAR(10),
	FOREIGN KEY (OrderID) REFERENCES Orderform(OrderID)
	);

CREATE TABLE Chats #聊天记录
	(CustomerID VARCHAR(20),
	SellerID VARCHAR(20),
	TextTime DATETIME,
	Content VARCHAR(200),
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
	PRIMARY KEY(CustomerID,SellerID,TextTime)
	);