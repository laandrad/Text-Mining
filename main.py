import os
import pandas as pd
from sys import argv
from scipy import spatial
from tools import *
from numpy import isnan
from io import open


def main():
    """this is the run file"""
    test_folders = argv[1]
    benchmark_file = argv[2]
    output_path = argv[3]

    method = ['n', 'a', 'a']
    bigram = ['False', 'False', 'True']
    output_file = output_path + '/' + 'method_comparison_cosine_values.csv'

    with open(test_folders, 'r') as f:
        test_folders = f.read()

    test_folders = test_folders.splitlines()

    with open(benchmark_file, 'r') as f:
        benchmark_file = f.read()

    benchmark_file = benchmark_file.splitlines()

    # initialize big data frame
    frames = []

    for k in xrange(len(benchmark_file)):

        test = str(test_folders[k]).replace('"', '')
        print "Reading test files from folder:"
        print test

        benchmark = str(benchmark_file[k]).replace('"', '')
        print "Reading benchmark form file:"
        print benchmark

        # read file paths from test documents folder
        query = sorted([os.path.join(test, f) for f in os.listdir(test) if f.endswith('.txt')])

        # load benchmark text file
        with open(benchmark, "r", encoding="utf-8", errors='ignore') as doc:
            raw = doc.read()

        # initialize dict of dicts for data frame
        method_csv = {}

        for j in xrange(len(method)):
            # extract features from benchmark
            dtm = ExtractFeatures(method[j], bigram[j])
            benchmark_name = benchmark_file[k].split('\\')[-1]
            benchmark_features = dtm.extract_features_from_text(raw, benchmark_name)

            # extract terms from each text document to create a vocabulary (keeping unique terms only)
            vocabulary = sorted(set(w[1] for w in benchmark_features))
            print "{0} features produced.".format(str(len(vocabulary)))

            benchmark_dtv = DTM(vocabulary, benchmark_name, benchmark_features)
            benchmark_dtv = benchmark_dtv.compute_dtv()

            # load test document features
            test_features = []
            for q in query:
                dtm1 = ExtractFeatures(method[j], bigram[j])
                test_features = test_features + dtm1.extract_features_from_file(q)

            documents = sorted(set([d for d, w in test_features]))
            print "{0} test documents read.".format(str(len(documents)))

            print "Computing DTM..."
            test_dtm = DTM(vocabulary, documents, test_features)
            test_dtm = test_dtm.compute_dtm()

            print "Computing cosine values..."
            dv = {}
            for i in xrange(len(documents)):
                d = 1 - spatial.distance.cosine(benchmark_dtv[benchmark_name], test_dtm[documents[i]])
                if isnan(d):
                    d = 0
                dv[documents[i]] = d

            this_method = "method=" + method[j] + '_' + "bigram=" + bigram[j]
            method_csv[this_method] = pd.Series(dv)

        print "Saving to data frame..."
        df = pd.DataFrame(method_csv)
        test = test.split('\\')[-1]
        test = test.split('.')[0]
        df['test_group'] = test

        frames.append(df)

    result = pd.concat(frames)

    print "Saving results to file: ", output_file
    result.to_csv(output_file)

    print 'Finished computing {0} data frames'.format(str(len(test_folders)))

if __name__ == '__main__':
    main()
