import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer



transformer = TfidfTransformer()

vectorizer = CountVectorizer(lowercase=False, tokenizer=lambda x:x, stop_words=None, max_features=5000, ngram_range=(1, 1), binary=False)
stemmer = SnowballStemmer("english")
stopwords_en = set(stopwords.words('english'))

__tokenization_pattern = r'''(?x)          # set flag to allow verbose regexps
        \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
      | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
      | \w+(?:-\w+)*        # words with optional internal hyphens
      | \.\.\.              # ellipsis
      | [][.,;"'?():_`-]    # these are separate tokens; includes ],
    '''
tokenizer = nltk.tokenize.regexp.RegexpTokenizer(__tokenization_pattern)




def preprocessor(hd, lp, td):
    temp = []
    for i in {hd, lp, td}:
        if i != None:
            temp.append(i)
    text = ' '.join(temp).encode('utf-8')
    stems = []
    tokens = tokenizer.tokenize(text.lower())
    for token in tokens:
        if token.isalpha() and token not in stopwords_en:
            stems.append(str(stemmer.stem(token)))
    return stems
