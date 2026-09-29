import streamlit as st
from src.ui.base_layout import style_base_layout,style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
import numpy as np
from PIL import Image

def student_screen():
  style_base_layout()
  style_background_dashboard()
  col1,col2 = st.columns(2,vertical_alignment='center')
  with col1:
    header_dashboard();
  with col2:
    st.button('Go back to Home',shortcut='control+backspace')

  st.header('Login with FaceID')
  st.space()
  st.space()

  photo_source = st.camera_input('Position your face in the center')
  if photo_source:
    np.array(Image.open(photo_source))
    
  footer_dashboard()