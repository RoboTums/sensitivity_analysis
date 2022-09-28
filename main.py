import streamlit as st
if "shared" not in st.session_state:
        #initialize session state

   st.session_state["shared"] = True
   st.session_state['variates'] = 1000
   st.session_state['consensus'] = {}
   st.session_state['consensus']['rev'] = {}
   st.session_state['consensus']['gm'] = {}
   st.session_state['consensus']['sm'] = {}
   st.session_state['consensus']['ga'] = {}
   st.session_state['consensus']['rd'] = {}
   st.session_state['consensus']['da'] = {}

   st.session_state['users'] = {}
   st.session_state['users']['rev'] = {}
   st.session_state['users']['gm'] = {}
   st.session_state['users']['sm'] = {}
   st.session_state['users']['ga'] = {}
   st.session_state['users']['rd'] = {}
   st.session_state['users']['da'] = {}
    # 

st.write('Here we can have the motivation of this ')
