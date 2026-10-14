import streamlit as st
from src.database.db import create_attendance

def show_attendance_result(df,logs):
  st.write('Please review attendance before confirming')
  st.dataframe(df,width='stretch',hide_index=True)
  
  c1,c2 = st.columns(2)
  
  with c1:
    if st.button('Discard',width='stretch'):
      st.session_state.voice_attendance_results=None
      st.session_state.attendance_images =[]

      st.rerun()
  
  with c2:
    if st.button('Confirm & Save',width='stretch',type='primary'):
      try:
        create_attendance(logs)
        st.toast('Attandance Taken')
        st.session_state.attendance_images = []
        st.session_state.voice_attendance_results = None
        st.rerun()
      except Exception as e:        
        st.error('Sync Failed')


@st.dialog('Attendance Report')
def attendance_result_dialog(df,logs):
  show_attendance_result(df,logs)
  