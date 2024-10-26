import pymysql
import gradio as gr
import datetime

# 连接到MySQL数据库
conn = pymysql.connect(
    host="localhost",  # 数据库主机
    port=3306,  # 端口号，默认为3306
    user="root",  # 数据库用户名
    password="751016xkb",  # 数据库密码
    database="library",  # 数据库名称
    connect_timeout=60,  # 将超时时间设置为60秒
    charset="utf8mb4"  # 使用utf8mb4字符集
)

# 创建游标对象
cursor = conn.cursor()


# sql的基本使用嵌套函数
def sql_insert(sql, values):
    try:
        cursor.execute(sql, values)
        conn.commit()
        msg = f"插入成功"
    except Exception as e:
        conn.rollback()  # 出现错误时回滚
        msg = f"插入失败：{e}"

    print(msg)
    return msg

def sql_delete(sql, values):
    try:
        cursor.execute(sql, values)
        conn.commit()
        msg = f"删除成功"
    except Exception as e:
        conn.rollback()  # 出现错误时回滚
        msg = f"删除失败：{e}"

    print(msg)
    return msg

def sql_search_one(sql, values):
    cursor.execute(sql, values)
    result = cursor.fetchone()

    return result

def sql_search_all(sql):
    cursor.execute(sql)
    result = cursor.fetchall()

    return result

# def insert_author(author_name, nationality=None):
#     if nationality is None:
#         sql = "INSERT INTO author (author_name) VALUES (%s)"
#         values = (author_name,)
#     else:
#         sql = "INSERT INTO author (author_name, nationality) VALUES (%s, %s)"
#         values = (author_name, nationality)
#
#     return sql_insert(sql, values)

# author表的基础增删改查
def insert_author(author_id, author_name, nationality):
    if not author_name:
        return "作者名不能为空"

    sql = "INSERT INTO author (author_id, author_name, nationality) VALUES (%s, %s, %s)"
    values = (author_id, author_name, nationality)
    return sql_insert(sql, values)

def delete_author(author_id):

    check_sql = "SELECT author_id FROM author WHERE author_id = %s"
    check_values = (author_id,)
    result = sql_search_one(check_sql, check_values)

    if result is None:
        msg = f"数据库中不存在序列号为{author_id}的作者"
        print(msg)
        return msg

    sql = "DELETE FROM author WHERE author_id = %s"
    values = (author_id,)
    return sql_delete(sql, values)


# def insert_book(title, category, publisher_name, bookshelf_location):
#     msg = ''
#
#     # 查询出版社 ID
#     sql_publisher = "SELECT publisher_id FROM publisher WHERE publisher_name = %s"
#     values1 = (publisher_name,)
#     # cursor.execute(sql_publisher, values1)
#     # publisher_result = cursor.fetchone()
#     publisher_result = sql_search_one(sql_publisher, values1)
#
#     if publisher_result is None:
#         msg = "插入失败：数据库中不存在对应的出版社"
#         print(msg)
#         return msg
#
#     publisher_id = publisher_result[0]
#
#     # 查询书架 ID
#     sql_bookshelf = "SELECT bookshelf_id FROM bookshelf WHERE location = %s"
#     values2 = (bookshelf_location,)
#     # cursor.execute(sql_bookshelf, values2)
#     # bookshelf_result = cursor.fetchone()
#     bookshelf_result = sql_search_one(sql_bookshelf, values2)
#
#     if bookshelf_result is None:
#         msg = "插入失败：数据库中不存在对应的书架"
#         print(msg)
#         return msg
#
#     bookshelf_id = bookshelf_result[0]
#
#     # 插入图书
#     sql_book = "INSERT INTO book (title, category, publisher_id, bookshelf_id) VALUES (%s, %s, %s, %s)"
#     values3 = (title, category, publisher_id, bookshelf_id)
#
#     msg = sql_insert(sql_book, values3)
#
#     return msg

# book表的基础增删查改
def insert_book(book_id, title, category, publisher_id, bookshelf_id):
    if not title:
        return "书名不能为空"
    sql = "INSERT INTO book(book_id, title, category, publisher_id, bookshelf_id) VALUES (%s, %s, %s, %s, %s)"
    values = (book_id, title, category, publisher_id, bookshelf_id)
    return sql_insert(sql, values)

