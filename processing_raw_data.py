import pandas as pd 


df=pd.read_csv("data/raw/raw_online_retail.csv")
print(df.dtypes)
invalid_invoice = df[df["Invoice"].str.startswith("C")]
negative_quantity = df[df["Quantity"]<0]
negative_price = df[df["Price"]<0]
negative_qantity_invalid_invoice = df[(df["Invoice"].str.startswith("C")) &(df["Quantity"]<0) ]
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("INVALID INVOICE DATA")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(invalid_invoice.head())
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(f"Number records of Invalid Invoice are {len(invalid_invoice)} out of {len(df)}")
print(f"Number records of Negative Quantities are {len(negative_quantity)} out of {len(df)}")
print(f"Number of records of both Invalid Invoices and Negative Quantities are {len(negative_qantity_invalid_invoice)} out of {len(df)}")
print(f"Number of records of negative prices are {len(negative_price)}")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("NEGATIVE PRICE DATA")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(negative_price.head())
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print()




