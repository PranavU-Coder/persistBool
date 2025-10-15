import pandas as pd
import re
from collections import Counter

class booleanPersistence:

    def __init__(self, affirmations_csv='data/affirmations.csv', non_affirmations_csv='data/non-affirmations.csv'):
        
        """
        So we initialize the counter by loading words from CSV files
        
        Args:
            affirmations_csv: This is a path to CSV file containing affirmation words
            non_affirmations_csv: and so this is the path to CSV file containing non-affirmation words
        """

        aff_df = pd.read_csv(affirmations_csv)
        self.affirmation_words = set(aff_df['word'].str.lower().tolist())
        
        non_aff_df = pd.read_csv(non_affirmations_csv)
        self.non_affirmation_words = set(non_aff_df['word'].str.lower().tolist())
        
        self.affirmation_count = 0
        self.non_affirmation_count = 0
        self.affirmation_details = Counter()
        self.non_affirmation_details = Counter()
        
        print(f"Loaded {len(self.affirmation_words)} affirmation words")
        print(f"Loaded {len(self.non_affirmation_words)} non-affirmation words")
    
    def quick_check(self, text):

        """
        This is based on simple check solution that booleanOutputParser implements, which works in most usecases
        However fails in scenarios where system prompt can lead to verbose output where the yes/no is properly encoded.
        """
        text_lower = text.lower()
        
        has_yes = bool(re.search(r'\byes\b', text_lower))
        if has_yes:
            return 'yes'
        
        # Check for no if yes not found
        
        has_no = bool(re.search(r'\bno\b', text_lower))
        if has_no:
            return 'no'
        
        return None


    def process_text(self, text):
        """
        Process text and count affirmation/non-affirmation words
        """
        
        # Always count - don't skip based on yes/no check!
        text_lower = text.lower()
        
        # Separating multi-word and single-word phrases
        multi_word_affirmations = {w for w in self.affirmation_words if len(w.split()) > 1}
        multi_word_non_affirmations = {w for w in self.non_affirmation_words if len(w.split()) > 1}
        
        single_word_affirmations = self.affirmation_words - multi_word_affirmations
        single_word_non_affirmations = self.non_affirmation_words - multi_word_non_affirmations
        
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
        
        words = re.findall(r'\b\w+\b', text_lower)
        
        for word in words:
            if word in single_word_affirmations:
                self.affirmation_count += 1
                self.affirmation_details[word] += 1
            elif word in single_word_non_affirmations:
                self.non_affirmation_count += 1
                self.non_affirmation_details[word] += 1
        
        # Do quick_check AFTER counting (informational only)
        quick_result = self.quick_check(text)
        
        return {
            'quick_check': quick_result,
            'skipped_detailed_count': False,
            'affirmation_count': self.affirmation_count,
            'non_affirmation_count': self.non_affirmation_count
        }
    
    def get_counts(self):

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
        Parser function that compares affirmation and non-affirmation counters
        Returns 'yes' if affirmations > non-affirmations, 'no' otherwise
        If counts are equal, defaults to 'no' (LLM is prolly hallucinating at that point)
        """

        if self.affirmation_count > self.non_affirmation_count:
            return 'yes'
        else:
            return 'no'