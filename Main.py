import streamlit as st
import streamlit_authenticator as stauth
from yaml import SafeLoader
import yaml
import extra_streamlit_components as stx

class LoginCheck(object):
    def __init__(self):
        with open('config.yaml') as file:
            self.config = yaml.load(file, Loader=SafeLoader)

        hashed_passwords = stauth.Hasher(['tomato', 'mango']).generate()

        for i, j in zip(self.config['credentials']['usernames'], hashed_passwords):
            self.config['credentials']['usernames'][i]['password'] = j

        self.authenticator = stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days'],
            self.config['preauthorized']
        )

        self.chosen_id = stx.tab_bar(data=[
            stx.TabBarItemData(id=1, title="Login", description="Existing Users"),
            stx.TabBarItemData(id=2, title="Register", description="New Users"),
            stx.TabBarItemData(id=3, title="Forgot Password", description=""),
            stx.TabBarItemData(id=4, title="Forgot Username", description=""),
        ], default=1)

        self.setup()

    def setup(self):
        if self.chosen_id == '1':
            name, authentication_status, username = self.authenticator.login('Login', 'main')

            if authentication_status:
                self.authenticator.logout('Logout', 'main')
                st.write(f'Welcome *{name}*')
                st.title('Some content')
            elif authentication_status == False:
                st.error('Username/password is incorrect')
            elif authentication_status == None:
                st.warning('Please enter your username and password')
        elif self.chosen_id == '2':
            # Register
            try:
                if self.authenticator.register_user('Register user', preauthorization=False):
                    st.success('User registered successfully')
                    with open('config.yaml', 'w') as file:
                        yaml.dump(self.config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)
        elif self.chosen_id == '3':
            # Forgot Password
            try:
                username_forgot_pw, email_forgot_password, random_password = self.authenticator.forgot_password(
                    'Forgot password')
                if username_forgot_pw:
                    st.success('New password sent securely')
                    # Random password to be transferred to user securely
                    with open('config.yaml', 'w') as file:
                        yaml.dump(self.config, file, default_flow_style=False)
                elif username_forgot_pw == False:
                    st.error('Username not found')
            except Exception as e:
                st.error(e)
        elif self.chosen_id == '4':
            # Forgot Username
            try:
                username_forgot_username, email_forgot_username = self.authenticator.forgot_username('Forgot username')
                if username_forgot_username:
                    st.success('Username sent securely')
                    # Username to be transferred to user securely
                    with open('config.yaml', 'w') as file:
                        yaml.dump(self.config, file, default_flow_style=False)
                elif username_forgot_username == False:
                    st.error('Email not found')
            except Exception as e:
                st.error(e)

if __name__ == "__main__":
    build = LoginCheck()













