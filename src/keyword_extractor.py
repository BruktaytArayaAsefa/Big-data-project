import spacy
from sklearn.feature_extraction.text import TfidfVectorizer 
import numpy as np

# Load the spaCy model (this assumes you have installed the spaCy model 'en_core_web_sm')
nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_abstract(abstract, top_n=10):
    if not abstract:
        return []
    
    # Process the abstract using spaCy
    doc = nlp(abstract)

    # Extract candidate keywords based on noun phrases and proper nouns
    candidates = [chunk.text for chunk in doc.noun_chunks] + [ent.text for ent in doc.ents]

    # If no candidates are found, return an empty list
    if not candidates:
        return []

    # Compute TF-IDF scores for the candidates
    vectorizer = TfidfVectorizer(vocabulary=list(set(candidates)))
    tfidf_matrix = vectorizer.fit_transform([abstract])
    scores = np.asarray(tfidf_matrix.sum(axis=0)).flatten()

    # Create a dictionary of candidates and their TF-IDF scores
    candidate_scores = {word: score for word, score in zip(vectorizer.get_feature_names_out(), scores)}

    # Sort candidates by their TF-IDF scores in descending order
    sorted_candidates = sorted(candidate_scores.items(), key=lambda item: item[1], reverse=True)

    # Return the top N keywords
    return [keyword for keyword, score in sorted_candidates[:top_n]]

