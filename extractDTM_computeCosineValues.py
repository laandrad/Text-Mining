import nltk, os, numpy as np, csv, sys
from scipy import spatial

def get_dtm(input_path, output_path, title, method, bigrams):
    ### This algorithm does two things:
    ### 1. It computes a document-term matrix for the text documents inside 'input_path' folder
    ### 2. It computes all pairwise cosine similarity values between the text documents  
    
    # get a path to the text files in 'input_path' folder
    query = sorted(get_imlist(input_path))
    
    # extract subject name for each text document
    subject = [query[i][-13:-4] for i in range(len(query))] 
                
    # read the text documents and convert words into tokens,
    # then bind all (tokens, subject) pairs into a list
    terms_by_subject = []
    for i in range(len(subject)):
        terms = category_tokens(query[i], subject[i], method, bigrams)
        terms_by_subject = terms_by_subject + terms
        print 'Preparing text vector for: ', subject[i]

    # create a frequency distribution from the (tokens, subject) list
    cfd = nltk.ConditionalFreqDist(terms_by_subject)
    
    # extract terms from each text document to create a vocabulary (keeping unique terms only)
    vocabulary = sorted(set(w[1] for w in terms_by_subject))
    # print vocabulary
    
    # initilize dtm file writer and write the header with the vocabulary
    # a 'title_dtm.csv' file will be written inside 'output_path' folder
    dtm_file = output_path + '/' + str(title) + '_dtm.csv'
    with open(dtm_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(vocabulary)

    # create a document-term matrix and write into csv file initialized above
    # 1. extract term frequencies from each text document - a.k.a. frequency vectors
    # 2. bind all frequency vectors into a dtm matrix
    dtm = []
    for ss in subject:
        dtv = [cfd[ss][word] for word in vocabulary] # vector of frequencies per vocabulary term
    
        with open(dtm_file, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(dtv)
        
        dtm.append(dtv)

    # initialize cosine similarity matrix file writer and write the header with the subject names
    # a 'title_cosine.csv' file will be written inside 'output_path' folder
    csm_file = output_path + '/' + str(title) + '_cosine.csv'
    with open(csm_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(subject)
    
    # compute a pairwise cosine values between (i, j) frequency vectors
    # bind all values into a matrix and write into csv file initialize above
    for i in xrange(len(dtm)):
        dv = []
        for j in xrange(len(dtm)):
            d = 1 - spatial.distance.cosine(dtm[j], dtm[i])
            print 'distance from document', i, 'to document', j, 'is', d
            dv.append(d)

        with open(csm_file, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(dv)
    


def get_imlist(path):
    ### This function extracts a path toward each txt file inside 'path' folder
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.txt')]


def category_tokens(path, name, method, bigrams):
    ### This function does two things:
    ### 1. read a text document from 'path' and convert words into token format 
    ### 2. Use 'name' argument to label to the extracted tokens
    with open(path, 'r') as file:
        raw = file.read()
    
    tokens = prepare_text(raw, method, bigrams)

    category = []
    for i in range(len(tokens)):
        category.append(name)

    return zip(category, tokens)


def prepare_text(raw_text, method = 1, bigrams = False):
    ### This function does four things to retrieve only names and nouns in 'raw_text':
    ### 1. retrieve a list of words from a 'raw_text' file
    ### 2. tokenize words in list using NLTK 
    ### 3. create part-of-speech (POS) tags per token
    ### 4. stem tokens using the Porter stemmer filter
    ### 5. method 1 uses nouns only, method 2 uses nouns and adverbs
    ### 6. Bigrams, boolean variable, that would additionally include bigrams
    raw = raw_text
    raw = raw.replace('\x92', "'")
    
    porter = nltk.PorterStemmer()    
    
    nouns = ['NN', 'NNP', 'NNS']
    advs = ['JJ', 'VBN']
    if method == '1':
        pos_tags = nouns
    else:
        pos_tags = nouns + advs

    sentences = raw.split('.')
    
    document = []
    for s in sentences:
        tokens = nltk.word_tokenize(s) 
        words = [w.lower() for w in tokens if w.isalpha()]
        print 'creating POS tags'
        tags = nltk.pos_tag(words)
        names = [w.lower() for w,t in tags if t in pos_tags]
        names = [porter.stem(t) for t in names]
        
        if bigrams == 'True':
            relations = list(nltk.bigrams(names)) 
        else:
            relations = []
            
        document = document + names + relations
    
    return document


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    title = sys.argv[3]
    method = sys.argv[4]
    bigrams = sys.argv[5]
    
    get_dtm(input_path, output_path, title, method, bigrams)


if __name__ == '__main__':
    main()
