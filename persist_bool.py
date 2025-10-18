import pandas as pd 
import numpy as np 

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

from scipy.special import softmax

import torch

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"

class SentimentAnalyzer:

    def get_scores(self, text):
        
        """
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary containing positive and negative sentiment scores
                  {'positive': float, 'negative': float}
        """
        
        # Loading the tokenizer and model

        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        
        # Tokenizing and get model output
        
        encoded_input = tokenizer(text, return_tensors='pt')
        
        with torch.no_grad():
            output = model(**encoded_input)
        
        scores = output.logits[0].detach().numpy()
        scores = softmax(scores)
        
        # Default model labels: 0 = negative, 1 = neutral, 2 = positive
        
        neg_score = float(scores[0])
        pos_score = float(scores[2])
        
        return {
            'positive': pos_score,
            'negative': neg_score
        }

    def parse(self, text):

        """
        Args:
            text (str): Input text to analyze
            
        Returns:
            bool: True if positive sentiment dominates, False if negative dominates
        """
        
        scores = self.get_scores(text)
        return scores['positive'] > scores['negative']