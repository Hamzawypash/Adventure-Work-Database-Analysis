import pyodbc
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

connection = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-P4JB2O7\SQLEXPRESS;'
    r'DATABASE=AdventureWorks2022;'
    r'Trusted_Connection=yes;'
    r'TrustServerCertificate=yes;'
)

query = """
select sp.Bonus, sp.BusinessEntityID, (e.VacationHours + SickLeaveHours) as total_annual_leave_Hours
from sales.SalesPerson as sp
Inner join HumanResources.Employee as e
ON sp.BusinessEntityID=e.BusinessEntityID"""


df = pd.read_sql_query(query, connection)


connection.close()

print(df)


x = df['total_annual_leave_Hours']  
y = df['Bonus']  
m, b = np.polyfit(x, y, 1)

correlation_coefficient = np.corrcoef(x, y)[0, 1]
print(f"Correlation Coefficient: {correlation_coefficient:.2f}")


plt.figure(figsize=(10, 6))
plt.plot(x, m*x + b, color='green', label=f'Correlation Line: y = {m:.2f}x + {b:.2f}')
plt.scatter(x, y, alpha=0.7, color='blue')
plt.title('Relationship Between Total Leave Hours and Bonus')
plt.xlabel('Total Leave Hours (Vacation + Sick)')
plt.ylabel('Bonus')
plt.text(
    x.max() * 0.7, y.max() * 0.9,
    f'Correlation Coefficient: {correlation_coefficient:.2f}',
    fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.5)
)
plt.grid()
plt.show()
