--1 �˿ͱ�
CREATE TABLE T_Customer (
  customerid CHAR(15) NOT NULL UNIQUE,
  customername VARCHAR(20) NOT NULL UNIQUE,
  gender CHAR(1) NOT NULL,
  age INT NOT NULL,
  customerbalance DECIMAL(12,2) NULL,
  paymentcode VARCHAR(10) NOT NULL,
  phonenumber VARCHAR(20) NOT NULL,
  customerprovince CHAR(10) NULL,
  customeraddress VARCHAR(50) NULL,
  customericon VARCHAR(50) NULL,
  PRIMARY KEY (customerid,customername));
  /*
  INSERT INTO T_Customer VALUES('c201804281545','fangjy','1',21,999.99,'785203','13719221569','�㶫','��ϸ��ַ','/web/images/fangjyicon.png')
  INSERT INTO T_Customer VALUES('c201804281547','dima Bilan','1',30,888.88,'456123','15236587495','�㶫','��ϸ��ַ','/web/images/dimabilanicon.png')
  INSERT INTO T_Customer VALUES('c201804281549','Amy','0',25,852,'458964','13714562389','�㶫','��ϸ��ַ','/web/images/fangjyicon.png')
  INSERT INTO T_Customer VALUES('c201804281550','David','1',23,892,'555666','13714562389','����','��ϸ��ַ','/web/images/fangjyicon.png')
  INSERT INTO T_Customer VALUES('c201804281551','caron','0',30,1520,'777888','13714562389','�Ĵ�','��ϸ��ַ','/web/images/fangjyicon.png')

  select * from T_Customer*/
  
  --2 �̼ұ�
  drop table T_Merchant
  CREATE TABLE T_Merchant (
  merchantid CHAR(15) NOT NULL UNIQUE,
  merchantname VARCHAR(20) NOT NULL UNIQUE,
  merchanttype VARCHAR(10) NOT NULL,
  merchantbalance DECIMAL(12,2) NULL,
  merchantdescribe VARCHAR(50) NULL,
  merchantstatement CHAR(2) NULL,
  merchantprovince CHAR(10) NULL,
  merchantaddress VARCHAR(50) NULL,
  merchanticon VARCHAR(50) NULL,
  remark VARCHAR(50) NULL,
  PRIMARY KEY (merchantid));
  /*
  INSERT INTO T_Merchant VALUES('b201804281558','ˮ����','7',5555.5,'������õ�ˮ����������','1','�㶫','��ϸ��ַ','/web/image.png','');
  INSERT INTO T_Merchant VALUES('b201804281604','�θ��С��','1',9999.9,'û�м����ķ�װ��','1','�㶫','��ϸ��ַ','/web/image.png','');
  INSERT INTO T_Merchant VALUES('b201804281606','�����˵����','2',8888,'��Ҫ�������Ƕ���','2','����','��ϸ��ַ','/web/image.png','��˲�ͨ����ԭ��');
  
  select * from T_Merchant*/
  
  --3 ����Ա��
  CREATE TABLE T_Manager(
  managerid CHAR(15) NOT NULL UNIQUE,
  managername VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (managerid));
  
  --4 �����
  CREATE TABLE T_Cryptogram (
  userid CHAR(15) NOT NULL UNIQUE,
  password VARCHAR(12) NOT NULL,
  answer VARCHAR(50) NOT NULL,
  role INT NOT NULL,--0����Ա��1�˿ͣ�2�̼�
  PRIMARY KEY (userid));
  
  INSERT INTO T_Cryptogram VALUES('c201804281545','123456','2018',1);
  INSERT INTO T_Cryptogram VALUES('b201804281558','1234567','2017',2);
  INSERT INTO T_Cryptogram VALUES('b201804281606','12345678','2016',2);
  
  SELECT * FROM T_Cryptogram
  
  
  --5 ��Ʒ��
CREATE TABLE T_Product (
  productid CHAR(15) NOT NULL UNIQUE,
  productname VARCHAR(50) NOT NULL,
  productdescribe VARCHAR(80) NOT NULL,
  discount DECIMAL(4,2) NULL DEFAULT 1.0,
  delivery CHAR(2) NULL,
  producttype VARCHAR(10) NOT NULL,
  merchantid CHAR(15) NOT NULL,
  productimage VARCHAR(50) NOT NULL,
  price DECIMAL(7,2) NOT NULL,
  productstatement CHAR(2) NOT NULL,
  productdate DATE NOT NULL,
  recommend INT NOT NULL DEFAULT 0,
  recommendprice DECIMAL(12,2) NULL,
  PRIMARY KEY (productid));
  select * from T_Product where productdescribe like '%��%'
