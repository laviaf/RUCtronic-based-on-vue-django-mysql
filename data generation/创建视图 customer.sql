CREATE VIEW view_customer_customer
as
select *
from customer;

CREATE VIEW view_customer_favorites
as
select *
from favorites;

CREATE VIEW view_customer_orderform
as
select *
from orderform;

CREATE VIEW view_customer_shoppingcart
as
SELECT *
FROM shoppingcart;

CREATE VIEW view_customer_chats
as
SELECT *
FROM chats;

CREATE VIEW view_customer_commodity
as
SELECT *
FROM commodity;

CREATE VIEW view_customer_salespromotion
as
SELECT *
FROM salespromotion;

CREATE VIEW view_customer_seller
as
SELECT SellerID, SellerName, SellerLV, SellerAddress, SellerTELE
FROM seller;


