# import the modules
from pymysql import *
import pandas.io.sql as sql
import pandas as pd
import streamlit as st

# connect the mysql with the python
con=connect(user="root",password="priyanka",host="localhost",database="attendease")

if st.button("Download Excel workbook"):
    df=sql.read_sql('select * from student',con)

    # print the data
    print(df)

    # writing to Excel
    datatoexcel = pd.ExcelWriter('RoboraceAttendease.xlsx')

    # write DataFrame to excel
    df.to_excel(datatoexcel)

    # save the excel
    datatoexcel.save()
    print('DataFrame is written to Excel File successfully.')