/*
 -- delete from T_Product
 drop table T_Product
  INSERT INTO T_Product VALUES('p201804281556','ƻ��','ƻ��',0.98,'1','7','b201804281558','/web/imag.png',5.2,'1','2018/04/28',1,0.1);
  INSERT INTO T_Product VALUES('p201804281609','�㽶','��ɫ���㽶',1.0,'1','7','b201804281558','/web/imag.png',4.5,'1','2018/04/28',1,0.1);
  INSERT INTO T_Product VALUES('p201804281610','������','��ɫ�ĺ�����',0.9,'1','7','b201804281558','/web/imag.png',3.8,'1','2018/04/28',1,0.2);
  INSERT INTO T_Product VALUES('p201804281611','��','��Բ����',0.98,'1','7','b201804281558','/web/imag.png',5.2,'1','2018/04/28',1,0.1);
 
 INSERT INTO T_Product VALUES('p201804281617','ñ��','��ɫ��ñ��',1,'1','1','b201804281604','/web/imag.png',32,'1','2018/04/25',1,0.2);
 INSERT INTO T_Product VALUES('p201804281618','����','��ɫ�Ķ���',0.98,'1','1','b201804281604','/web/imag.png',88.8,'1','2018/2/28',1,0.2);
 INSERT INTO T_Product VALUES('p201804281619','ţ�п�','��ɫ�ش�ţ�п�',0.95,'1','1','b201804281604','/web/imag.png',99.9,'1','2018/03/28',1,0.1);
 INSERT INTO T_Product VALUES('p201804281620','�˶�Ь','�˶���Ь��',0.85,'1','1','b201804281604','/web/imag.png',200,'1','2018/03/29',0,0.1);
 INSERT INTO T_Product VALUES('p201805142311','�˶�Ь','�˶���Ь��',0.85,'1','1','b201804281604','/web/imag.png',200,'1','2018/03/29',0,0.1);
 
 INSERT INTO T_Product VALUES('p201805142344','t��','Ī�����޶�����ʿt������ɫv���������·�������װ�����˿������',0.85,'1','1','b201804281604','/web/imag.png',200,'1','2018/03/29',0,0.1);
 
  select * from T_Product */
  
  select * from T_Index i,T_Keyword k where i.keywordid = k.keywordid
  select * from T_Keyword
  delete from T_Keyword where keywordid = 'k20180507215104' or keywordid = 'k20180514232315'
  delete from T_Index where productid = 'p201804281619'
  UPDATE T_Product SET recommend=1,recommendprice=0.2 WHERE productid='p201804281556'
  
  SELECT  FROM T_Index i,(SELECT keywordid,keyword FROM T_Keyword) k 
  WHERE i.keywordid = k.keywordid and k.keyword like '%����%'
  
  --6 ͼƬ��
  CREATE TABLE T_Image(
  imageid INT NOT NULL,
  imageurl VARCHAR(100) NOT NULL,
  productid VARCHAR(15) NOT NULL,
  PRIMARY KEY (imageid,productid));
  
  INSERT INTO T_Image VALUES(1,'pic1.png','p201804281618');
  INSERT INTO T_Image VALUES(2,'pic2.png','p201804281618');
  INSERT INTO T_Image VALUES(3,'pic3.png','p201804281618');
  INSERT INTO T_Image VALUES(1,'pic4.png','p201804281556');
  INSERT INTO T_Image VALUES(2,'pic5.png','p201804281556');

  --7 ���Ա�
  CREATE TABLE T_Attribute (
  producttype VARCHAR(10) NOT NULL,
  attributeid VARCHAR(4) NOT NULL,
  attributename VARCHAR(10) NULL,
  PRIMARY KEY (producttype,attributeid));
 
 /*
INSERT INTO T_Attribute VALUES('1', 'a101','��ɫ');
INSERT INTO T_Attribute VALUES('1', 'a102','�ߴ�');
INSERT INTO T_Attribute VALUES('7', 'a701','��ɫ');

select * from T_Attribute*/

  --8 ��Ʒ���Ա�
  CREATE TABLE T_Productattribute(
  productid CHAR(15) NOT NULL,
  attributeid VARCHAR(4) NOT NULL,
  attribute VARCHAR(10) NOT NULL,
  storeid CHAR(15) NOT NULL,
  PRIMARY KEY (productid, attributeid, attribute, storeid));
  
  /*
  INSERT INTO T_Productattribute VALUES('p201804281556','a701','��ɫ','s20180428155601');
  INSERT INTO T_Productattribute VALUES('p201804281609','a701','��ɫ','s20180428160901');
  INSERT INTO T_Productattribute VALUES('p201804281610','a701','��ɫ','s20180428161001');
  INSERT INTO T_Productattribute VALUES('p201804281611','a701','��Բ','s20180428161101');
  
  INSERT INTO T_Productattribute VALUES('p201804281617','a101','��ɫ','s20180428161701');--��ɫ��ñ��
  INSERT INTO T_Productattribute VALUES('p201804281617','a101','��ɫ','s20180428161702');--��ɫ��ñ��
  
  INSERT INTO T_Productattribute VALUES('p201804281618','a101','��ɫ','s20180428161801');--��ɫС�ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a102','С��','s20180428161801');--��ɫС�ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a101','��ɫ','s20180428161802');--��ɫ��ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a102','���','s20180428161802');--��ɫ��ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a101','��ɫ','s20180428161803');--��ɫС�ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a102','С��','s20180428161803');--��ɫС�ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a101','��ɫ','s20180428161804');--��ɫС�ŵĶ���
  INSERT INTO T_Productattribute VALUES('p201804281618','a102','���','s20180428161804');--��ɫС�ŵĶ���
  
  INSERT INTO T_Productattribute VALUES('p201804281619','a101','��ɫ','s20180428161901');--��ɫ��ţ�п�
  INSERT INTO T_Productattribute VALUES('p201804281619','a101','��ɫ','s20180428161902');--��ɫ��ţ�п�
  
  INSERT INTO T_Productattribute VALUES('p201804281620','a101','��ɫ','s20180428162001');--��ɫ���˶�Ь
  INSERT INTO T_Productattribute VALUES('p201804281620','a101','��ɫ','s20180428162002');--��ɫ���˶�Ь
  
  SELECT * FROM T_Productattribute*/
  
  --9 ����
  
  CREATE TABLE T_Store (
  storeid CHAR(15) NOT NULL UNIQUE,
  storage INT NOT NULL,
  PRIMARY KEY (storeid));
  
  /*
  INSERT INTO T_Store(storeid,storage) SELECT distinct(storeid),100 FROM T_Productattribute
  INSERT INTO T_Store(storeid,storage) VALUES('s20180428155603',50)
  
  SELECT * FROM T_Store*/
  
  --10 ���ﳵ
  
  CREATE TABLE T_Shoppingcart (
  cartid CHAR(15) NOT NULL,
  customerid CHAR(15) NOT NULL,
  storeid CHAR(15) NOT NULL,
  quantity INT NOT NULL,
  shoppingcarttotal DECIMAL(12,2) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (cartid);
  
  /*
  select * from T_Shoppingcart
  INSERT INTO T_Shoppingcart VALUES('c201804281545','s20180428161803',1,88.8,'2018-4-30')
  INSERT INTO T_Shoppingcart VALUES('c201804281545','s20180428162002',1,300,'2018-4-30')
  INSERT INTO T_Shoppingcart VALUES('c201804281545','s20180428161001',5,52.2,'2018-4-30')
  INSERT INTO T_Shoppingcart VALUES('c201804281545','s20180428155603',3,22.2,'2018-4-30')
  
  delete from T_Shoppingcart WHERE customerid = 'c201804281545' and storeid = 's20180428164501'*/
  
  --11 ������
  drop table T_Order
  CREATE TABLE T_Order(
  orderid CHAR(15) NOT NULL UNIQUE,
  customerid CHAR(15) NOT NULL,
  ordercondition VARCHAR(12) NOT NULL,
  orderdate DATE NOT NULL,
  PRIMARY KEY (orderid));
  
   --12 �������
 CREATE TABLE T_Orderitem(
    orderid CHAR(15) NOT NULL,
    storeid CHAR(15) NOT NULL,
    quantity INT NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    PRIMARY KEY(storeid,orderid));
  /*
--delete from T_Order

SELECT * FROM T_Order o,T_Orderitem oi where o.orderid=oi.orderid order by orderdate DESC; 
SELECT * FROM T_Order where orderid = 'o20180503222401' order by orderdate DESC;
SELECT * FROM T_Orderitem where orderid = 'o20180503222401'
delete from T_Order where orderid = 'o20180503235751';
delete from T_Orderitem where orderid ='o20180503235751'

INSERT INTO T_Order VALUES('o20180503222401','c201804281545','3','2018/04/01');
INSERT INTO T_Orderitem VALUES('o20180503222401','s20180428155601',9,55.5);
INSERT INTO T_Orderitem VALUES('o20180503222401','s20180428161803',9,55.5);
INSERT INTO T_Order VALUES('o20180503222805','c201804281545','3','2018/04/02');
INSERT INTO T_Orderitem VALUES('o20180503222805','s20180428160901',8,43.5);
INSERT INTO T_Order VALUES('o20180503223255','c201804281545','3','2018/04/02');
INSERT INTO T_Orderitem VALUES('o20180503223255','s20180428161001',9,55.5);
INSERT INTO T_Order VALUES('o20180503223356','c201804281545','3','2018/04/03');
INSERT INTO T_Orderitem VALUES('o20180503223356','s20180428161101',9,55.5);

INSERT INTO T_Order VALUES('o20180503223458','c201804281547','3','2018/04/10');
INSERT INTO T_Orderitem VALUES('o20180503223458','s20180428161701',9,55.5);
INSERT INTO T_Order VALUES('o20180503223545','c201804281547','3','2018/04/15');
INSERT INTO T_Orderitem VALUES('o20180503223545','s20180428161804',9,55.5);
INSERT INTO T_Order VALUES('o20180503223689','c201804281547','3','2018/04/12');
INSERT INTO T_Orderitem VALUES('o20180503223689','s20180428161901',9,55.5);
INSERT INTO T_Order VALUES('o20180503223785','c201804281547','3','2018/04/05');
INSERT INTO T_Orderitem VALUES('o20180503223785','s20180428162002',9,55.5);

INSERT INTO T_Order VALUES('o20180503223901','c201804281549','3','2018/04/15');
INSERT INTO T_Orderitem VALUES('o20180503223901','s20180428155601',9,55.5);
INSERT INTO T_Order VALUES('o20180503223902','c201804281549','3','2018/04/15');
INSERT INTO T_Orderitem VALUES('o20180503223902','s20180428161001',9,55.5);
INSERT INTO T_Order VALUES('o20180503224103','c201804281549','3','2018/04/18');
INSERT INTO T_Orderitem VALUES('o20180503224103','s20180428161702',9,55.5);
INSERT INTO T_Order VALUES('o20180503224204','c201804281549','3','2018/04/17');
INSERT INTO T_Orderitem VALUES('o20180503224204','s20180428160901',9,55.5);
INSERT INTO T_Order VALUES('o20180503224205','c201804281549','3','2018/04/20');
INSERT INTO T_Orderitem VALUES('o20180503224205','s20180428161902',9,55.5);

INSERT INTO T_Order VALUES('o20180503224406','c201804281550','3','2018/04/08');
INSERT INTO T_Orderitem VALUES('o20180503224406','s20180428161101',9,55.5);
INSERT INTO T_Order VALUES('o20180503224407','c201804281550','3','2018/04/08');
INSERT INTO T_Orderitem VALUES('o20180503224407','s20180428161801',9,55.5);
INSERT INTO T_Order VALUES('o20180503224408','c201804281550','3','2018/04/05');
INSERT INTO T_Orderitem VALUES('o20180503224408','s20180428161901',9,55.5);
INSERT INTO T_Order VALUES('o20180503224409','c201804281550','3','2018/04/10');
INSERT INTO T_Orderitem VALUES('o20180503224409','s20180428162001',9,55.5);

INSERT INTO T_Order VALUES('o20180503224410','c201804281551','3','2018/04/20');
INSERT INTO T_Orderitem VALUES('o20180503224410','s20180428161902',9,55.5);
INSERT INTO T_Order VALUES('o20180503224411','c201804281551','3','2018/04/23');
INSERT INTO T_Orderitem VALUES('o20180503224411','s20180428161101',9,55.5);
INSERT INTO T_Order VALUES('o20180503224412','c201804281551','3','2018/04/07');
INSERT INTO T_Orderitem VALUES('o20180503224412','s20180428161803',9,55.5);

select * from T_Order,T_Store where T_Order.storeid = T_Store.storeid
SELECT * FROM T_Order
INSERT INTO T_Order(orderid,customerid,storeid,ordercondition,quantity,
            orderdate,total) VALUES ('o20180430163249','c201804281545','s20180428161801','0',2,'2018-04-30',174.048)
 */
 
SELECT o.customerid,oi.storeid,o.orderdate FROM T_Order o,T_Orderitem oi 
WHERE o.orderid = oi.orderid and o.ordercondition='3' ORDER BY o.orderdate
 
 --13 ������Ϣ��
 CREATE TABLE T_Chat (
  chatid INT NOT NULL UNIQUE AUTO_INCREMENT,
  from CHAR(15) NOT NULL,
  to CHAR(15) NOT NULL,
  chatrecorder VARCHAR(200) NOT NULL,
  chatstatement VARCHAR(12) NOT NULL,
  PRIMARY KEY (chatid));
  
 --14 ��Ʒ���۱�
 CREATE TABLE T_Remark(
  customerid CHAR(15) NOT NULL,
  productid CHAR(15) NOT NULL,
  level INT NOT NULL,
  comment VARCHAR(400) NULL,
  PRIMARY KEY (customerid, productid));
  
  INSERT INTO T_Remark VALUES('c201804281545','p201804281618',4,'�·��ܺÿ�');
  INSERT INTO T_Remark VALUES('c201804281547','p201804281618',3,'һ��');
  INSERT INTO T_Remark VALUES('c201804281545','p201804281556',4,'����');
  INSERT INTO T_Remark VALUES('c201804281551','p201804281556',4,'��������һ��');
  
  SELECT c.customername,c.customericon,r.level,r.comment FROM T_Remark r,        
  (SELECT customerid,customername,customericon FROM T_Customer) c     
  WHERE r.customerid = c.customerid and r.productid='p201804281618' 
  
  SELECT * FROM T_Remark r,T_Customer c where r.customerid = c.customerid
 --15 �ؼ��ֱ�
 drop table T_Keyword
 CREATE TABLE T_Keyword(
  keywordid CHAR(15) NOT NULL UNIQUE ,
  keyword VARCHAR(10) NOT NULL UNIQUE,
  keywordtype INT NOT NULL,--0-�ƹ�ؼ��֣�1-����
  PRIMARY KEY (keywordid));
 
 SELECT * FROM T_Keyword
 
 INSERT INTO T_Keyword VALUES('k20180507215101','����',0);
  INSERT INTO T_Keyword VALUES('k20180507215111','����',0);
 INSERT INTO T_Keyword VALUES('k20180507215102','����',0);
 INSERT INTO T_Keyword VALUES('k20180507215103','�¿�',0);
 INSERT INTO T_Keyword VALUES('k20180507215104','����',1);
 INSERT INTO T_Keyword VALUES('k20180507215105','��װ',1);
 
 
 
 --16 ������
 CREATE TABLE T_Index (
  productid CHAR(15) NOT NULL,
  keywordid CHAR(15) NOT NULL,
  price DECIMAL(12,2) NOT NULL DEFAULT 0.01,
  weight DECIMAL(12,2) NOT NULL,
  PRIMARY KEY (productid, keywordid));
 
 INSERT INTO T_Index VALUES('p201804281618','k20180507215103',0.05,0.4);
 INSERT INTO T_Index VALUES('p201804281618','k20180507215105',0.01,0.3);
 INSERT INTO T_Index VALUES('p201804281618','k20180507215101',0.01,0.4);
 
 INSERT INTO T_Index VALUES('p201804281619','k20180507215105',0.01,0.3);
 
 SELECT * FROM T_Index i,T_Keyword k WHERE i.keywordid = k.keywordid;
 
 --17 ͷ����
 drop table T_Headline 
 CREATE TABLE T_Headline (
  productid CHAR(15) NOT NULL,
  image VARCHAR(50) NOT NULL,
  price DECIMAL(12,2) NOT NULL,
  date DATE NOT NULL,
  statement INT NOT NULL,
  PRIMARY KEY (productid));
  
  SELECT * FROM T_Headline
  INSERT INTO T_Headline VALUES('p201804281556','web/apple.png',9.9,'2018-5-6',0);
  
  SELECT productid,price,statement FROM T_Headline WHERE productid in
(SELECT productid FROM T_Product where merchantid='b201804281558')
  
 --18 ��Ʒ���ƶȱ�
 CREATE TABLE T_Itemsimilarity(
	productid1 CHAR(15) NOT NULL,
	productid2 CHAR(15) NOT NULL,
	similarity DECIMAL(8,6) NOT NULL,
	PRIMARY KEY(productid1,productid2)
 );
  select * from T_Itemsimilarity
  
 --19 �û�ϲ�ñ�
 drop table T_Customertaste
 CREATE TABLE T_Customertaste(
	customerid CHAR(15) NOT NULL,
	productid CHAR(15) NOT NULL,
	taste INT NOT NULL,--0��ʾ��ϲ����1��ʾϲ��
	date DATE NOT NULL,
	PRIMARY KEY(customerid,productid));
 
 INSERT INTO T_Customertaste VALUES('c201804281545','p201804281556',1,'2018-5-5');
 INSERT INTO T_Customertaste VALUES('c201804281545','p201804281611',0,'2018-5-5');

 SELECT * FROM T_Customertaste
 UPDATE T_Customertaste SET taste = 1 WHERE customerid = 'c201804281545' and productid='p201804281556'
 INSERT INTO T_Itemsimilarity VALUES('p201804281618', 'p201804281617', 0.06804138174397717)
 SELECT o.customerid,pa.productid,o.orderdate
             FROM T_Order o,(SELECT productid,storeid FROM T_Productattribute) pa
             WHERE o.storeid = pa.storeid
             
SELECT distinct(productid,storeid) FROM T_Productattribute

SELECT storeid,orderdate FROM T_Order WHERE customerid=c201804281551

p201804281618
[{"attrname":"��ɫ","attrvalue":"��ɫ"},{"attridname":"�ߴ�","attrvalue":"С��"}]

SELECT pa.storeid FROM T_ProductAttribute pa,
	(SELECT p.productid,a.attributeid FROM T_Product p,T_Attribute a
		WHERE p.producttype = a.producttype and p.productid = 'p201804281618' and a.attributename='��ɫ') m
	WHERE pa.productid = m.productid and pa.attributeid = m.attributeid and pa.attribute='��ɫ'
	
SELECT pa.storeid FROM T_ProductAttribute pa,
	(SELECT p.productid,a.attributeid FROM T_Product p,T_Attribute a
		WHERE p.producttype = a.producttype and p.productid = 'p201804281618' and a.attributename='�ߴ�') m
	WHERE pa.productid = m.productid and pa.attributeid = m.attributeid and pa.attribute='С��'
	

SELECT orderid,customerid,storeid,ordercondition,quantity,total,orderdate FROM T_Order 
WHERE storeid in
(SELECT distinct(pa.storeid) FROM T_Productattribute pa,T_Product p 
	WHERE pa.productid=p.productid and p.merchantid='b201804281558')

SELECT pa.storeid FROM T_ProductAttribute pa,
	(SELECT p.productid,a.attributeid FROM T_Product p,T_Attribute a
     WHERE p.producttype = a.producttype and p.productid = 'p201804281618' and a.attributename='��ɫ') m
     WHERE pa.productid = m.productid and pa.attributeid = m.attributeid and pa.attribute='��ɫ'
     

SELECT o.orderid,o.customerid,oi.storeid,o.ordercondition,oi.quantity,oi.total,o.orderdate 
FROM T_Order o,T_Orderitem oi 
WHERE o.orderid=oi.orderid and o.customerid='c201804281545'
SELECT o.orderid,o.customerid,oi.storeid,o.ordercondition,oi.quantity,oi.total,o.orderdate 
FROM T_Order o,T_Orderitem oi          
WHERE o.orderid=oi.orderid and o.customerid='c201804281545' and o.ordercondition='3'
SELECT o.orderid,o.customerid,oi.storeid,o.ordercondition,oi.quantity,oi.total,o.orderdate 
FROM T_Order o,T_Orderitem oi       
WHERE o.orderid=oi.orderid and o.customerid='c201804281545' and o.orderid='o20180503222401'

SELECT o.orderid,o.customerid,oi.storeid,o.ordercondition,oi.quantity,oi.total,o.orderdate 
FROM T_Order o,T_Orderitem oi           
WHERE o.orderid = oi.orderid and oi.storeid in             
	(SELECT distinct(pa.storeid) FROM T_Productattribute pa,T_Product p            
	WHERE pa.productid=p.productid and p.merchantid='b201804281558')

SELECT k.keywordid,k.keyword,count(distinct i.productid) num
FROM T_Keyword k,T_Index i
WHERE k.keywordid = i.keywordid
GROUP BY k.keywordid,k.keyword
ORDER BY num DESC;

SELECT * FROM T_Index

SELECT * FROM T_Order o,T_Orderitem oi 
WHERE o.orderid = oi.orderid and oi.storeid like 's201804281619%' and o.ordercondition = '3'