def delete_book(book_id):
    check_sql = "SELECT book_id FROM book WHERE book_id = %s"
    check_values = (book_id,)
    result = sql_search_one(check_sql, check_values)
    if result is None:
        msg = f"数据库中不存在序列号为{book_id}的图书"
        print(msg)
        return msg

    sql = "DELETE FROM book WHERE book_id = %s"
    values = (book_id,)
    return sql_delete(sql, values)


# book_author表的基础增删改查
def insert_book_author(book_id, author_id):
    sql = "INSERT INTO book_author(book_id, author_id) VALUES (%s, %s)"
    values = (book_id, author_id)
    return sql_insert(sql, values)

def delete_book_author(book_id, author_id):
    check_sql = "SELECT book_id, author_id FROM book_author WHERE book_id = %s AND author_id = %s"
    check_values = (book_id, author_id)
    result = sql_search_one(check_sql, check_values)

    if result is None:
        msg = f"数据库中不存在图书序列号为{book_id}作者序列号为{author_id}的著作关系"
        print(msg)
        return msg

    sql = "DELETE FROM book_author WHERE book_id = %s AND author_id = %s"
    values = (book_id, author_id)
    return sql_delete(sql, values)


# bookshelf表的基础增删改查操作
def insert_bookshelf(bookshelf_id, location):
    sql = "INSERT INTO bookshelf (bookshelf_id, location) VALUES (%s, %s)"
    values = (bookshelf_id, location)
    return sql_insert(sql, values)

def delete_book_shelf(bookshelf_id):
    check_sql = "SELECT bookshelf_id FROM bookshelf WHERE bookshelf_id = %s"
    check_values = (bookshelf_id,)
    result = sql_search_one(check_sql, check_values)
    if result is None:
        msg = f"数据库中不存在序列号为{bookshelf_id}的书架"
        print(msg)
        return msg

    sql = "DELETE FROM bookshelf WHERE bookshelf_id = %s"
    values = (bookshelf_id,)
    return sql_delete(sql, values)


# def insert_librarian(librarian_name, job, year, month, day):
#     msg = ''
#     hire_date = ''
#
#     # 检查librarian_name是否为None或空字符串
#     if not librarian_name:
#         msg = "插入失败：管理员姓名不能为空"
#         print(msg)
#         return msg
#
#     # 检查日期格式是否正确
#     try:
#         # 如果year, month, day均不为空，则构建日期
#         if year is not None and month is not None and day is not None:
#             hire_date = datetime.date(year, month, day)
#         else:
#             msg = "插入失败：雇佣日期必须提供完整的年、月和日"
#             print(msg)
#             return msg
#     except ValueError:
#         msg = "插入失败：日期格式不正确，年、月、日应为有效值"
#         print(msg)
#         return msg
#
#     # 构建SQL语句和参数
#     sql = "INSERT INTO librarian (librarian_name, job, hire_date) VALUES (%s, %s, %s)"
#     values = (librarian_name, job, hire_date)
#
#     return sql_insert(sql, values)

# fine的增删改查基本操作
def insert_fine(fine_id, amount, reason, record_id):
    sql = "INSERT INTO fine(fine_id, amount, reason, record_id) VALUES (%s, %s, %s, %s)"
    values = (fine_id, amount, reason, record_id)
    return sql_insert(sql, values)

def delete_fine(fine_id):
    check_sql = "SELECT fine_id FROM fine WHERE fine_id = %s"
    check_values = (fine_id,)
    result = sql_search_one(check_sql, check_values)
    if result is None:
        msg = f"数据库中不存在序列号为{fine_id}的罚款记录"
        print(msg)
        return msg

    sql = "DELETE FROM fine WHERE fine_id = %s"
    values = (fine_id,)
    return sql_delete(sql, values)

# librarian表的基础增删改查操作
def insert_librarian(librarian_id, librarian_name, job, hire_date):
    sql = "INSERT INTO librarian (librarian_id, librarian_name, job, hire_date) VALUES (%s, %s, %s, %s)"
    values = (librarian_id, librarian_name, job, hire_date)
    return sql_insert(sql, values)

def delete_librarian(librarian_id):
    check_sql = "SELECT librarian_id FROM librarian WHERE librarian_id = %s"
    check_values = (librarian_id,)
    result = sql_search_one(check_sql, check_values)

    if result is None:
        msg = f"数据库中不存在序列号为{librarian_id}的管理员"
        print(msg)
        return msg

    sql = "DELETE FROM librarian WHERE librarian_id = %s"
    values = (librarian_id,)
    return sql_delete(sql, values)

