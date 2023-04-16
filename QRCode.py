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

# Initialize connection.
# Uses st.cache_resource to only run once.

@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

    

    
# number = conn.cursor().execute("SELECT count(*) FROM information_schema.columns WHERE table_name ='eventdata';")
# st.write(number)
# rows = pd.read_sql('SELECT * from eventdata;',conn)

# query_df = pd.DataFrame(query_results)
					# st.dataframe(query_df)

# Print results.


def decode(im):
    # Decode QR code and barcode from the image using PyZBar library
    decoded_objs = pyzbar.decode(im, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

    # Loop through all decoded objects and return the data
    for obj in decoded_objs:
        return obj.data.decode('utf-8')



def scan():
    # Open the default camera using OpenCV
    cap = cv2.VideoCapture(0)

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    prev_data = None  # Initialize previous data as None

    st.title("Attendease")
    st.subheader("Scan the QR CODE")

    st.sidebar.text("Select Events")
    st.sidebar.checkbox("Roborace");
    st.sidebar.checkbox("Armour Wars");

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("PRN")
    with col2:
        st.header("Name")
    with col3:
        st.header("Division")
    with col4:
        st.header("Temperature")

    # rows = run_query("SELECT student.PRN, student.name, student.division FROM student INNER JOIN roboraceevent ON student.PRN=roboraceevent.PRN;")

    # for row in rows:
    #         with col1:
    #             st.write(f"{row[0]}")
    #         with col2:
    #             st.write(f"{row[1]}")
    #         with col3:
    #             st.write(f"{row[2]}")

    while True:
        # ans=st.sidebar.radio("Roborace",('Click','Unclick'))
        TS = request.urlopen("http://api.thingspeak.com/channels/2108652/feeds/last.json?api_key="+st.secrets["api_key"]);
        response = TS.read()
        datawebsite=json.loads(response)

    # print(data);
        a = datawebsite['created_at']
        # b = datawebsite['field1']
        c = datawebsite['field2']

        ambient=0;
        object=0;
        temp=0;
        # print("\n");
        # print(a);
        # print("\n");
        # if(b!=None):
        #     ambient=float(b);
        #     temp=ambient
            # print(b);
            # print("\n");
    
        if(c!=None):
            object=float(c);
            temp=object
            # print(c);
            # print("\n");  
        
        ret, frame = cap.read()

        data = decode(frame)

        if data is not None and data != prev_data:
            # st.write(data)
            # st.write(type(data))
            prev_data = data
            # PRNdata=int(data)
            # st.write(type(PRNdata))
            # rows = run_query("CALL projectFetchCheckin("+data+");")
            # if((ambient<=100.4) or (object<=100.4)):
            if((object<=100.4)):
                rows = run_query("SELECT student.PRN, student.name, student.division FROM student where PRN="+data+";")
                for row in rows:
                    with col1:
                        st.write(f"{row[0]}")
                    with col2:
                        st.write(f"{row[1]}")
                    with col3:
                        st.write(f"{row[2]}")
                    with col4:
                        st.write(temp)
            else:
                for row in rows:
                    with col1:
                        st.write(f"{row[0]}")
                    with col2:
                        st.write(f"{row[1]}")
                    with col3:
                        st.write(f"{row[2]}")
                    with col4:
                        st.write("Danger"+f"{temp}")

        cv2.imshow('QRCode Scanner', frame)

        
        # if ans=='Click':
        #     rows = run_query("SELECT student.PRN, student.name, student.division FROM student INNER JOIN roboraceevent ON student.PRN=roboraceevent.PRN where student.PRN=@data;")

        # for row in rows:
        #     with col1:
        #         st.write(f"{row[0]}")
        #     with col2:
        #         st.write(f"{row[1]}")
        #     with col3:
        #         st.write(f"{row[6]}")
        TS.close()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    scan()