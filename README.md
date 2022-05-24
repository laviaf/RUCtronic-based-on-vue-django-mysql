## RUCtronic
本项目为《数据库系统概论》课程作业，项目名称为《RUCtronic旗舰店》。项目组以设计并实现一个类似京东、当当或亚马逊的网上B2C购物系统为目标，完成了用户需求分析、数据库概念设计、数据填充、图形化界面搭建、数据库安全性测试、分析性查询以及压力测试，基于vue+django+mysql实现。所给代码为数据填充为数据填充、图形化界面搭建及分析性查询部分代码，分别基于SQL语言与vue+django框架开发。项目成果已发布至b站https://www.bilibili.com/video/BV1sr4y1m7VS 。

### 平台角色及视图设定
平台将用户角色设定为买家、卖家与游客，并分别授予买家视图、卖家视图与游客视图。此外设置了商品、订单、满减活动与购物车实体以满足实际需求，并根据需要设置哈希索引以提高查询效率。在商品交易功能的基础上，为买家增加实现了商品加购、订单状态查询、退货、确认收货等功能，为买家增设了管理商品、管理满减活动、取消订单等功能。E-R图如下所示。

<div style="align: center">
  <img style="border-radius: 0.3125em;
  box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
  src="https://user-images.githubusercontent.com/65237103/170059974-cdeae2b3-3f20-4adb-9e55-0b62a407affd.png" width = "666" height = "428">
  <br>
</div>

### 数据填充
RUCtronic 旗舰店数据库填充数据基于来自Amazon review data(nijianmo.github.io)的数据(Ni et al,2019)改编而成。该数据集是2014 年发布的亚马逊评论数据集的更新版本。与上一个版本一样，这个数据集包括评论(评分、文本、帮助投票)、产品数据(描述、类别信息、价格、品牌和图像功能)。
RUCtronic 项目组下载了该数据集下Electronic 分类中的reviews(20,994,353 reviews)和metadata(786,868 products)数据，并通过Python中的Faker实现了各类编号、日期、地址的随机生成，合并后填入数据库的商品、卖家和买家表。随后，RUCtronic项目组综合利用了重复采样的随机方法，从商品表、买家表和买家表中随机有放回抽取子集，按照数据语义合并后作为购物车等其他表的数据进行填充。

### django
django主要根据url及请求中的参数建立视图的映射关系。本项目组在apps中设置Adiministrator, Customer, Seller以对应管理员、买家、卖家三种角色，并通过django为每个用户赋予不同的权限（在最开始建立视图时，本项目组仅针对买家与卖家建立了两种视图，在django针对每个用户进一步细分权限）。对于买家和卖家，在登录时赋予token参数。

urls.py对前端返回的url进行重映射。views.py中实现主体功能函数。

### vue
vue参照cmh1996给出的模板实现:https://github.com/cmh1996/vue-mall 。非常感谢该作者，该项目模板极大程度上帮助了我们理解vue前端的工作原理并快速上手java及css。

最后，该项目仅供参考，希望能够对师弟师妹们有所帮助。
