import cv2
import pyzbar.pyzbar as pyzbar
import pyqrcode
from pyzbar.pyzbar import ZBarSymbol
import streamlit as st
import mysql.connector
import pandas as pd
import urllib.request as request
from bs4 import BeautifulSoup as bs
import re
import json
import time


count=0;
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def decode(im):
    decoded_objs = pyzbar.decode(im, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

    for obj in decoded_objs:
        return obj.data.decode('utf-8')

def scan():
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    prev_data = None 
    with placeholder.container():
        st.title("Attendease")
        st.subheader("Scan the QR CODE")

        st.sidebar.text("Select Events")
        event1=st.sidebar.checkbox("Roborace");
        event2=st.sidebar.checkbox("Armour Wars");
        event3=st.sidebar.checkbox("Project Competition");

        col1, col2, col3, col4 = st.columns(4)
       
        if event1:
            with col1:
                st.header("PRN")
            with col2:
                st.header("Name")
            with col3:
                st.header("Division")
            with col4:
                st.header("Roll No")

            rows = run_query("SELECT * FROM roborace;")
            for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")

        if event2:
            with col1:
                st.header("PRN")
            with col2:
                st.header("Name")
            with col3:
                st.header("Division")
            with col4:
                st.header("Roll No")
            

            rows = run_query("SELECT * FROM armour_wars;")
            for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")

        
        if event3:
            with col1:
                st.header("PRN")
            with col2:
                st.header("Name")
            with col3:
                st.header("Division")
            with col4:
                st.header("Roll No")

            rows = run_query("SELECT * FROM project_competition;")
            for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")
                        

        while True:
            ret, frame = cap.read()

            data = decode(frame)

            if event1 and data is not None and data != prev_data:
                prev_data = data
                rows = run_query("SELECT student.PRN, student.name, student.division, student.roll_no FROM student where PRN="+data+";")
                for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")

                        query="INSERT INTO roborace values(%s,%s,%s,%s)";
                        val = (str(row[0]), str(row[1]), str(row[2]),str(row[3]));
                        cursor=conn.cursor()
                        cursor.execute(query, val);
                        conn.commit();
            
            if event2 and data is not None and data != prev_data:
                prev_data = data
                rows = run_query("SELECT student.PRN, student.name, student.division, student.roll_no FROM student where PRN="+data+";")
                for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")

                        query="INSERT INTO armour_wars values(%s,%s,%s,%s)";
                        val = (str(row[0]), str(row[1]), str(row[2]),str(row[3]));
                        cursor=conn.cursor()
                        cursor.execute(query, val);
                        conn.commit();
            
            if event3 and data is not None and data != prev_data:
                prev_data = data
                rows = run_query("SELECT student.PRN, student.name, student.division, student.roll_no FROM student where PRN="+data+";")
                for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")

                        query="INSERT INTO project_competition values(%s,%s,%s,%s)";
                        val = (str(row[0]), str(row[1]), str(row[2]),str(row[3]));
                        cursor=conn.cursor()
                        cursor.execute(query, val);
                        conn.commit();

            cv2.imshow('QRCode Scanner', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

placeholder = st.empty()

if __name__ == '__main__':
    # if count==0:
        # st.write(count)
        with placeholder.container():
            user=st.text_input("Username")
            passwd=st.text_input("Password")
            if st.button("Login"):
                if((user=="Admin" ) and (passwd=="123")):
                    # count=1;
                    # st.write(count);
                    scan()
    # else:
    #      scan()
