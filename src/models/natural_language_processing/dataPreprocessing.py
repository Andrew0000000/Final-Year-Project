import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Ensure necessary NLTK resources are downloaded
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Tokenize the text
def tokenize_text(text):
    return word_tokenize(text)

# Remove stopwords from a list of tokens
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

# Lemmatize a list of tokens
def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in tokens]

# Preprocess a single description
def preprocess_description(text):
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return ' '.join(lemmatized_tokens)

# Preprocess all descriptions in a list and return a transformed list
def preprocess_description_list(description_list):
    return description_list.apply(preprocess_description)

# Vectorize a series of preprocessed documents
def vectorize_documents(preprocessed_text):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(preprocessed_text)