-- 创建数据库
CREATE DATABASE library;
use library;

-- 创建会员表
CREATE TABLE member(
    member_id       INT PRIMARY KEY,
    member_name     VARCHAR(50) NOT NULL ,
    gender          ENUM('M', 'F'),
    birth           DATE,
    reg_date        DATE
);

-- 创建管理员表
CREATE TABLE librarian(
    librarian_id    INT PRIMARY KEY,
    librarian_name  VARCHAR(50) NOT NULL ,
    job             VARCHAR(30),
    hire_date       DATE
);

-- 创建书架表
CREATE TABLE bookshelf(
    bookshelf_id    INT PRIMARY KEY,
    location        VARCHAR(50) NOT NULL
);

-- 创建出版社表
CREATE TABLE publisher(
    publisher_id    INT PRIMARY KEY,
    publisher_name  VARCHAR(50) NOT NULL ,
    address         VARCHAR(100)
);

-- 创建图书表
CREATE TABLE book(
    book_id         INT PRIMARY KEY,
    title           VARCHAR(100) NOT NULL ,
    category        VARCHAR(50),
    publisher_id    INT,
    bookshelf_id    INT,
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id),
    FOREIGN KEY (bookshelf_id) REFERENCES bookshelf(bookshelf_id)
);

-- 创建作者表
CREATE TABLE author(
    author_id       INT PRIMARY KEY,
    author_name     VARCHAR(50) NOT NULL ,
    nationality     VARCHAR(50)
);

-- 图书作者多对多关系表
CREATE TABLE book_author(
    book_id         INT,
    author_id       INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (author_id) REFERENCES author(author_id)
);

-- 创建借阅记录表
CREATE TABLE record(
    record_id       INT PRIMARY KEY,
    borrow_date     DATE,
    return_date     DATE,
    member_id       INT ,
    book_id         INT,
    librarian_id    INT,
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (book_id)   REFERENCES book(book_id),
    FOREIGN KEY (librarian_id) REFERENCES librarian(librarian_id)
);

-- 创建罚款记录表
CREATE TABLE fine(
    fine_id     INT PRIMARY KEY,
    amount      DECIMAL(10, 2) NOT NULL ,
    reason      TEXT,
    record_id   INT,
    FOREIGN KEY (record_id) REFERENCES record(record_id)
)