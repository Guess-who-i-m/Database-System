-- 1
SELECT ename
FROM employee ,works_on, project
WHERE employee.essn = works_on.essn AND works_on.pno = project.pno AND project.pname = 'SQL';


SELECT ename
FROM employee
JOIN works_on ON employee.essn = works_on.essn
JOIN project ON works_on.pno = project.pno
WHERE project.pname = 'SQL'
GROUP BY employee.essn;


-- 2
SELECT ename, address
FROM employee
JOIN department on employee.dno = department.dno
WHERE department.dname = '研发部' AND employee.salary < 3000;

-- 3
# SELECT ename
# FROM employee
# JOIN works_on ON works_on.essn = employee.essn
# WHERE works_on.pno != 'P1'
# GROUP BY employee.essn;

SELECT e1.ename
FROM employee AS e1, employee AS e2
JOIN works_on ON works_on.essn = e2.essn
WHERE e1.essn NOT IN (
    SELECT e2.essn
    FROM e2
    WHERE works_on.pno = 'P1'
    );

SELECT ename
FROM employee
WHERE essn NOT IN (
    SELECT employee.essn
    FROM employee
    JOIN works_on ON employee.essn = works_on.essn
    WHERE works_on.pno = 'P1'
    )
GROUP BY essn;

-- 4
SELECT e1.ename, dname
FROM employee AS e1, employee as e2, department
WHERE e1.superssn = e2.essn AND e2.ename = '张红' AND department.dno = e1.dno;

-- 5
select w1.essn
FROM works_on AS w1, works_on AS w2
WHERE w1.essn = w2.essn AND w1.pno = 'P1' AND w2.pno = 'P2';

-- 6
SELECT essn, ename
FROM employee
WHERE essn IN(
    SELECT essn
    FROM works_on
    GROUP BY essn
    HAVING COUNT(works_on.pno) = (
        SELECT COUNT(*)
        FROM project
        )
    );



-- 7
SELECT dname
FROM department, employee
WHERE department.dno = employee.dno
GROUP BY employee.dno
HAVING AVG(employee.salary) < 3000;

-- 8
SELECT employee.ename
FROM employee
JOIN works_on ON employee.essn = works_on.essn
GROUP BY employee.essn
HAVING SUM(works_on.hours) <= 8;

-- 9
SELECT department.dname, SUM(employee.salary) / SUM(works_on.hours)
FROM employee, works_on, department
WHERE employee.essn = works_on.essn AND employee.dno = department.dno
GROUP BY department.dno;

SELECT essn
FROM works_on
GROUP BY works_on.essn;