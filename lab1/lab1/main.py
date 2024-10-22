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

def sql_search(sql, values):
    cursor.execute(sql, values)
    result = cursor.fetchone()

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
    result = sql_search(check_sql, check_values)

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
#     publisher_result = sql_search(sql_publisher, values1)
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
#     bookshelf_result = sql_search(sql_bookshelf, values2)
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
    result = sql_search(check_sql, check_values)
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
    result = sql_search(check_sql, check_values)

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
    result = sql_search(check_sql, check_values)
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
    result = sql_search(check_sql, check_values)
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
    result = sql_search(check_sql, check_values)

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
    result = sql_search(check_sql, check_values)

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
    result = sql_search(check_sql, check_values)
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
    result = sql_search(check_sql, check_values)
    if result is None:
        msg = f"数据库中不存在序列号为{record_id}的借阅记录"
        print(msg)
        return msg

    sql = "DELETE FROM record WHERE record_id = %s"
    values = (record_id,)
    return sql_delete(sql, values)


# 测试函数
def test_library_functions():
    # 测试插入作者
    print(insert_author(4, "J.K. Rowling", "British"))

    # 测试插入图书
    print(insert_book(5, "Harry Potter and the Philosopher's Stone", "Fantasy", 1, 1))

    # 测试插入书架
    print(insert_bookshelf(4, "Aisle 1"))

    # 测试插入管理员
    print(insert_librarian(3, "Alice", "Librarian", "2024-01-01"))

    # 测试插入会员
    print(insert_member(5, "John Doe", "M", "1990-01-01", "2024-01-01"))

    # 测试插入借阅记录
    print(insert_record(5, "2024-10-01", 1, 1, 1))

    # 测试插入罚款记录
    print(insert_fine(3, 5.00, "Late return", 1))

    # 测试插入出版社
    print(insert_publisher(3, "Bloomsbury", "50 Bedford Square, London"))

    # 测试删除作者
    print(delete_author(4))

    # 测试删除图书
    print(delete_book(5))

    # 测试删除书架
    print(delete_book_shelf(4))

    # 测试删除管理员
    print(delete_librarian(3))

    # 测试删除会员
    print(delete_member(5))

    # 测试删除借阅记录
    print(delete_record(5))

    # 测试删除罚款记录
    print(delete_fine(3))

    # 测试删除出版社
    print(delete_publisher(3))




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
            with gr.Tab("作者信息管理界面"):

                gr.Markdown("---")
                gr.Markdown(
                    """<div style='text-align: center; font-size: 24px; font-weight: bold;'>
                    增加作者
                    </div>"""
                )

                author_id = gr.Textbox(label="作者编号")
                author_name = gr.Textbox(label="作者姓名")
                nationality = gr.Textbox(label="作者国籍")

                insert_author_button = gr.Button(label="增加作者信息", variant='primary')

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

                del_author_button = gr.Button(label="删除作者", variant='stop')

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

    demo.launch()








    # # 使用 Blocks 来构建多个页面
    # with gr.Blocks() as demo:
    #     # 添加全局居中的标题
    #     gr.Markdown(
    #         """<div style='text-align: center; font-size: 48px; font-weight: bold;'>
    #         图书馆信息管理系统
    #         </div>"""
    #     )
    #
    #     # 创建 Tabs 组件
    #     with gr.Tabs():
    #         # 第一个页面 - 欢迎界面
    #         with gr.Tab("作者"):
    #             interface1 = gr.Interface(
    #                 fn=insert_author,
    #                 inputs=["text", "text"],
    #                 outputs="label",
    #                 title="增加作者信息",
    #                 description="输入作者姓名和国籍，将作者信息增加到数据库中"
    #             )
    #
    #             interface2 = gr.Interface(
    #                 fn=delete_author,
    #                 inputs=["text"],
    #                 outputs="label",
    #                 title="删除作者信息",
    #                 description="输入作者id，将作者信息从数据库中删除"
    #             )
    #
    #
    #         # 第二个页面 - 再见界面
    #         with gr.Tab("书籍"):
    #             interface3 = gr.Interface(
    #                 fn=insert_book,
    #                 inputs=[
    #                     gr.Textbox(label="书籍名称"),  # 第一个输入框的标签
    #                     gr.Textbox(label="书籍种类"),  # 第二个输入框的标签
    #                     gr.Textbox(label="出版商 ID"),  # 第三个输入框的标签
    #                     gr.Textbox(label="书架 ID")  # 第四个输入框的标签
    #                 ],
    #                 outputs=gr.Textbox(label="结果"),
    #                 title="增加书籍信息",
    #                 description="输入书籍名称、种类、出版商id、书架id，将书籍信息增加到数据库中",
    #                 article="这里是article所摆放的位置"
    #             )
    #             # interface2.render()  # 在当前选项卡中渲染另一个接口
    #
    # # 运行 Gradio 应用
    # demo.launch()