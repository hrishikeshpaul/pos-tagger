from pos_scorer import Score
from pos_solver import *
import sys
import json

# Read in training or test data file
#
def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        exemplars += [ (data[0::2], data[1::2]), ]
    return exemplars


def main(sentence):
    train_file = 'bc.train'
    # test_file = 'bc.test'
    test_data = sentence['sentence'].split()

    print("Learning model...")
    solver = Solver()
    train_data = read_data(train_file)
    solver.train(train_data)

    print("Loading test data...")
    # test_data = ('poet', 'twisted', 'again', 'and', "nick's", 'knuckles', 'scraped', 'on', 'the', 'air', 'tank', ',', 'ripping', 'off', 'the', 'skin', '.')
    # test_data = read_data(test_file)
    scorer = Score()

    Algorithms = ("Simple", "HMM", "Complex")
    outputs = {}

    for algo in Algorithms:
        outputs[algo] = solver.solve( algo, test_data)

    posteriors = { o: { a: solver.posterior( a, test_data, outputs[o] ) for a in Algorithms } for o in outputs }
    return (Score.print_results(test_data, outputs, posteriors, Algorithms))
