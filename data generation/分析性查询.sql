#a)显示每个商家(以卖家S1343174563为例）最热卖的top3商品
SELECT sid,cid1,csv1
FROM (SELECT c1.SellerID sid, c1.CommodityID cid1, c2.CommodityID cid2, c1.CommoditySalesVolume csv1, c2.CommoditySalesVolume csv2
FROM commodity AS c1 LEFT JOIN commodity AS c2 ON c1.SellerID = c2.SellerID
WHERE c1.CommoditySalesVolume < c2.CommoditySalesVolume) cc
GROUP BY cid1
HAVING COUNT(*) <= 3
ORDER BY sid,csv1 DESC

#b)给定一个商品，显示售卖此商品价格最低的5个卖家
select seller.SellerID,seller.SellerName
from commodity, seller
where commodity.SellerID=seller.SellerID and
      CommodityName LIKE '输入商品的名字'
ORDER BY	CommodityPrice
limit 0,5;

#c)显示每个商家的年销售总额
select SellerID, SellerIncome
from Seller
ORDER BY SellerIncome DESC


#d)显示每个会员购买次数最多的商品
SELECT sid,cid1,csv1
FROM (SELECT c1.CustomerID cuid, c1.CommodityID cid1, c2.CommodityID cid2, count(CommodityID) ccid1, count(CommodityID) ccid2
FROM orderform AS c1 LEFT JOIN orderform AS c2 ON c1.CustomerID = c2.CustomerID
WHERE c1.count(co < c2.CommoditySalesVolume) cc
GROUP BY cid1
HAVING COUNT(*) <= 3
ORDER BY sid,csv1 DESC






SELECT cbc1.CustomerID, cbc1.CommodityID, cbc2.CustomerID, cbc2.CommodityID
FROM (SELECT CustomerID,CommodityID, COUNT(*) num
	FROM orderform
	GROUP BY CustomerID,CommodityID
	ORDER BY CustomerID) cbc1 LEFT JOIN cbc1 as cbc2 ON cbc1.CustomerID = cbc2.CustomerID







select CustomerID, CommodityID
from 
(SELECT CustomerID, CommodityID, count(CommodityID) as 'Number of buying'
from orderform
GROUP BY CustomerID,CommodityID
ORDER BY count(CommodityID) DESC
)n
GROUP BY CustomerID
where CustomerID='A00126503SUWI86KZBMIN'
limit 0,1;



#e)显示每个省份的会员的平均消费额、最大消费额和最小消费额，并按平均消费额降序排列
SELECT province, round(avg(UnitPrice*Quantity),2) AS 'Average consumption', round(MAX(UnitPrice*Quantity),2) as 'Maximum consumption', round(MIN(UnitPrice*Quantity),2) as 'Minimum consumption'
from customer,orderform
where customer.customerID=orderform.CustomerID
group by province
order by AVG(UnitPrice*Quantity) DESC

