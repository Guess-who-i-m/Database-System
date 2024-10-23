DELIMITER //

CREATE TRIGGER before_insert_record
BEFORE INSERT ON record
FOR EACH ROW
BEGIN
    DECLARE current_borrowed_books INT;

    -- 查询会员当前借阅的书籍数量，判断条件是借出3本以上并且尚未归还
    SELECT COUNT(*) INTO current_borrowed_books
    FROM record
    WHERE member_id = NEW.member_id AND return_date IS NULL;

    -- 如果当前借阅的书籍数量已达到或超过3本，则抛出错误
    IF current_borrowed_books > 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '该会员已借阅超过3本书，无法继续借书';
    END IF;
END//

DELIMITER ;

DROP TRIGGER IF EXISTS before_insert_record;