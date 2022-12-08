from src.pos_scorer import Score
from src.pos_solver import *
import os

# Read in training or test data file
#
def read_data(fname):
    exemplars = []
    file = open(fname, "r")
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        exemplars += [
            (data[0::2], data[1::2]),
        ]
    return exemplars


def main(sentence):
    env = os.environ.get("ENV")
    solver = Solver()

    # test_file = 'bc.test'
    test_data = sentence.get("sentence", "").split()

    train_file = "data/bc.train"
    train_data = read_data(train_file)
    solver.train(train_data, env)
        

    print("Loading test data...")
    # test_data = ('poet', 'twisted', 'again', 'and', "nick's", 'knuckles', 'scraped', 'on', 'the', 'air', 'tank', ',', 'ripping', 'off', 'the', 'skin', '.')
    # test_data = read_data(test_file)

    output = solver.solve("HMM", test_data)

    print(output)

    # TODO: Work on showing the probability on the FE
    # scorer = Score()
    # posteriors = solver.posterior("HMM", test_data, [i["tag"] for i in output] )
    # return (Score.print_results(test_data, outputs, posteriors, Algorithms))

    # print(posteriors)

    return output
