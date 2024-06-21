import streamlit as st
import pyrebase
from firebase_config import firebaseConfig
import requests
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# db = firebase.database()
storage = firebase.storage()


def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Account created successfully!')
    except Exception as e:
        st.error(e)


# main ui component
def mainui():
    try:
        st.sidebar.success('Logged in as {}'.format(st.session_state['user']['email']))

        uploaded_file = st.file_uploader("Choose a call transcript", type="txt")

        if uploaded_file is not None:
            # Display the uploaded transcript
            transcript = uploaded_file.read().decode('utf-8')
            st.text_area("Uploaded Transcript", transcript, height=300)

            # Save the uploaded file
            with open("uploaded_transcript.txt", "w") as f:
                f.write(transcript)

            if st.button("Analyze Sentiment"):
                files = {'file': open("uploaded_transcript.txt", 'rb')}
                response = requests.post("https://backend-ij7jryptz-goodtobetrue2gmailcoms-projects.vercel.app/upload", files=files)
                
                if response.status_code == 200:
                    sentiment_results = response.json()
                    st.write("Sentiment Analysis Results:")
                    st.write(sentiment_results)

                    # Visualization (Pie Chart)
                    sentiments = [result['label'] for result in sentiment_results]
                    sentiment_df = pd.DataFrame(sentiments, columns=['Sentiment'])
                    sentiment_counts = sentiment_df['Sentiment'].value_counts()
                    
                    fig, ax = plt.subplots()
                    sentiment_counts.plot.pie(autopct='%1.1f%%', ax=ax)
                    ax.set_ylabel('')
                    ax.set_title('Sentiment Distribution')
                    st.pyplot(fig)

                else:
                    st.write("Error in sentiment analysis")
    except Exception as e:
        st.error(e)

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success('Logged in successfully!')
        st.session_state['logged_in'] = True
        st.session_state['user'] = user
    except Exception as e:
        st.error(e)
# Non fnctn part starts here
st.title('Sentiment Analysis on Call Transcripts')

# Authentication check
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.sidebar.title('Login / Sign Up')
    choice = st.sidebar.selectbox('Choose Action', ['Login', 'Sign Up'])

    email = st.sidebar.text_input('Email')
    password = st.sidebar.text_input('Password', type='password')

    if choice == 'Sign Up':
        if st.sidebar.button('Sign Up'):
            signup(email, password)
    else:
        if st.sidebar.button('Login'):
            login(email, password)
    print(st.session_state['logged_in'])
if st.session_state['logged_in']:
    # Main UI
    st.sidebar.success('Logged in as {}'.format(st.session_state['user']['email']))

    uploaded_file = st.file_uploader("Choose a call transcript", type="txt")

    if uploaded_file is not None:
        # Display the uploaded transcript
        transcript = uploaded_file.read().decode('utf-8')
        st.text_area("Uploaded Transcript", transcript, height=300)

        # Save the uploaded file
        with open("uploaded_transcript.txt", "w",encoding="utf-8") as f:
            f.write(transcript)

        if st.button("Analyze Sentiment"):
            files = {'file': open("uploaded_transcript.txt", 'rb')}
            response = requests.post("http://localhost:5000/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                chunk_results = data["chunk_results"]
                aggregated_results = data["aggregated_results"]
               
                # # sentiments = [result['label'] for result in aggregated_results]
                # sentiment_df = pd.DataFrame(aggregated_results, columns=['Sentiment',"Score"])
                # sentiment_counts = pd.Series(sentiment_df,index=sentiment_df.iloc[0])
                
                # fig, ax = plt.subplots()
                # sentiment_df.plot.pie(autopct='%1.1f%%', ax=ax)
                # ax.set_ylabel('')
                # ax.set_title('Sentiment Distribution')
                # st.pyplot(fig)

                
                st.subheader('Aggregated Sentiment Analysis Results')
                st.write(aggregated_results)

                
                st.subheader('Sentiment Analysis Results by Chunk')
                df = pd.DataFrame(chunk_results)
                st.dataframe(df)

                
                st.subheader('Sentiment Analysis Visualization')
                fig = px.bar(df, x="label", y="score", color="label", title="Sentiment Analysis by Chunk")
                st.plotly_chart(fig)

            else:
                st.write("Error in sentiment analysis")

 
    if st.sidebar.button('Logout'):
        st.session_state['logged_in'] = False
        st.session_state['user'] = None
        st.experimental_rerun()

# if __name__ =="__main__":
#     st.title('Sentiment Analysis on Call Transcripts')
#     if 'logged_in' not in st.session_state:
#         st.session_state['logged_in'] = False
#     sidebarTitle = None
#     sidebarSelectionBox=st.sidebar.selectbox
#     emailInput = st.sidebar.text_input
#     passwordInput = st.sidebar.text_input
#     ctaButton = st.sidebar.button

#     if not st.session_state['logged_in']:
#         sidebarTitle=st.sidebar.title('Login/Sign Up')
#         choice = sidebarSelectionBox('Choose Action', ['Login', 'Sign Up'],key="sidebar__choice")

#         email = emailInput('Email')
#         password = passwordInput('Password', type='password')

#         if choice == 'Sign Up':
#             if ctaButton('Sign Up'):
#                 signup(email, password)
#         else:
#             if ctaButton('Login'):
#                 login(email, password)
    