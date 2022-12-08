import pickle


def dumpPkl(filename, data):
    with open(f'models/{filename}.pkl', 'wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
        print(f'{filename}.pkl data saved')

def readPkl(filename):
    with open(f'models/{filename}.pkl', 'rb') as inp:
        data = pickle.load(inp)
    return data