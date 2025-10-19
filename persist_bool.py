from langchain_core.output_parsers import BaseOutputParser

import pandas as pd 
import numpy as np 
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

class SentimentAnalyzer(BaseOutputParser):
    
    def parse(self, text: str) -> bool:

        """        
        Args:
            text (str): LLM response text to analyze
            
        Returns:
            bool: True if positive sentiment dominates, False if negative
        """

        scores = self.get_scores(text)
        return scores['positive'] > scores['negative']
    
    def get_scores(self, text):
        
        """
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary containing positive and negative sentiment scores
        """
        
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        
        encoded_input = tokenizer(text, return_tensors='pt')
        
        with torch.no_grad():
            output = model(**encoded_input)
        
        scores = output.logits[0].detach().numpy()
        scores = softmax(scores)
        
        neg_score = float(scores[0])
        pos_score = float(scores[2])
        
        return {
            'positive': pos_score,
            'negative': neg_score
        }
    
    @property
    def _type(self) -> str:
        return "sentiment_analyzer"