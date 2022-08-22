#Task 1: Understanding and Preparing Data
#Step 1: Read the 2010-2011 data in the Online Retail II excel. Make a copy of the dataframe you created.
import pandas as pd
import datetime as dt
import pandas as pd
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
pd.set_option("display.float_format", lambda x:"%.5f" %x)
df_=pd.read_excel("datasets/online_retail_II.xlsx",sheet_name="Year 2010-2011")
df=df_.copy()
df.head()
#Step 2: Examine the descriptive statistics of the dataset.
df.describe().T

#Step 3: Are there any missing observations in the dataset? If yes, how many missing observations in each variable?
df.isnull().value_counts().any()
df.isnull().sum()

#Step 4: Remove the missing observations from the dataset. Use the 'inplace=True' parameter for subtraction.
df.dropna(inplace=True)

#Step 5: How many unique items are there?
df["StockCode"].nunique()

#Step 6: How many of each product are there?
df["StockCode"].value_counts()

#Step 7: Sort the 5 most ordered products from most to least
df["StockCode"].value_counts().sort_values(ascending=False).head()

#Step 8: The 'C' in the invoices shows the canceled transactions. Remove the canceled transactions from the dataset.
df=df[~df["Invoice"].str.contains("C",na=False)]
df.head()

#Step 9: Create a variable named 'TotalPrice' that represents the total earnings per invoice.
df["TotalPrice"] = df["Quantity"]*df["Price"]
df.drop("TotalPrice",axis=1,inplace=True)

#Task 2: Calculating RFM Metrics
df["InvoiceDate"].max()
today_date=dt.datetime(2011,12,11)
#Step 1: Define Recency, Frequency and Monetary.
df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate: (today_date - InvoiceDate.max()).days,"Invoice": lambda Invoice: Invoice.nunique(),"Total_Price": lambda Total_Price: Total_Price.sum()})
#Step 3: Assign your calculated metrics to a variable named rfm.
rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate: (today_date - InvoiceDate.max()).days,"Invoice": lambda Invoice: Invoice.nunique(),"Total_Price": lambda Total_Price: Total_Price.sum()})
#Step 4: Change the names of the metrics you created to recency, frequency and monetary.
rfm.columns=["recency","frequency","monetary"]
rfm=rfm[rfm["monetary"]>0]
rfm.describe().T

#Task 3: Generate RFM Scores and Convert to a Single Variable
#Step 1: Convert the Recency, Frequency and Monetary metrics to scores between 1-5 with the help of qcut.
rfm["recency_score"]=pd.qcut(rfm["recency"],5,labels=[5,4,3,2,1])
rfm["frequency_score"]=pd.qcut(rfm["frequency"].rank(method="first"),5,labels=[1,2,3,4,5])
rfm["monetary_score"]=pd.qcut(rfm["monetary"],5,labels=[1,2,3,4,5])
rfm["RFM_Score"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
rfm.describe().T

#Task 4: Defining RF Score by Segment
#Step 1: Make segment definitions for the generated RF scores.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm["Segment"] = rfm["RFM_Score"].replace(seg_map,regex=True)
rfm.head()

#Quest 5: Time for Action!
#Step 1: Select the 3 segments you consider important. Interpret these three segments in terms of both action decisions and the structure of the segments (mean RFM values).
rfm[["Segment","recency","frequency","monetary"]].groupby("Segment").agg(["mean","count"])
loyal_df=pd.DataFrame()
loyal_df["loyal_customer_id"] = rfm[rfm["Segment"] == "loyal_customers"].index
loyal_df.head()
#Step 2: Select the customer IDs of the "Loyal Customers" class and get the excel output.
loyal_df.to_excel("loyal_customers.xlsx",sheet_name="Loyal Customers Index")
