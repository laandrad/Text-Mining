import nltk, os, numpy as np, csv, sys

def get_dtm(path, dtm_file):
    query = sorted(get_imlist(path)) # the text files in folder
    subject = [query[i][-13:-4] for i in range(len(query))] # extract the subject name
                
    # read the files and convert words into tokens
    terms_by_subject = []
    for i in range(len(subject)):
        terms = category_tokens(query[i], subject[i])
        terms_by_subject = terms_by_subject + terms

    # create a frequency distribution
    cfd = nltk.ConditionalFreqDist(terms_by_subject)
    
    # extract the terms/vocabulary across text files
    vocabulary = sorted(set(w[1] for w in terms_by_subject))
    print vocabulary
    
    # initilize file writing
    with open(dtm_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(vocabulary)

    # extract the frequencies to create a document-term matrix and write a csv file with the dtm
    dtm = []
    for ss in subject:
        dtv = [cfd[ss][word] for word in vocabulary] # vector of frequencies per vocabulary term
        print ss
        print dtv
    
        with open(dtm_file, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(dtv)


def get_imlist(path):
    # a function to extract all the txt files in a given folder
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.txt')]


def category_tokens(path, name):
    # a function to zip the words to a student label 
    with open(path, 'r') as file:
        raw = file.read()
    
    tokens = prepare_text(raw)

    category = []
    for i in range(len(tokens)):
        category.append(name)

    return zip(category, tokens)


def prepare_text(raw_text):
    # a function to retrieve a list of words after applying a given POS and stemmer filters
    raw = raw_text
    raw = raw.replace('\x92', "'")
    tokens = nltk.word_tokenize(raw) 
    words = [w.lower() for w in tokens if w.isalpha()]
    tags = nltk.pos_tag(words)

    nouns = ['NN', 'NNP', 'NNS']
    ##stop_words_tags = ['DT', 'PRP', 'IN', '.', ',', '(', ')', 'TO', 'RB']
    names = [w.lower() for w,t in tags if t in nouns] # normalize to lower and get only names and nouns

    porter = nltk.PorterStemmer()
    names = [porter.stem(t) for t in names]

    return names
    

def main():
    path = sys.argv[1]
    dtm_file = sys.argv[2]
    get_dtm(path, dtm_file)


if __name__ == '__main__':
    main()
