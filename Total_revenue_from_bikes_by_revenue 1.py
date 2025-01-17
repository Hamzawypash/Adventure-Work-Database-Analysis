import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Establish Connection to the Database
connection = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-G1HPGDT\SQLEXPRESS;'
    r'DATABASE=AdventureWorks2022;'
    r'Trusted_Connection=yes;'
)

# Step 2: # Step 2: Define the SQL Query to get Bikes by country and revenue
query = """
SELECT 
    a.CountryRegionName AS Country,
    pc.Name AS Category,
    SUM(soh.TotalDue) AS Revenue
FROM 
    Sales.SalesOrderHeader AS soh
JOIN 
    Sales.SalesOrderDetail AS sod
    ON soh.SalesOrderID = sod.SalesOrderID
JOIN 
    Production.Product AS p
    ON sod.ProductID = p.ProductID
JOIN 
    Production.ProductSubcategory AS psc
    ON p.ProductSubcategoryID = psc.ProductSubcategoryID
JOIN 
    Production.ProductCategory AS pc
    ON psc.ProductCategoryID = pc.ProductCategoryID
JOIN 
    Sales.vStoreWithAddresses AS a
    ON soh.ShipToAddressID = a.BusinessEntityID  -- Corrected Join Condition
WHERE 
    pc.Name = 'Bikes'
GROUP BY 
    a.CountryRegionName, pc.Name
ORDER BY 
    Revenue ASC;
"""

# Step 3: Execute the Query and Load Data into DataFrame
df = pd.read_sql(query, connection)

# Step 4: Close the Database Connection
connection.close()

# Step 5: Display the DataFrame
print(df)

import matplotlib.pyplot as plt

# Plot the horizontal bar chart
plt.figure(figsize=(12, 8))
plt.barh(df['Country'], df['Revenue']/1000000, color='firebrick')
plt.xlabel('Total Revenue (in million)')
plt.ylabel('Country')
plt.title('Total Revenue From Bikes by Country', fontweight='bold', fontsize='28')
plt.show()

