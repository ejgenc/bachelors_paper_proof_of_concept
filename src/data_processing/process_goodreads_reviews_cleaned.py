# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This script ingests the file goodreads_reviews_cleaned.csv in order to process
it into a second level or analysis

This script targets the following file:
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    
The resulting csv file is located at:
    ../../data/raw/review_sentences_raw.csv
    
"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
import re #regex
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
review_sentences = pd.read_csv(import_fp)

# NLTK stopwords data
nltk.download('stopwords')

#%% --- Process: drop unnecessary columns ---

unnecessary_columns = ["date_scraped", "reviewer_id", "reviewer_name",
                       "review_date", "rating"]

review_sentences.drop(labels = unnecessary_columns,
                      axis = 1,
                      inplace = True)

review_sentences.reset_index(drop = True)

#%% --- Process: tokenize reviews into sentences ---

review_sentences["review"] = review_sentences["review"].apply(sent_tokenize)

#%% --- Process: expand individual sentences into different rows for tidy data ---

review_sentences = review_sentences.explode("review").reset_index(drop = True)

#%% --- Process: rename "review" column to "review_sentence"

review_sentences.rename({"review": "review_sentence"},
                        axis = "columns",
                        inplace = True)

#%% --- Process: tag each sentence with a sentence id ---

review_sentences["sentence_id"] = np.arange(len(review_sentences))
review_sentences["sentence_id"] = "s" + review_sentences["sentence_id"].astype(str)

#%% --- Process: calculate sentence length (in words), count stopwords too ---

review_sentences["length_in_words_with_stopwords"] = review_sentences["review_sentence"].str.split().str.len()

#%% --- Process: calculate sentence length (in words), don't count stopwords too ---

#create a temp copy of "review_sentence" column

review_sentences["TEMP"] = review_sentences["review_sentence"].copy()

#split the sentence from spaces for better removal

#review_sentences["TEMP"] = review_sentences["review_sentence"].str.split(" ")

#Use regex to remove "stopwords" from this column

pat = re.compile('|'.join(map(re.escape, stopwords.words("english"))))

review_sentences["TEMP"]  = [pat.sub('', text) for text in review_sentences['TEMP']]

#Calculate column "length_in_words_without_stopwords" using the intermediary column

#Drop intermediary column


#%% --- Export data ---

# export_fp = Path("../../data/raw/review_sentences_raw.csv")
# review_sentences .to_csv(export_fp, encoding = "utf-8", index = False)


