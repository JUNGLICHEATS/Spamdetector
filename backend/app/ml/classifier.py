import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import re
import string
from typing import Dict, List, Tuple
import os

class SpamClassifier:
    """Machine Learning based spam classifier"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.nb_classifier = MultinomialNB()
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.feature_names = []
        
        # Try to load pre-trained model
        self.load_model()
        
        # If no model exists, train with sample data
        if not self.is_trained:
            self.train_with_sample_data()
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for classification"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\d{3}-\d{3}-\d{4}|\d{10}', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_features(self, text: str) -> Dict[str, float]:
        """Extract additional features from text"""
        features = {}
        
        # Length features
        features['length'] = len(text)
        features['word_count'] = len(text.split())
        
        # Character features
        features['uppercase_ratio'] = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        features['digit_ratio'] = sum(1 for c in text if c.isdigit()) / max(len(text), 1)
        features['punctuation_ratio'] = sum(1 for c in text if c in string.punctuation) / max(len(text), 1)
        
        # Spam indicators
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['dollar_count'] = text.count('$')
        features['url_count'] = len(re.findall(r'http\S+|www\S+', text))
        
        # Urgency indicators
        urgency_words = ['urgent', 'hurry', 'act now', 'limited time', 'expires']
        features['urgency_score'] = sum(1 for word in urgency_words if word in text.lower())
        
        # Promotional words
        promo_words = ['free', 'win', 'winner', 'prize', 'offer', 'deal', 'discount']
        features['promo_score'] = sum(1 for word in promo_words if word in text.lower())
        
        return features
    
    def train_with_sample_data(self):
        """Train the classifier with sample spam/ham data"""
        # Sample training data
        spam_messages = [
            "URGENT! You've won $1,000,000! Click here NOW!",
            "Get rich quick! Make $5000 per week working from home!",
            "FREE VIAGRA! Best prices guaranteed! No prescription needed!",
            "CONGRATULATIONS! You're our lucky winner! Claim your prize now!",
            "Limited time offer! Act now or miss out forever!",
            "Your account will be closed! Click here to verify immediately!",
            "Amazing weight loss pills! Lose 50 pounds in 30 days!",
            "Hot singles in your area! Click to meet them now!",
            "Lowest mortgage rates! Apply now and save thousands!",
            "Make money online! No experience required! Start today!",
            "FREE iPhone! Just pay shipping! Limited quantity!",
            "URGENT TAX REFUND! Click here to claim your money!",
            "Increase your income by 500%! Guaranteed results!",
            "WARNING: Your computer is infected! Download now!",
            "Get paid to take surveys! $100 per hour guaranteed!"
        ]
        
        ham_messages = [
            "Hi, I'm interested in your web development services.",
            "Thank you for the great presentation at the conference.",
            "Could you please send me more information about pricing?",
            "I would like to schedule a meeting next week.",
            "The project looks interesting. Let's discuss further.",
            "I attended your workshop and found it very helpful.",
            "Can you help me with a technical issue I'm experiencing?",
            "I'm looking for a reliable web development partner.",
            "Your portfolio is impressive. I'd like to work with you.",
            "Could we set up a call to discuss the requirements?",
            "I need assistance with my website's contact form.",
            "The proposal you sent looks good. When can we start?",
            "I'm interested in learning more about your services.",
            "Thanks for the quick response to my previous email.",
            "I have some questions about the project timeline."
        ]
        
        # Create training dataset
        messages = spam_messages + ham_messages
        labels = [1] * len(spam_messages) + [0] * len(ham_messages)  # 1 for spam, 0 for ham
        
        # Preprocess messages
        processed_messages = [self.preprocess_text(msg) for msg in messages]
        
        # Fit vectorizer and transform texts
        X_text = self.vectorizer.fit_transform(processed_messages)
        
        # Extract additional features
        additional_features = []
        for msg in processed_messages:
            features = self.extract_features(msg)
            additional_features.append(list(features.values()))
        
        # Combine text features with additional features
        X_additional = np.array(additional_features)
        X = np.hstack([X_text.toarray(), X_additional])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=0.2, random_state=42
        )
        
        # Train classifiers
        self.nb_classifier.fit(X_train, y_train)
        self.rf_classifier.fit(X_train, y_train)
        
        # Evaluate
        nb_pred = self.nb_classifier.predict(X_test)
        rf_pred = self.rf_classifier.predict(X_test)
        
        nb_accuracy = accuracy_score(y_test, nb_pred)
        rf_accuracy = accuracy_score(y_test, rf_pred)
        
        print(f"Naive Bayes Accuracy: {nb_accuracy:.3f}")
        print(f"Random Forest Accuracy: {rf_accuracy:.3f}")
        
        self.is_trained = True
        self.feature_names = self.vectorizer.get_feature_names_out().tolist()
        
        # Save the model
        self.save_model()
    
    def predict(self, message: str) -> Dict[str, float]:
        """Predict if a message is spam or ham"""
        if not self.is_trained:
            raise ValueError("Model is not trained yet")
        
        # Preprocess the message
        processed_message = self.preprocess_text(message)
        
        # Transform text
        X_text = self.vectorizer.transform([processed_message])
        
        # Extract additional features
        additional_features = self.extract_features(processed_message)
        X_additional = np.array([list(additional_features.values())])
        
        # Combine features
        X = np.hstack([X_text.toarray(), X_additional])
        
        # Get predictions from both classifiers
        nb_prob = self.nb_classifier.predict_proba(X)[0][1]  # Probability of spam
        rf_prob = self.rf_classifier.predict_proba(X)[0][1]  # Probability of spam
        
        # Combine probabilities (ensemble)
        combined_prob = (nb_prob + rf_prob) / 2
        
        return {
            'confidence': combined_prob,
            'nb_probability': nb_prob,
            'rf_probability': rf_prob,
            'prediction': 'spam' if combined_prob > 0.5 else 'ham'
        }
    
    def get_feature_importance(self, message: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """Get the most important features for a prediction"""
        if not self.is_trained:
            return []
        
        processed_message = self.preprocess_text(message)
        X_text = self.vectorizer.transform([processed_message])
        
        # Get feature weights
        feature_weights = []
        text_features = X_text.toarray()[0]
        
        for i, weight in enumerate(text_features):
            if weight > 0 and i < len(self.feature_names):
                feature_weights.append((self.feature_names[i], weight))
        
        # Sort by weight and return top N
        feature_weights.sort(key=lambda x: x[1], reverse=True)
        return feature_weights[:top_n]
    
    def save_model(self):
        """Save the trained model to disk"""
        try:
            os.makedirs('models', exist_ok=True)
            
            model_data = {
                'vectorizer': self.vectorizer,
                'nb_classifier': self.nb_classifier,
                'rf_classifier': self.rf_classifier,
                'feature_names': self.feature_names,
                'is_trained': self.is_trained
            }
            
            with open('models/spam_classifier.pkl', 'wb') as f:
                pickle.dump(model_data, f)
            
            print("Model saved successfully")
            
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self):
        """Load a pre-trained model from disk"""
        try:
            with open('models/spam_classifier.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.nb_classifier = model_data['nb_classifier']
            self.rf_classifier = model_data['rf_classifier']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
            
            print("Model loaded successfully")
            
        except FileNotFoundError:
            print("No pre-trained model found. Will train new model.")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def retrain(self, new_messages: List[str], new_labels: List[int]):
        """Retrain the model with new data"""
        if not self.is_trained:
            raise ValueError("Initial model must be trained first")
        
        # Preprocess new messages
        processed_messages = [self.preprocess_text(msg) for msg in new_messages]
        
        # Transform texts
        X_text = self.vectorizer.transform(processed_messages)
        
        # Extract additional features
        additional_features = []
        for msg in processed_messages:
            features = self.extract_features(msg)
            additional_features.append(list(features.values()))
        
        # Combine features
        X_additional = np.array(additional_features)
        X = np.hstack([X_text.toarray(), X_additional])
        
        # Partial fit for incremental learning
        self.nb_classifier.partial_fit(X, new_labels)
        
        # For Random Forest, we need to retrain completely
        # This is a limitation of scikit-learn's RandomForest
        print("Note: Random Forest requires complete retraining with new data")
        
        # Save updated model
        self.save_model()
    
    def get_model_stats(self) -> Dict[str, any]:
        """Get model statistics"""
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        return {
            "is_trained": self.is_trained,
            "feature_count": len(self.feature_names),
            "vectorizer_vocab_size": len(self.vectorizer.vocabulary_),
            "model_types": ["Naive Bayes", "Random Forest"]
        }