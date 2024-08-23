import streamlit as st 
import pickle 
import nltk
from nltk.stem.porter import PorterStemmer
import string
from nltk.corpus import stopwords
nltk.download('stopwords')


ps = PorterStemmer()

model  = pickle.load(open('model.pkl','rb'))
tfidf = pickle.load(open('vectorizer.pkl' , 'rb'))

st.title("Email|Spam Classification")

input_sms = st.text_area("Enter Mail to classify")
 
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y) 

if st.button('predict'):
    
    
    transformed_input = transform_text(input_sms)

    vectorized_input = tfidf.transform([transformed_input])

    result = model.predict(vectorized_input)

    if result == 1:
        st.header(":red[Spam]")
    else :
        st.header(":blue[Not Spam]")