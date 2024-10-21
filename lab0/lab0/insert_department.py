import pymysql

# 连接到MySQL数据库
conn = pymysql.connect(
    host="localhost",  # 数据库主机
    user="root",  # 数据库用户名
    password="751016xkb",  # 数据库密码
    database="company",  # 数据库名称
    charset="utf8mb4"  # 使用utf8mb4字符集
)

# 创建游标对象
cursor = conn.cursor()

# 读取department.txt文件
with open('./dbms_lab/department.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 按制表符（Tab）分割数据
        data = line.strip().split('\t')
        dname, dno, mgrssn, mrgstartdate = data

        # 插入数据到department表
        sql = "INSERT INTO department (dname, dno, mgrssn, mrgstartdate) VALUES (%s, %s, %s, %s)"
        values = (dname, dno, mgrssn, mrgstartdate)

        try:
            cursor.execute(sql, values)
        except pymysql.MySQLError as err:
            print(f"Error: {err}")

# 提交更改
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()

print("数据插入完成！")
