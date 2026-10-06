import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialogue

def teacher_screen():

  style_base_layout()
  style_background_dashboard()
  if 'teacher_data' in st.session_state:
    teacher_dashboard()
  elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
    teacher_screen_login()
  elif st.session_state.teacher_login_type == 'register':
    teacher_screen_register()

  footer_dashboard()

def teacher_dashboard():

  style_base_layout()
  style_background_dashboard()

  teacher_data = st.session_state.teacher_data

  col1,col2 = st.columns(2,gap="xxlarge",vertical_alignment='center')

  with col1:
    header_dashboard()
  with col2:
    st.subheader(f"""Welcome,{teacher_data['name']}""")
    if st.button('Logout',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
      st.session_state['is_logged_in'] = False
      del st.session_state.teacher_data
      st.rerun()

  st.space()
  st.space()

  if 'current_teacher_tab' not in st.session_state:
    st.session_state.current_teacher_tab = 'take_attendance'

  tab1,tab2,tab3 = st.columns(3)

  with tab1:
    type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
    if st.button('Take Attendance',width='stretch',type=type1,icon=':material/ar_on_you:'):
      st.session_state.current_teacher_tab = 'take_attendance'
      st.rerun()

  with tab2:
    type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
    if st.button('Manage Subjects',width='stretch',type=type2,icon=':material/book_ribbon:'):
      st.session_state.current_teacher_tab = 'manage_subjects'
      st.rerun()

  with tab3:
    type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
    if st.button('Attendance Records',width='stretch',type=type3,icon=':material/cards_stack:'):
      st.session_state.current_teacher_tab='attendance_records'
      st.rerun()

  st.divider()

  if st.session_state.current_teacher_tab == 'take_attendance':
    teacher_tab_take_attendance()
  if st.session_state.current_teacher_tab == 'manage_subjects':
    teacher_tab_manage_subjects()
  if st.session_state.current_teacher_tab == 'attendance_records':
    teacher_tab_attendance_records()

def teacher_tab_take_attendance():
  st.header("Take Attendance")

def teacher_tab_manage_subjects():
  teacher_id = st.session_state.teacher_data['teacher_id']
  col1,col2 = st.columns(2)
  with col1:
    st.header("Manage subjects")
  with col2:
    if st.button('Create New Subject',width='stretch'):
      create_subject_dialog(teacher_id)

  #List all subjects
  subjects = get_teacher_subjects(teacher_id)
  if subjects:
    for sub in subjects:
      stats = [
        ("👥","Students",sub['total_students']),
        ("🕰️","Classes",sub['total_classes'])
      ]

    def share_btn():
      if st.button(f'Share Code : {sub['name']}',key=f'share_{sub['subject_code']}',icon=':material/share:'):
        share_subject_dialogue(sub['name'],sub['subject_code'])

      st.space()

    subject_card(
      name = sub['name'],
      code = sub['subject_code'],
      section = sub['section'],
      stats = stats,
      footer_callback = share_btn
    )

  else:
    st.info('No Subjects Found. Create One Above.')


def teacher_tab_attendance_records():
  st.header("Attendance records")



def login_teacher(teacher_username,teacher_pass):
  if not teacher_username or not teacher_pass:
    return False
  teacher= teacher_login(teacher_username,teacher_pass)
  if teacher:
    st.session_state.user_role = 'teacher'
    st.session_state.teacher_data = teacher
    st.session_state.is_logged_in=True
    return True

  return False

def teacher_screen_login():
  col1,col2 = st.columns(2,gap="xxlarge",vertical_alignment='center')
  with col1:
    header_dashboard()
  with col2:
    if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
      st.session_state['login_type'] = None
      st.rerun()
  
  st.header('Login using Password',text_alignment='center')
  st.space()
  st.space()

  teacher_username = st.text_input('Enter username',placeholder='@abhishek')
  teacher_pass = st.text_input('Enter Password',placeholder='Enter your password',type='password')

  st.divider()

  btnc1,btnc2 = st.columns(2,gap='medium')
  with btnc1:
    if st.button('Login',shortcut='control+enter',width='stretch',icon=':material/passkey:'):
      if login_teacher(teacher_username,teacher_pass):
        st.toast("Welcome back!")
        import time
        time.sleep(2)
        st.rerun()
      else:
        st.error("Invalid username or password!")
  with btnc2:
    if st.button('Register Instead',type='primary',width='stretch',icon=':material/passkey:'):
      st.session_state.teacher_login_type ='register'
      st.rerun()

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
  if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
    return False,"All fields are required"
  if check_teacher_exists(teacher_username):
    return False,"Username already exists"
  if teacher_pass != teacher_pass_confirm:
    return False,"Password does not match"
  try:
    create_teacher(teacher_username,teacher_pass,teacher_name)
    return True,"Successfully registered! Login Now"
  except Exception as e:
    return False,"Unexpected Error!"

def teacher_screen_register():
  col1,col2 = st.columns(2,gap="xxlarge",vertical_alignment='center')
  with col1:
    header_dashboard()
  with col2:
    if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
      st.session_state['login_type']= None
      st.rerun()
  
  st.header('Register your Teacher Profile')
  st.space()
  st.space()

  teacher_username = st.text_input('Enter username',placeholder='@abhishek')
  teacher_name = st.text_input('Enter name',placeholder='Abhishek Sharma')
  teacher_pass = st.text_input('Enter password',placeholder='Enter your password',type='password')
  teacher_pass_confirm = st.text_input('Confirm password',placeholder='Confirm your password',type='password')

  st.divider()

  btnc1, btnc2= st.columns(2)
  with btnc1:
    if st.button('Register Now',icon=':material/passkey:',shortcut='control+enter',type='primary',width='stretch'):
      success,Message = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
      if success:
        st.success(Message)
        import time
        time.sleep(2)
        st.session_state.teacher_login_type='login'
        st.rerun()
      else:
        st.error(Message)
  with btnc2:
    if st.button('Login Instead',icon=':material/passkey:',width='stretch'):
      st.session_state.teacher_login_type = 'login'
      st.rerun()