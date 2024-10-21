-- 创建数据库 
CREATE DATABASE company;
use company; 

-- 创建表
employee CREATE TABLE employee( 
    ename VARCHAR(10), 
    essn NCHAR(18) PRIMARY KEY , 
    address VARCHAR(30), 
    salary INT, 
    superssn NCHAR(18), 
    dno VARCHAR(3) 
); 

-- 创建表
department CREATE TABLE department( 
    dname VARCHAR(20), 
    dno VARCHAR(3) PRIMARY KEY,
    mgrssn NCHAR(18), 
    mrgstartdate DATE 
); 

-- 创建表
project CREATE TABLE project( 
    pname VARCHAR(20), 
    pno VARCHAR(3) PRIMARY KEY, 
    plocation VARCHAR(20), 
    dno VARCHAR(3) 
);
 -- 创建表
works_on CREATE TABLE works_on ( 
    essn VARCHAR(18), 
    pno VARCHAR(3), 
    hours INT PRIMARY KEY (essn, pno) 
);
