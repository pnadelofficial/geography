import pandas as pd

# Create a simple DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Write to Excel with openpyxl engine
df.to_excel('test.xlsx', index=False, engine='openpyxl')