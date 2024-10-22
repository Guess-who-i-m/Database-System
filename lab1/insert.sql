-- 插入会员数据
INSERT INTO member (member_id, member_name, gender, birth, reg_date) VALUES
(1, '王艾', 'F', '1990-05-14', '2023-01-01'),
(2, '李博', 'M', '1985-08-22', '2023-02-15'),
(3, '张槎', 'M', '1992-12-11', '2023-03-10'),
(4, '刘典', 'F', '1988-03-05', '2023-04-20');

-- 插入管理员数据
INSERT INTO librarian (librarian_id, librarian_name, job, hire_date) VALUES
(1, '陈梦', '领导', '2022-05-01'),
(2, '周帆', '助理', '2022-06-15');

-- 插入书架数据
INSERT INTO bookshelf (bookshelf_id, location) VALUES
(1, '第一楼 书架 A'),
(2, '第一楼 书架 B'),
(3, '第二楼 书架 A');

-- 插入出版社数据
INSERT INTO publisher (publisher_id, publisher_name, address) VALUES
(1, '清华大学出版社', '北京市朝阳区'),
(2, '复旦大学出版社', '上海市浦东新区');

-- 插入图书数据
INSERT INTO book (book_id, title, category, publisher_id, bookshelf_id) VALUES
(1, '数据库原理', '计算机', 1, 1),
(2, '算法导论', '计算机', 1, 2),
(3, '人类简史', '历史', 2, 1),
(4, '活着', '文学', 2, 3);

-- 插入作者数据
INSERT INTO author (author_id, author_name, nationality) VALUES
(1, '王小波', '中国'),
(2, 'Yuval Noah Harari', '以色列'),
(3, '曹文轩', '中国');

-- 插入图书与作者的关系数据
INSERT INTO book_author (book_id, author_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3);

-- 插入借阅记录数据
INSERT INTO record (record_id, borrow_date, return_date, member_id, book_id, librarian_id) VALUES
(1, '2024-01-10', '2024-01-17', 1, 1, 1),
(2, '2024-02-01', NULL, 2, 2, 2),
(3, '2024-03-05', '2024-03-12', 3, 3, 1),
(4, '2024-04-20', NULL, 4, 4, 2);

-- 插入罚款记录数据
INSERT INTO fine (fine_id, amount, reason, record_id) VALUES
(1, 5.00, '逾期归还', 2),
(2, 10.00, '书籍损坏', 1);