# member的基础增删改查操作
def insert_member(member_id, member_name, gender, birth, reg_date):
    sql = "INSERT INTO member(member_id, member_name, gender, birth, reg_date) VALUES (%s, %s, %s, %s, %s)"
    values = (member_id, member_name, gender, birth, reg_date)
    return sql_insert(sql, values)

def delete_member(member_id):
    check_sql = "SELECT member_id FROM member WHERE member_id = %s"
    check_values = (member_id,)
    result = sql_search_one(check_sql, check_values)

    if result is None:
        msg = f"数据库中不存在序列号为{member_id}的会员"
        print(msg)
        return msg

    sql = "DELETE FROM member WHERE member_id = %s"
    values = (member_id,)
    return sql_delete(sql, values)

# publisher表的基础增删改查操作
def insert_publisher(publisher_id, publisher_name, address):
    sql = "INSERT INTO publisher(publisher_id, publisher_name, address) VALUES (%s, %s, %s)"
    values = (publisher_id, publisher_name, address)
    return sql_insert(sql, values)

def delete_publisher(publisher_id):
    check_sql = "SELECT publisher_id FROM publisher WHERE publisher_id = %s"
    check_values = (publisher_id,)
    result = sql_search_one(check_sql, check_values)
    if result is None:
        msg = f"数据库中不存在序列号为{publisher_id}的出版社"
        print(msg)
        return msg

    sql = "DELETE FROM publisher WHERE publisher_id = %s"
    values = (publisher_id,)
    return sql_delete(sql, values)

# record的增删改查
# 借书时插入借阅信息
def insert_record(record_id, borrow_date, member_id, book_id, librarian_id):
    # borrow_date = datetime.date(borrow_year, borrow_month, borrow_day)
    sql = "INSERT INTO record (record_id, borrow_date, member_id, book_id, librarian_id) VALUES (%s, %s, %s, %s, %s)"
    values = (record_id, borrow_date, member_id, book_id, librarian_id)
    return sql_insert(sql, values)

def delete_record(record_id):
    check_sql = "SELECT record_id FROM record WHERE record_id = %s"
    check_values = (record_id,)
    result = sql_search_one(check_sql, check_values)
    if result is None:
        msg = f"数据库中不存在序列号为{record_id}的借阅记录"
        print(msg)
        return msg

    sql = "DELETE FROM record WHERE record_id = %s"
    values = (record_id,)
    return sql_delete(sql, values)

# 查询部分
# 利用视图查询，使用视图查询每一个会员借的的每一本书
def search_member_borrow():
    sql = "SELECT * FROM member_borrow;"
    result = sql_search_all(sql)
    return tuple_to_list_string(result)

# 设计一个利用到了连接查询的方法
# 查询会员的借阅书籍和还书情况
def search_record_from_member_name(member_name):
    sql = ("SELECT member.member_id, member.member_name, record.record_id, record.book_id, book.title, record.borrow_date, record.return_date "
           "FROM record "
           "JOIN book ON record.book_id = book.book_id "
           "JOIN member ON record.member_id = member.member_id "
           "WHERE member.member_name = %s;")
    values = (member_name,)

    try:
        cursor.execute(sql, values)
        result = cursor.fetchall()

        # 如果查询结果为空，返回提示信息
        if not result:
            return "没有找到相关借阅记录。"

        return tuple_to_list_string(result)

    except Exception as e:
        return f"查询失败：{e}"

# 查询借阅了两本书以上的用户
def search_member_n_books(book_num):
    sql = ("SELECT member.member_id, member.member_name, COUNT(record.record_id) "
           "FROM member "
           "JOIN record ON member.member_id = record.member_id "
           "WHERE member.member_id IN (SELECT record.member_id FROM record GROUP BY record.member_id HAVING COUNT(record.record_id) >= %s) "
           "GROUP BY member.member_id")
    values = (book_num,)

    try:
        cursor.execute(sql, values)
        result = cursor.fetchall()

        # 如果查询结果为空，返回提示信息
        if not result:
            return "没有找到相关借阅记录。"

        return tuple_to_list_string(result)

    except Exception as e:
        return f"查询失败：{e}"

