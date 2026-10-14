# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName
FROM employees e
JOIN offices o USING (officeCode)
WHERE o.city = 'Boston';
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e USING (officeCode)
WHERE e.employeeNumber IS NULL;
""", conn)

# STEP 3
df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o USING (officeCode)
ORDER BY e.firstName, e.lastName;
""", conn)

# STEP 4
df_contacts = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o USING (customerNumber)
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName;
""", conn)

# STEP 5
df_payment = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers c
JOIN payments p USING (customerNumber)
ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# STEP 6
df_credit = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName,
       COUNT(c.customerNumber) AS n_customers
FROM employees e
JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
GROUP BY e.employeeNumber
HAVING AVG(c.creditLimit) > 90000
ORDER BY n_customers DESC;
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od USING (productCode)
GROUP BY p.productCode
ORDER BY totalunits DESC;
""", conn)

# STEP 8
df_total_customers = pd.read_sql("""
SELECT p.productName, p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od USING (productCode)
JOIN orders o USING (orderNumber)
GROUP BY p.productCode
ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
df_customers = pd.read_sql("""
SELECT ofc.officeCode, ofc.city, COUNT(c.customerNumber) AS n_customers
FROM offices ofc
JOIN employees e USING (officeCode)
JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
GROUP BY ofc.officeCode;
""", conn)

# STEP 10
df_under_20 = pd.read_sql("""
WITH low_products AS (
  SELECT od.productCode
  FROM orderdetails od
  JOIN orders o USING (orderNumber)
  GROUP BY od.productCode
  HAVING COUNT(DISTINCT o.customerNumber) < 20
)
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,
       ofc.city, ofc.officeCode
FROM employees e
JOIN offices ofc USING (officeCode)
JOIN customers c ON c.salesRepEmployeeNumber = e.employeeNumber
JOIN orders o ON o.customerNumber = c.customerNumber
JOIN orderdetails od ON od.orderNumber = o.orderNumber
WHERE od.productCode IN (SELECT productCode FROM low_products)
ORDER BY e.lastName;
""", conn)

conn.close()