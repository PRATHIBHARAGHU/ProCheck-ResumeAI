import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

# Ensure systemic resources are compiled safely locally
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

class NLPPreprocessingService:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Safe internal programmatic fallback context if spacy model is not dynamically initialized via command line shell
            self.nlp = None
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        """
        Executes robust pipeline: lowercases text, matches regex strings for non-alphanumeric clearings, 
        tokenizes text, filters out functional stop words, and returns clear clean textual corpus tokens.
        """
        if not text:
            return ""
        
        # Lowercase and clean characters
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s\-\.\+#]', ' ', text)
        
        if self.nlp:
            doc = self.nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_space]
            return " ".join(tokens)
        else:
            # Fallback NLTK execution strategy
            tokens = word_tokenize(text)
            filtered_tokens = [w for w in tokens if w not in self.stop_words and len(w) > 1]
            return " ".join(filtered_tokens)