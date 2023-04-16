import streamlit as st
from PIL import Image
import numpy as np
import pyzbar.pyzbar as pyzbar
import pyqrcode
from pyzbar.pyzbar import ZBarSymbol

def decode(im):
    # Decode QR code and barcode from the image using PyZBar library
    decoded_objs = pyzbar.decode(im, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

    # Loop through all decoded objects and return the data
    for obj in decoded_objs:
        return obj.data.decode('utf-8')
    
img_file_buffer = st.camera_input("Take a picture")

prev_data = None  

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    data = decode(img_array)

    if data is not None and data != prev_data:
        st.write(data)
        prev_data = data

    # If data is not None and it is different from the previous data, print it on the console and update the previous data

    # Check the type of img_array:
    # Should output: <class 'numpy.ndarray'>
    st.write(type(img_array))

    # Check the shape of img_array:
    # Should output shape: (height, width, channels)
    st.write(img_array.shape)


# import streamlit as st

# from PIL import Image
# import numpy as np
# import cv2

# def qr_code_dec(image):
    
#     decoder = cv2.QRCodeDetector()
    
#     data, vertices, rectified_qr_code = decoder.detectAndDecode(image)
    
#     if len(data) > 0:
#         print("Decoded Data: '{}'".format(data))

#     # Show the detection in the image:
#         show_qr_detection(image, vertices)
        
#         rectified_image = np.uint8(rectified_qr_code)
        
#         decoded_data = 'Decoded data: '+ data
        
#         rectified_image = cv2.putText(rectified_image,decoded_data,(50,350),fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale = 2,
#             color = (250,225,100),thickness =  3, lineType=cv2.LINE_AA)
        
        
#         return decoded_data

# decoded_data = qr_code_dec(np.array(Image.open('image2.jpg')))
# st.markdown(decoded_data)
# # qr_code_dec();