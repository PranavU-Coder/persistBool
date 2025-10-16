import pandas as pd
import re
from collections import Counter

class booleanPersistence:

    def __init__(self, affirmations_csv='data/affirmations.csv', non_affirmations_csv='data/non-affirmations.csv'):
        
        """
        Initialize the counter by loading words from CSV files
        
        Args:
            affirmations_csv: Path to the CSV file containing affirmative words
            non_affirmations_csv: Path to the CSV file containing non-affirmative words
        """
        
        aff_df = pd.read_csv(affirmations_csv)
        self.affirmation_words = set(aff_df['word'].str.lower().tolist())
        
        non_aff_df = pd.read_csv(non_affirmations_csv)
        self.non_affirmation_words = set(non_aff_df['word'].str.lower().tolist())
        
        self.affirmation_count = 0
        self.non_affirmation_count = 0
        self.affirmation_details = Counter()
        self.non_affirmation_details = Counter()
    
    def process_text(self, text):
        
        # Process text and classify them as affirmative or non-affirmative from lookup in files
        
        text_lower = text.lower()
        
        # Separate multi-word and single-word phrases
        
        multi_word_affirmations = {w for w in self.affirmation_words if len(w.split()) > 1}
        multi_word_non_affirmations = {w for w in self.non_affirmation_words if len(w.split()) > 1}
        
        single_word_affirmations = self.affirmation_words - multi_word_affirmations
        single_word_non_affirmations = self.non_affirmation_words - multi_word_non_affirmations
        
        # Count multi-word phrases first (they are harder to do so cause double-counting)

        for phrase in multi_word_affirmations:
            if phrase in text_lower:
                count = text_lower.count(phrase)
                self.affirmation_count += count
                self.affirmation_details[phrase] += count
                text_lower = text_lower.replace(phrase, ' ')
        
        for phrase in multi_word_non_affirmations:
            if phrase in text_lower:
                count = text_lower.count(phrase)
                self.non_affirmation_count += count
                self.non_affirmation_details[phrase] += count
                text_lower = text_lower.replace(phrase, ' ')
        
        # Count single words

        words = re.findall(r'\b\w+\b', text_lower)
        
        for word in words:
            if word in single_word_affirmations:
                self.affirmation_count += 1
                self.affirmation_details[word] += 1
            elif word in single_word_non_affirmations:
                self.non_affirmation_count += 1
                self.non_affirmation_details[word] += 1
    
    def get_counts(self):
        
        # for analysis and debugging at 2AM
        
        return {
            "affirmation_total": self.affirmation_count,
            "non_affirmation_total": self.non_affirmation_count,
            "affirmation_details": dict(self.affirmation_details),
            "non_affirmation_details": dict(self.non_affirmation_details)
        }
    
    def reset_counters(self):
        
        self.affirmation_count = 0
        self.non_affirmation_count = 0
        self.affirmation_details.clear()
        self.non_affirmation_details.clear()
    
    def print_summary(self):
        
        # Print a human-readable summary of counts for anyone that wants to cross verify 

        print(f"\nAffirmation words found: {self.affirmation_count}")
        print(f"Non-affirmation words found: {self.non_affirmation_count}")
        
        if self.affirmation_details:
            print("\nAffirmation breakdown:")
            for word, count in self.affirmation_details.most_common():
                print(f"  {word}: {count}")
        
        if self.non_affirmation_details:
            print("\nNon-affirmation breakdown:")
            for word, count in self.non_affirmation_details.most_common():
                print(f"  {word}: {count}")
    
    def parse(self):
        
        """
        Compare affirmation and non-affirmation counters
        Returns 'yes' if affirmations > non-affirmations, 'no' otherwise (usually the case of it being equal is super rare)
        """

        return 'yes' if self.affirmation_count > self.non_affirmation_count else 'no'