import nltk, sys, json
from itertools import tee, izip

def slice_document(transcript_file, output_folder):
    
    with open(transcript_file, 'r') as file:
        raw = file.read()

    raw = raw.replace('\x92', "'")
    tokens = nltk.word_tokenize(raw)
    words = [w.lower() for w in tokens if w.isalnum()]
    
    print 'Number of tokens: ', len(tokens)
    print 'Number of words: ', len(words)

    
    i = 1
    path = output_folder + '/'
    
    for each in window(words, 100):
        print list(each)
        with open(path + 'window' + str(i) + '.txt', 'w') as f:
            json.dump(each, f)
        i += 1
            

def window(iterable, size):
    iters = tee(iterable, size)
    for i in xrange(1, size):
        for each in iters[i:]:
            next(each, None)
    return izip(*iters)
    
    
def main():
    transcript_file = sys.argv[1]
    output_folder = sys.argv[2]

    slice_document(transcript_file, output_folder)


if __name__ == '__main__':
    main()
