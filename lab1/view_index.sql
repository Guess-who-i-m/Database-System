-- 创建视图和索引
use library;

-- 创建查询会员的借阅记录的视图
CREATE VIEW member_borrow AS
SELECT member.member_name, book.title, record.borrow_date, record.return_date
FROM record
JOIN member ON record.member_id = member.member_id
JOIN book ON record.book_id = book.book_id;

-- 创建查询超期借阅及罚款情况的视图
CREATE VIEW overdue_fine AS
SELECT member.member_name, book.title, fine.amount, fine.reason
FROM fine
JOIN record ON fine.record_id = record.record_id
JOIN member ON record.member_id = member.member_id
JOIN book ON record.book_id = book.book_id;

-- 为常用的属性创建索引
CREATE INDEX idx_book_title ON book(title);
CREATE INDEX idx_member_name ON member(member_name);
CREATE INDEX iex_author_name ON author(author_name);
