GRANT ALL on view_seller_chats
TO role_seller;

GRANT ALL ON view_seller_seller
to role_seller;

GRANT select ON view_seller_customer
to role_seller;

grant all on view_seller_commodity
to role_seller;

grant INSERT (OrderID, SellerID, commodityid, UnitPrice, orderdate, OrderExpressNO, OrderState) on view_seller_orderform
to role_seller;

grant update (OrderID, SellerID, commodityid, UnitPrice, orderdate, OrderExpressNO, OrderState) on view_seller_orderform
to role_seller;

grant DELETE on orderform
to role_seller;

grant SELECT(customerid, quantity, IsRating, Rating, COMMENT) on view_seller_orderform
to role_seller;

grant all on view_seller_salespromotion
to role_seller;