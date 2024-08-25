import streamlit as st
import pickle
import nltk
from nltk.stem.porter import PorterStemmer
import string
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt') 

ps = PorterStemmer()

# Load the model and vectorizer
try:
    model = pickle.load(open('model.pkl', 'rb'))
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model: {e}")

st.title("Spam Ham Classification")

# Text area for input
input_sms = st.text_area("Enter Mail to classify", placeholder="Type your email here...")

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)  # Tokenize the text

    y = [i for i in text if i.isalnum()]

    y = [ps.stem(i) for i in y if i not in stopwords.words('english') and i not in string.punctuation]

    return " ".join(y)

if st.button('Predict'):
    if not input_sms.strip():
        st.warning("Please enter some text to classify.")
    else:
        transformed_input = transform_text(input_sms)
        vectorized_input = tfidf.transform([transformed_input])
        result = model.predict(vectorized_input)

        if result == 1:
            st.header(":red[Spam]")
        else:
            st.header(":blue[Not Spam]")
