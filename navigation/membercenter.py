#membercenter
import streamlit as st
from dao.UserDao import UserDao

def page(currentUser):

    # cash=str(getcash(currentUser))
    cash=UserDao.getCashByUsername(currentUser)
    st.title('Member Center 💥', anchor = "title")

    st.markdown(
    "### &emsp; &emsp;  Username:  &emsp; "+currentUser+"\n"+
    "### &emsp; &emsp;  Amount Available:  &emsp;"+str(round(cash,4))+" (USD)"
    )
    buff, col, buff2 = st.columns([0.03,0.1,0.5])
    charge = col.number_input(label ='Charge Section (USD)',max_value =1000000000)
    buff, bt, buff2 = st.columns([0.03,0.1,0.5])
    if bt.button('Charge'):
        chargeToDb(cash,charge,currentUser)
    

def chargeToDb(cash,charge,name):
    cash=float(cash)+float(charge)
    UserDao.updateCashByUsername(name,cash)
    st.experimental_rerun()