# import os
from io import open
from sys import argv

import pandas as pd
from numpy import isnan
from scipy import spatial

from tools import *


def main():
    """this is the run file"""
    transcript_files = argv[1]
    benchmark_files = argv[2]
    output_path = argv[3]

    method = 'a'
    bigram = 'False'
    output_file = output_path + '/' + 'transcripts_cosine_values.csv'

    # load file which points to transcript files
    with open(transcript_files, 'r', encoding="utf-8", errors='ignore') as f:
        transcript_files = f.read()
    transcript_files = transcript_files.splitlines()

    with open(benchmark_files, 'r', encoding="utf-8", errors='ignore') as f:
        benchmark_files = f.read()
    benchmark_files = benchmark_files.splitlines()

    # load k transcript and benchmark files
    frames = []

    for k in range(len(transcript_files)):
        benchmark_file = str(benchmark_files[k]).replace('"', '')
        print benchmark_file
        with open(benchmark_file, 'r', encoding="utf-8", errors='ignore') as f:
            benchmark = f.read()

        transcript_file = str(transcript_files[k]).replace('"', '')
        print "Reading text from file: ", transcript_file
        group = transcript_file.split("\\")
        group = group[-1].split(".")[0]

        with open(transcript_file, 'r', encoding="utf-8", errors='ignore') as f:
            transcript = f.read()

        transcript = transcript.splitlines()

        # load expert vocabulary and features
        bench_features = ExtractFeatures(method, bigram)
        bench_features = bench_features.extract_features_from_text(benchmark, 'benchmark')
        vocabulary = sorted(set(w[1] for w in bench_features))

        # iterate over each line
        dict_dv = {}
        dict_n = {}
        dict_g = {}
        i = 1

        for line in transcript:
            # print line
            text = nltk.word_tokenize(line)
            time, name, line = [text[1], text[3], text[4:]]
            assert time[0] == "0" and time[2] == ":",\
                "Time slot not a time before: " + text[0] + ' ' + text[1] + ' ' + group
            # print time[2] + name + group
            line = ' '.join(line)
            line_features = ExtractFeatures(method, bigram)
            line_features = line_features.extract_features_from_text(line, name)
            features = line_features + bench_features

            dtm = DTM(vocabulary, [name, 'benchmark'], features)
            dtm = dtm.compute_dtm()

            print "Computing cosine values for line", i, "of", len(transcript), "in transcript", k, "of", len(transcript_files)
            if not sum(dtm[name]) == 0:
                d = 1 - spatial.distance.cosine(dtm[name], dtm['benchmark'])
            else:
                d = 0
            if isnan(d):
                d = 0
            dict_dv[time] = d
            dict_n[time] = name
            dict_g[time] = group
            i += 1

        df = {'dv': pd.Series(dict_dv), 'ID': pd.Series(dict_n), 'Group': pd.Series(dict_g)}
        df = pd.DataFrame(df)

        frames.append(df)

    result = pd.concat(frames)
    print result

    print "Saving results to file: ", output_file
    result.to_csv(output_file)

    print 'Finished computing {0} data frames'.format(str(len(transcript_files)))


if __name__ == '__main__':
    main()
