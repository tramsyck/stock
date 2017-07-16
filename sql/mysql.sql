create database stock;
use stock;

create table stocks(id int auto_increment primary key,
 stockid varchar(20),
 name varchar(20));

create table dayinfo(id int AUTO_INCREMENT PRIMARY KEY, stockid VARCHAR(20),
today_start_price FLOAT,
lowest_price FLOAT,
 hight_price FLOAT,
 deal_mount BIGINT,
 deal_money FLOAT,
 change FLOAT,
 flow_market_value FLOAT,
 total_market_value DEFAULT,
 info_date date
)