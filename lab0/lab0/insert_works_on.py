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
with open('./dbms_lab/works_on.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 按制表符（Tab）分割数据
        data = line.strip().split('\t')
        # dname, dno, mgrssn, mrgstartdate = data
        # ename, essn, address, salary, superssn, dno = data
        # pname, pno, plocation, dno = data
        essn, pno, hours = data

        # 插入数据到department表
        # sql = "INSERT INTO department (dname, dno, mgrssn, mrgstartdate) VALUES (%s, %s, %s, %s)"
        # sql = "INSERT INTO employee (ename, essn, address, salary, superssn, dno) VALUES (%s, %s, %s, %s, %s, %s)"
        sql = "INSERT INTO works_on (essn, pno, hours) VALUES (%s, %s, %s)"
        values = (essn, pno, hours)

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