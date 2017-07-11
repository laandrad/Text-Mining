import types
import io
import re
import nltk


class DTM:
    """"This is an object for quantitative representation of documents"""

    def __init__(self, vocabulary, documents, features):
        self.vocabulary = vocabulary
        self.documents = documents
        self.features = features

    def compute_dtm(self):
        # 1. extract term frequencies from each text document - a.k.a. frequency vectors
        # 2. bind all frequency vectors into a dtm matrix
        dtm = {}
        for d in self.documents:
            a = [word for doc, word in self.features if doc == d]
            dtv = [a.count(word) for word in self.vocabulary]  # vector of frequencies per vocabulary term
            # print d, sum(dtv)
            dtm[d] = dtv

        return dtm

    def compute_dtv(self):
        dtv = {}
        a = [word for doc, word in self.features]
        a = [a.count(word) for word in self.vocabulary]
        dtv[self.documents] = a
        # print self.documents, sum(a)

        return dtv


class ExtractFeatures:
    """This is an object for feature extraction"""

    def __init__(self, method, bigrams):
        # self.data = []
        self.method = method
        self.bigrams = bigrams

    def extract_features_from_file(self, file_path):
        """This method extracts features from a document given in path"""
        assert isinstance(file_path, types.StringType)
        assert [x for x in ['a', 'n'] if self.method in x] is not None
        assert [x for x in ['True', 'False'] if self.bigrams in x] is not None

        print "Extracting features from file: " + file_path

        if self.method == 'n':
            print "Using method: Nouns"
        else:
            print "Using method: Nouns + Adverbs"

        print "Using bigrams: " + self.bigrams

        name = file_path.split("\\")
        name = name[-1]
        name = name.split('.')
        name = name[0]

        raw = io.open(file_path, "r", encoding="utf-8", errors='ignore')
        # sentences = raw.splitlines()

        features = []
        for s in raw:
            words = self._prepare_text(s)
            features = features + words

        category = []
        for i in range(len(features)):
            category.append(name)

        return zip(category, features)

    def extract_features_from_text(self, text_file, name):
        """This method extracts features from a given text"""

        assert isinstance(text_file, types.UnicodeType)
        assert [x for x in ['a', 'n'] if self.method in x] is not None
        assert [x for x in ['True', 'False'] if self.bigrams in x] is not None

        print "Extracting features from text..."

        if self.method == 'n':
            print "Using method: Nouns"
        else:
            print "Using method: Nouns + Adverbs"

        print "Using bigrams: " + self.bigrams
        
        sentences = text_file.splitlines()

        features = []
        for s in sentences:
            words = self._prepare_text(s)
            features = features + words

        category = []
        for i in range(len(features)):
            category.append(name)

        return zip(category, features)

    def _prepare_text(self, s):
        porter = nltk.PorterStemmer()

        nouns = ['NN', 'NNP', 'NNS']
        advs = ['JJ', 'VBN']

        if self.method == 'n':
            pos_tags = nouns
        else:
            pos_tags = nouns + advs
        s = s.lower()
        s = re.sub(r'[^\w\s]', '', s)  # remove punctuation
        tokens = nltk.word_tokenize(s)
        words = [w for w in tokens if w.isalpha()]  # remove numbers
        tags = nltk.pos_tag(words)
        names = [w for w, t in tags if t in pos_tags]  # create POS tags
        names = [porter.stem(t) for t in names]  # stem words

        if self.bigrams == 'True':
            relations = list(nltk.bigrams(names))
        else:
            relations = []

        features = names + relations

        return features



