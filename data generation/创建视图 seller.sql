CREATE view view_visitor_seller
as
SELECT SellerID, SellerName, SellerLV, SellerAddress, SellerTELE
FROM seller;

CREATE VIEW view_visitor_SalesPromotion
as
SELECT *
from SalesPromotion;

CREATE VIEW view_visitor_commodity
as
SELECT *
from commodity;