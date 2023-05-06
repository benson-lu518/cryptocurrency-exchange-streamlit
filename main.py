#main
from pathlib import Path
from navigation import dashboard_yf, trading, membercenter,history

import streamlit as st  
import streamlit_authenticator as stauth  
from dao.UserDao import UserDao
#https://emojipedia.org/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

import sqlite3 
conn = sqlite3.connect('data.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
registerState=True
loginState=True

def fetch_data():
    allUsernames=UserDao.getAllUsernames()
    allUserpasswds=UserDao.getAllPasswords()
    hashed_passwords = stauth.Hasher(allUserpasswds).generate()
    return allUsernames,hashed_passwords


def add_userdata(username,password,cash=0):
    userInfoByusername=UserDao.getUserByUsername(username)
    userInfoBypassword=UserDao.getUserByPassword(password)

    if len(userInfoByusername) !=0:
        st.warning("Usernames has been registered ")
    elif len(userInfoBypassword) != 0:
        st.warning("Password has been registered ")
    else:
        UserDao.insertUser(username,password,cash)
        st.success("You have successfully created a valid Account")


if loginState:
    #get registered users 
    names,hashed_passwords=fetch_data()
    credentials = {"usernames":{}} #to yaml format 
    for un, n, pw in zip(names, names, hashed_passwords):
        user_dict = {"name":n,"password":pw}
        credentials["usernames"].update({un:user_dict})

    #login
    authenticator = stauth.Authenticate(credentials, "app_home", "auth",cookie_expiry_days=30,preauthorized=True)

    name, authentication_status, username = authenticator.login("Login", "main")
   
if authentication_status == False:
    
    st.error("Useraccount/password is incorrect")

if authentication_status == None:

    st.warning("Please enter your username and password")

if authentication_status:
    registerState=False
    loginState=False
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.image(
    "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/z3ahdkytzwi1jxlpazje",
    width=50)

    pages = {
        '🏠 Member Center':membercenter.page,
        '📈 Crypto Dashboard': dashboard_yf.page,
        '💰 Trading System': trading.page,
        '✅ Trading hitory': history.page
    }

    selected_page = st.sidebar.radio("Navigation", pages.keys())
    pages[selected_page](name)

if registerState:
    try:
        if authenticator.register_user(form_name='Register user',preauthorization=False):
            username=credentials['usernames'][str(list(credentials['usernames'])[-1])]['name']
            password=credentials['usernames'][str(list(credentials['usernames'])[-1])]['password']
            
            print(username)
            print(password)
            add_userdata(username,password,cash=0)

    except Exception as e:
        st.error(e)
