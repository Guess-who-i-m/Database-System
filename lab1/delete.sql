-- 禁用外键约束
SET FOREIGN_KEY_CHECKS = 0;

-- 删除罚款记录表中的所有数据
DELETE FROM fine;

-- 删除借阅记录表中的所有数据
DELETE FROM record;

-- 删除图书-作者关系表中的所有数据
DELETE FROM book_author;

-- 删除图书表中的所有数据
DELETE FROM book;

-- 删除作者表中的所有数据
DELETE FROM author;

-- 删除会员表中的所有数据
DELETE FROM member;

-- 删除管理员表中的所有数据
DELETE FROM librarian;

-- 删除书架表中的所有数据
DELETE FROM bookshelf;

-- 删除出版社表中的所有数据
DELETE FROM publisher;


-- 启用外键约束
SET FOREIGN_KEY_CHECKS = 1;
