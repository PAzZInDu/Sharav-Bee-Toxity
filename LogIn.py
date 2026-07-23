import streamlit as st

IMAGE_ADDRESS = ("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNQ6CbMIl8D4ubya8YeWDAJh3saE-TIG8HK2v9j8J_IJ3cJxbRQgpFV4pI&s=10")

# Home page
st.title("Bee Toxicity Classification")

# Add an image
st.image(IMAGE_ADDRESS)


if not st.user.is_logged_in:
    if st.sidebar.button("Log in with Google", type="primary", icon=":material/login:"):
        st.login()

else:
    if st.sidebar.button("Log out", type="secondary", icon=":material/logout:"):
        st.logout()
        st.stop()