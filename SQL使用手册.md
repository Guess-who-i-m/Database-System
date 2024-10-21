# SQL语言的使用手册

## 数据库相关

#### 创建数据库
```sql
CREATE DATABASE 数据库名称;
```

#### 删除数据库
```sql
DROP DATABASE 数据库名称;
```

#### 显示所有数据库
```sql
show databases;
```

#### 使用某一数据库
```sql
use 数据库名称;
```

#### 展示当前数据库的所有表
```sql
show tables;
```

#### 更改数据库字符集
```sql
ALTER DATABASE 数据库名称 DEFAULT CHARCTER SET 字符集名称;
```

## 表相关

#### 创建表
```sql
CREATE TABLE 表名(列名 类型[属性], 列名 类型[属性]……);  属性可省
```

#### 删除表
```sql
DROP TABLE 表名;
```

#### 添加列
```sql
ALTER TABLE 表名 ADD 列名 类型;
```

#### 删除列
```sql
ALTER TABLE 表名 DROP COLUMN 列名;
```

#### 展示表中的所有列
```sql
show columns from 表名;
```

#### 显示表中的所有数据
```sql
select * from 表名;
```

## 约束相关
MySQL中提供了四种约束，分别是
- 主键（PRIMARY KEY）：唯一标识每一行，每一行的主键不为空
- 外键（FOREIGN KEY）：定义两个表间的关系，一个表中的数据要与另一个表中的数据相匹配
- 非空约束（NOT NULL）：确保一个列或者多个列的值不为NULL
- 唯一约束（UNIQUE）：确保一个或者多个列的每个值都是唯一的，允许空值
- 检查约束（CHECK）：检查一个列中的值不超过某一个范围

#### 通过create创建包含约束的表
```sql
CREATE TABLE orders(
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

#### 通过ALTER …… ADD ……在创建表后添加约束
##### 添加主键约束

```sql
ALTER TABLE table_name ADD PRIMARY KEY (column_table);
```

##### 添加唯一约束
```sql
ALTER TABLE table_name ADD UNIQUE (column_name);
```

##### 添加外键约束
```sql
ALTER TABLE table_name ADD FOREIGN KEY (column_name) REFERENCES other_table_name (other_column_name);
```

## 数据相关

#### 添加数据
```sql
INSERT INTO 表名 VALUES(值, 值, 值……);  // 默认添加顺序就是列名顺序
```

#### 删除数据
```sql
DELETE FROM 表名 WHERE 条件;
```

#### 修改数据
```sql
UPDATE 表名 SET 列名 = 值 WHERE 条件;
```

## MySQL数据类型
### 数值类型
- INT 整数
- FLOAT 单精度浮点数
- DOUBLE 双精度浮点数
- DECIMAL 定点数，一般用于财务计算

### 日期和时间类型
- DATE 日期格式，格式为：YYYY-MM-DD
- TIME 时间类型，格式为：HH:MM:SS
- DATETIME 日期时间类型，格式为YY-MM-DD HH:MM:SS
- TIMESTAMP 时间戳类型，表示从1970年以来的秒数

### 字符串类型
- CHAR 固定长度字符串类型，最多255个字符
- VARCHAR 可变长度字符串类型，最多65535个字符
- TEXT 长文本类型，最多65535个字符
- ENUM 枚举类型，允许从预定义的值列表里选一个值
- SET 集合类型，允许从预定义的值集合里选择一个或者多个值

### 二进制类型
- BINARY 固定长度的二进制字符串类型
- VARBINARY 可变长度的二进制字符串类型
- BLOB 二进制大对象类型，用来存储大块的二进制数据

### 其他类型
- BOOL 布尔类型，可以存储True或者False
- JSON JSON数据类型，用于存储JSON格式的数据

## MySQL中的事务
MySQL提供了一系列的事务，利用BEGIN, COMMIT, ROLLBACK语句可以控制事务：
- BEGIN：启动事务
- COMMIT：提交事务
- ROLLBACK：回滚撤销事务

```sql
BEGIN； --开启事务

UPDATE accounts SET balance = balance - 1000 WHERE = 1;
UPDATE accounts SET balance = balance + 1000 WHERE = 999;  --无效的ID

ROLLBACK；  --回滚撤销事务
COMMIT;     --提交事务
```

## 一些查询语句的技巧

#### 连接查询

下面两个SQL查询等价
```sql
SELECT s
```