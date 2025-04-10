from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Function to preprocess text
def preprocess_text(message):
    words = message.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

# Load and preprocess dataset
data = pd.read_csv("sms_spam_dataset.csv", sep='\t', names=["Label", "Message"])
data['Label'] = data['Label'].map({'ham': 0, 'spam': 1})
data['Message'] = data['Message'].apply(preprocess_text)

# Train model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['Message'])
y = data['Label']

model = MultinomialNB()
model.fit(X, y)

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the message from the request
        message = request.json.get("message", "")
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Preprocess and predict
        processed_message = preprocess_text(message)
        vectorized_message = vectorizer.transform([processed_message])
        prediction = model.predict(vectorized_message)[0]
        return jsonify({"prediction": "Spam" if prediction == 1 else "Not Spam"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