# 分组查询，按照类别对书籍数量进行统计
def search_books_num_by_category(num):
    sql = "SELECT book.category, COUNT(book.book_id) FROM book GROUP BY book.category HAVING COUNT(book.book_id) >= %s"
    values = (num,)

    try:
        cursor.execute(sql,values)
        result = cursor.fetchall()

        # 如果查询结果为空，返回提示信息
        if not result:
            return "没有找到相关借阅记录。"

        return tuple_to_list_string(result)

    except Exception as e:
        return f"查询失败：{e}"

# 查询结果
def tuple_to_list_string(data):
    result = []
    for item in data:
        # 将每个元组元素转换为字符串，处理 None 值
        formatted_item = [
            str(element) if element is not None else "None"
            for element in item
        ]
        # 将每个元组格式化为字符串并添加到列表中
        result.append(",\t".join(formatted_item))

    # 将所有元素加入一个列表展示形式的字符串
    return "\n".join(f"- {i + 1}. {entry}" for i, entry in enumerate(result))


# gradio部分
# 作为测试用例
if __name__ == '__main__':
    # 可以拿来用的gradio模板
    # # 使用 Blocks 来构建多个页面
    with gr.Blocks(title='图书馆信息管理系统') as demo:
        # 添加全局居中的标题
        gr.Markdown(
            """<div style='text-align: center; font-size: 48px; font-weight: bold;'>
            图书馆信息管理系统
            </div>"""
        )

        # 创建 Tabs 组件
        with gr.Tabs():
            # 第一个页面 - 作者信息管理页面
            with gr.Tab("作者"):

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加作者
                    </div>"""
                )

                author_id = gr.Textbox(label="作者编号")
                author_name = gr.Textbox(label="作者姓名")
                nationality = gr.Textbox(label="作者国籍")

                insert_author_button = gr.Button("增加作者信息", variant='primary')

                insert_author_output = gr.Textbox(label="结果")


                insert_author_button.click(
                    fn=insert_author,
                    inputs=[author_id, author_name,nationality],
                    outputs=insert_author_output
                )
                gr.Markdown("---")

                # 删除作者部分
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除作者
                    </div>"""
                )

                del_author_id = gr.Textbox(label="作者编号")

                del_author_button = gr.Button("删除作者", variant='stop')

                del_author_output = gr.Textbox(label="删除结果")

                del_author_button.click(
                    fn=delete_author,
                    inputs=del_author_id,
                    outputs=del_author_output
                )
                gr.Markdown("---")

            # 第二个页面 - 书籍页面
            with gr.Tab("书籍"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加书籍
                    </div>"""
                )

                add_book_id = gr.Textbox(label="书籍编号")
                add_title = gr.Textbox(label="书籍名称")
                add_category = gr.Textbox(label="书籍种类")
                add_publisher_id = gr.Textbox(label='出版社编号')
                add_bookshelf_id = gr.Textbox(label="书架编号")
                add_book_button = gr.Button("增加书籍", variant='primary')
                add_book_output = gr.Textbox(label="结果")

                add_book_button.click(
                    fn=insert_book,
                    inputs=[add_book_id, add_title, add_category, add_publisher_id, add_bookshelf_id],
                    outputs=add_book_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除书籍
                    </div>"""
                )

                book_id = gr.Textbox(label="书籍id")
                delete_book_button = gr.Button("减少书籍", variant='stop')
                delete_book_output = gr.Textbox(label="结果")
                delete_book_button.click(
                    fn=delete_book,
                    inputs=[book_id],
                    outputs=delete_book_output
                )
                gr.Markdown("---")

            # 第三个页面 - 图书-作者页面
            with gr.Tab("作者-书籍"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加作者-书籍记录
                    </div>"""
                )

                add_book_id = gr.Textbox(label="书籍编号")
                add_author_id = gr.Textbox(label="作者编号")
                add_book_author_button = gr.Button("增加书籍-作者记录", variant="primary")
                add_book_author_output = gr.Textbox(label="结果")
                add_book_author_button.click(
                    fn=insert_book_author,
                    inputs=[add_book_id, add_author_id],
                    outputs=add_book_author_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除作者-书籍记录
                    </div>"""
                )

                del_book_id = gr.Textbox(label="书籍编号")
                del_author_id = gr.Textbox(label="作者编号")

                del_book_author_button = gr.Button("减少作者-书籍记录", variant='stop')
                del_book_author_output = gr.Textbox(label="结果")
                del_book_author_button.click(
                    fn=delete_book_author,
                    inputs=[del_book_id, del_author_id],
                    outputs=del_book_author_output
                )
                gr.Markdown("---")

            # 第四个页面 - 书架页面
            with gr.Tab("书架"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加书架信息
                    </div>"""
                )

                add_bookshelf_id = gr.Textbox(label="书架编号")
                add_location = gr.Textbox(label="书架位置")
                add_bookshelf_button = gr.Button("增加书架", variant="primary")
                add_bookshelf_output = gr.Textbox(label="结果")
                add_bookshelf_button.click(
                    fn=insert_bookshelf,
                    inputs=[add_bookshelf_id, add_location],
                    outputs=add_bookshelf_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除书架信息
                    </div>"""
                )

                del_bookshelf_id = gr.Textbox(label="书架编号")
                del_bookshelf_button = gr.Button("减少书架", variant='stop')
                del_bookshelf_output = gr.Textbox(label="结果")
                del_bookshelf_button.click(
                    fn=delete_book_shelf,
                    inputs=[del_bookshelf_id, ],
                    outputs=del_bookshelf_output
                )
                gr.Markdown("---")

            # 第五个页面 - 罚款页面
            with gr.Tab("处罚记录"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加处罚记录
                    </div>"""
                )

                add_fine_id = gr.Textbox(label="处罚记录编号")
                add_amount = gr.Textbox(label="罚款总额")
                add_reason = gr.Textbox(label="罚款原因")
                add_record_id = gr.Textbox(label="所处理的借阅记录编号")
                add_fine_button = gr.Button("增加处罚记录", variant="primary")
                add_fine_output = gr.Textbox(label="结果")
                add_fine_button.click(
                    fn=insert_fine,
                    inputs=[add_fine_id, add_amount, add_reason, add_record_id],
                    outputs=add_fine_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除处罚记录
                    </div>"""
                )

                del_fine_id = gr.Textbox(label="处罚记录编号")
                del_fine_button = gr.Button("删除处罚记录", variant='stop')
                del_fine_output = gr.Textbox(label="结果")
                del_fine_button.click(
                    fn=delete_fine,
                    inputs=[del_fine_id, ],
                    outputs=del_fine_output
                )
                gr.Markdown("---")

            # 第六个页面 - 图书管理员页面
            with gr.Tab("图书管理员"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加图书管理员信息
                    </div>"""
                )

                add_librarian_id = gr.Textbox(label="图书管理员编号")
                add_librarian_name = gr.Textbox(label="图书管理员姓名")
                add_job = gr.Textbox(label="图书管理员职称")
                add_hire_date = gr.Textbox(label="雇佣日期（格式YYYY-MM-DD）")
                add_librarian_button = gr.Button("增加图书管理员", variant="primary")
                add_librarian_output = gr.Textbox(label="结果")
                add_librarian_button.click(
                    fn=insert_librarian,
                    inputs=[add_librarian_id, add_librarian_name, add_job, add_hire_date],
                    outputs=add_librarian_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除图书管理员信息
                    </div>"""
                )

                del_librarian_id = gr.Textbox(label="图书管理员编号")
                del_librarian_button = gr.Button("删除图书管理员", variant='stop')
                del_librarian_output = gr.Textbox(label="结果")
                del_librarian_button.click(
                    fn=delete_librarian,
                    inputs=[del_librarian_id, ],
                    outputs=del_librarian_output
                )
                gr.Markdown("---")

            # 第七个页面 - 会员页面
            with gr.Tab("会员"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加会员信息
                    </div>"""
                )

                add_member_id = gr.Textbox(label="会员编号")
                add_member_name = gr.Textbox(label="会员姓名")
                add_gender = gr.Textbox(label="会员性别（M或者F）")
                add_birth = gr.Textbox(label="生日（格式YYYY-MM-DD）")
                add_reg_date = gr.Textbox(label="注册日期（格式YYYY-MM-DD")
                add_member_button = gr.Button("增加会员", variant="primary")
                add_member_output = gr.Textbox(label="结果")
                add_member_button.click(
                    fn=insert_member,
                    inputs=[add_member_id, add_member_name, add_gender, add_birth, add_reg_date],
                    outputs=add_member_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除会员信息
                    </div>"""
                )

                del_member_id = gr.Textbox(label="会员编号")
                del_member_button = gr.Button("删除会员", variant='stop')
                del_member_output = gr.Textbox(label="结果")
                del_member_button.click(
                    fn=delete_member,
                    inputs=[del_member_id, ],
                    outputs=del_member_output
                )
                gr.Markdown("---")

            # 第八个页面 - 出版社页面
            with gr.Tab("出版社"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加出版社信息
                    </div>"""
                )

                add_publisher_id = gr.Textbox(label="出版社编号")
                add_publisher_name = gr.Textbox(label="出版社名")
                add_adress = gr.Textbox(label="出版社地址")
                add_publiher_button = gr.Button("增加出版社", variant="primary")
                add_publiher_output = gr.Textbox(label="结果")
                add_publiher_button.click(
                    fn=insert_publisher,
                    inputs=[add_publisher_id, add_publisher_name, add_adress],
                    outputs=add_publiher_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除出版社信息
                    </div>"""
                )

                del_publisher_id = gr.Textbox(label="出版社编号")
                del_publisher_button = gr.Button("删除出版社", variant='stop')
                del_publisher_output = gr.Textbox(label="结果")
                del_publisher_button.click(
                    fn=delete_publisher,
                    inputs=[del_publisher_id, ],
                    outputs=del_publisher_output
                )
                gr.Markdown("---")

            # 第九个页面 - 借阅记录页面
            with gr.Tab("借阅记录"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加借阅记录信息总览
                    </div>"""
                )

                add_record_id = gr.Textbox(label="借阅记录编号")
                add_borrow_date = gr.Textbox(label="借阅日期（格式YYYY-MM-DD）")
                add_member_id = gr.Textbox(label="会员编号")
                add_book_id = gr.Textbox(label="图书编号")
                add_librarian_id = gr.Textbox(label="管理员编号")
                add_record_button = gr.Button("增加借阅记录", variant="primary")
                add_record_output = gr.Textbox(label="结果")
                add_record_button.click(
                    fn=insert_record,
                    inputs=[add_record_id, add_borrow_date, add_member_id, add_book_id, add_librarian_id],
                    outputs=add_record_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    删除借阅记录信息
                    </div>"""
                )

                del_record_id = gr.Textbox(label="借阅记录编号")
                del_record_button = gr.Button("删除借阅记录", variant='stop')
                del_record_output = gr.Textbox(label="结果")
                del_record_button.click(
                    fn=delete_record,
                    inputs=[del_record_id, ],
                    outputs=del_record_output
                )
                gr.Markdown("---")

            # 第十个页面 - 查询视图用户借阅情况页面
            with gr.Tab("查询页面"):
                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    用户借阅情况查询
                    </div>"""
                )


                search_member_borrow_button = gr.Button("查询用户借阅结果", variant="primary")
                search_member_borrow_output = gr.Textbox(label="结果")
                search_member_borrow_button.click(
                    fn=search_member_borrow,
                    outputs=search_member_borrow_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    根据用户姓名查询用户借阅书籍情况
                    </div>"""
                )
                search_member_name = gr.Textbox(label="输入用户姓名")
                search_name_borrow_button = gr.Button("查询用户借阅结果", variant="primary")
                search_name_borrow_output = gr.Textbox(label="结果")
                search_name_borrow_button.click(
                    fn=search_record_from_member_name,
                    inputs=search_member_name,
                    outputs=search_name_borrow_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    查询借阅书籍数量大于n的用户
                    </div>"""
                )
                search_num_books = gr.Textbox(label="输入书籍数量n")
                search_num_books_button = gr.Button("查询用户借阅结果", variant="primary")
                search_num_books_output = gr.Textbox(label="结果")
                search_num_books_button.click(
                    fn=search_member_n_books,
                    inputs=search_num_books,
                    outputs=search_num_books_output
                )
                gr.Markdown("---")

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    查询每一类图书的数量
                    </div>"""
                )
                search_catogory_input = gr.Textbox(label="至少多少本（默认为0）")
                search_category_button = gr.Button("查询每一类图书的数量", variant="primary")
                search_category_output = gr.Textbox(label="结果")
                search_category_button.click(
                    inputs = search_catogory_input,
                    fn=search_books_num_by_category,
                    outputs= search_category_output
                )
                gr.Markdown("---")


    demo.launch()