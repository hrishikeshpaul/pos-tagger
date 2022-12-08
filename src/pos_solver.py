#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: Ishita Kumar (ishkumar@iu.edu), Hrishikesh Paul (hrpaul@iu.edu), Rushabh Shah (shah12@iu.edu)
#
# based on skeleton code by D. Crandall, 11/2019
#
# Part 1- POS Tagging
#

import numpy as np
from collections import Counter
from src.files import dumpPkl, readPkl


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.


class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!

    def posterior(self, model, sentence, label):
        """

        :param model:       Stores the type of model: Simple, complex, mcmc
        :param sentence:    Stores each senetence in the dataset
        :param label:       Stores the Part of Speech related to every Word in
                            Sentence
        :return:            Returns the posterior Probability of each model

        """
        if model == "Simple":
            cost = 0
            for i in range(len(sentence)):
                if sentence[i] in self.emission[label[i]]:
                    cost += (self.emission[label[i]][sentence[i]]) + (
                        self.part_of_speech_prob[label[i]]
                    )
                else:
                    cost += np.log(1 / float(10**10)) + (
                        self.part_of_speech_prob[label[i]]
                    )
            return cost
        elif model == "Complex":
            # code inspired by https://github.com/mjaglan/AI-Foundations/blob/master/5%20Part%20of%20Speech%20(NB%2C%20Viterbi%2C%20MCMC)/pos_solver.py
            #    and https://github.com/Chitz/Part-of-Speech-Tagger/ starts here
            posterior = []
            for i in range(len(sentence)):
                if i == 0:

                    posterior.append(
                        self.emission[label[i]][sentence[i]] + self.initial[label[i]]
                        if sentence[i] in self.emission[label[i]]
                        else (1 / float(10**10)) + self.initial[label[i]]
                    )

                else:

                    posterior.append(
                        self.emission[label[i]][sentence[i]]
                        + (
                            (
                                np.log(self.transition[label[i - 1]][label[i]])
                                + self.part_of_speech_prob[label[i - 1]]
                            )
                            / self.part_of_speech_prob[label[i]]
                        )
                        + (
                            np.log(self.transition[label[i - 1]][label[i]])
                            + self.part_of_speech_prob[label[i - 2]]
                            / self.part_of_speech_prob[label[i]]
                        )
                        + self.part_of_speech_prob[label[i]]
                        if sentence[i] in self.emission[label[i]]
                        else (1 / float(10**10))
                        + (
                            np.log(self.transition[label[i - 1]][label[i]])
                            + self.part_of_speech_prob[label[i - 1]]
                            / self.part_of_speech_prob[label[i]]
                        )
                        + (
                            np.log(self.transition[label[i - 2]][label[i]])
                            + self.part_of_speech_prob[label[i - 2]]
                            / self.part_of_speech_prob[label[i]]
                        )
                        + self.part_of_speech_prob[label[i]]
                    )

            for p in posterior:
                posterior = np.log(p)

            cost = np.sum(posterior)
            return cost
        # code inspired by https://github.com/mjaglan/AI-Foundations/blob/master/5%20Part%20of%20Speech%20(NB%2C%20Viterbi%2C%20MCMC)/pos_solver.py
        #    and https://github.com/Chitz/Part-of-Speech-Tagger/ starts here
        if model == "HMM":
            posterior = []
            for i in range(len(sentence)):
                if i == 0:
                    if sentence[i] in self.emission[label[i]]:
                        posterior.append(
                            (
                                ((self.initial[label[i]]))
                                + ((self.emission[label[i]][sentence[i]]))
                            )
                        )
                    else:
                        posterior.append(
                            ((self.initial[label[i]])) + np.log((1 / float(10**10)))
                        )
                else:
                    if sentence[i] in self.emission[label[i]]:
                        posterior.append(
                            self.emission[label[i]][sentence[i]]
                            + posterior[i - 1]
                            + np.log(self.transition[label[i - 1]][label[i]])
                        )
                    else:
                        posterior.append(
                            np.log((1 / float(10**10)))
                            + posterior[i - 1]
                            + np.log(self.transition[label[i - 1]][label[i]])
                        )
            cost = np.sum(posterior)
            return cost
        else:
            print("Unknown algo!")

    # Do the training!
    def train(self, data, env = 'production'):
        """
        :param data:    Stores the words and its related part of speech

        """

        if env == 'production':
            self.emission = readPkl('emission_prob')
            self.initial = readPkl('initial')
            self.speech = readPkl('speech')
            self.transition = readPkl('transition')
            self.part_of_speech_prob = readPkl('part_of_speech_prob')
            return

        print("Learning model...")

        speech = [
            "adj",
            "adv",
            "adp",
            "conj",
            "det",
            "noun",
            "num",
            "pron",
            "prt",
            "verb",
            "x",
            ".",
        ]
        train_data = []

        for i in range(len(data)):
            train_data.append(data[i][1])

        train_data = np.concatenate(train_data)
        #  Calculating the number of times each Part of speech occurs in Dataset
        part_of_speech_count = np.array(np.unique(train_data, return_counts=True)).T
        sum = 0
        for i in part_of_speech_count:
            sum += int(i[1])

        # Calculating the initial probability for each part of speech
        initial_prob_part_of_speech = {}
        for i in part_of_speech_count:
            initial_prob_part_of_speech[i[0]] = np.log(int(i[1]) / sum)

        word_speech = []
        for i in data:
            for j in range(len(i[0])):
                word_speech.append(tuple([i[0][j], i[1][j]]))
        # tuple with word, part of speech and occurences pair
        word_count = Counter(word_speech)

        """Calculatingthe Posterior Probability"""
        part_of_speech_dict = {part_of_speech: {} for part_of_speech in speech}

        for w in word_count:
            part_of_speech_dict[w[1]].update({w[0]: word_count[w]})

        part_of_speech_count_dict = {}
        wordpos_list = ()
        for line in data:
            for i in range(len(line[0])):
                wordpos_list = tuple([line[0][i], line[1][i]])

        part_of_speech_prob = {}
        for part_of_speech in part_of_speech_dict.keys():
            tt = list(part_of_speech_dict[part_of_speech].values())
            tt_sum = 0
            for i in tt:
                tt_sum += i
            part_of_speech_prob[part_of_speech] = np.log(
                float(tt_sum / len(wordpos_list))
            )

        for i in part_of_speech_count:
            part_of_speech_count_dict[i[0]] = int(i[1])
        emission_prob = {}
        for i in speech:
            emission_prob[i] = {}
        for i in word_count:
            emission_prob[i[1]].update(
                {i[0]: np.log(word_count[i] / part_of_speech_count_dict[i[1]])}
            )

        tcounter = {}
        transition_probability = {}
        # Calculating the Transition Probability
        for part_of_speech in speech:
            tcounter[part_of_speech] = {}
        for part_of_speech in speech:
            transition_probability[part_of_speech] = {}
        part_of_speech_transition = []
        for line in data:
            for i in range(len(line[1]) - 1):
                part_of_speech_transition.append(tuple([line[1][i], line[1][i + 1]]))
        unique_part_of_speech_transition = []
        unique_part_of_speech_transition = list(set(part_of_speech_transition))

        for element in unique_part_of_speech_transition:
            tcounter[element[0]].update(
                {element[1]: part_of_speech_transition.count(element)}
            )

        for part_of_speech in speech:
            transition_probability[part_of_speech] = {
                part_of_speech: (1 / float(10**10)) for part_of_speech in speech
            }
            for key, v in tcounter[part_of_speech].items():
                tt = list(tcounter[part_of_speech].values())
                tt_sum = 0
                for i in tt:
                    tt_sum += i
                transition_probability[part_of_speech][key] = v / tt_sum

        self.emission = emission_prob
        self.initial = initial_prob_part_of_speech
        self.speech = speech
        self.transition = transition_probability
        self.part_of_speech_prob = part_of_speech_prob

        dumpPkl('emission_prob', emission_prob)
        dumpPkl('initial', initial_prob_part_of_speech)
        dumpPkl('speech', speech)
        dumpPkl('transition', transition_probability)
        dumpPkl('part_of_speech_prob', part_of_speech_prob)


    def simplified(self, sentence):
        """
        :param sentence:    Stores each senetence in the dataset
        :return:            Returns the sequence of Part of Speech

        """
        sequence = []
        for i in range(len(sentence)):
            prob = []
            for j in self.speech:
                if sentence[i] in self.emission[j]:
                    prob.append(self.initial[j] + self.emission[j][sentence[i]])
                else:
                    prob.append(self.initial[j] + np.log(0.000000001))
            word_index = np.argmax(prob)
            sequence.append(self.speech[word_index])
        return sequence

    #    code inspired by https://github.com/mjaglan/AI-Foundations/blob/master/5%20Part%20of%20Speech%20(NB%2C%20Viterbi%2C%20MCMC)/pos_solver.py
    #    and https://github.com/Chitz/Part-of-Speech-Tagger/ starts here
    def complex_mcmc(self, sentence):
        """
        :param sentence:    Stores each senetence in the dataset
        :return:            Returns the sequence of Part of Speech

        """
        prob = {}
        part_of_speech_mcmc_dict = {
            "PartofSpeech_" + str(i): {} for i in range(len(sentence))
        }

        sequence = ["noun"] * len(sentence)
        for i in range(len(sentence)):

            if i == 0:
                if sentence[i] not in prob.keys():
                    prob[sentence[i]] = {
                        pos: np.exp(self.emission[pos][sentence[i]])
                        * np.exp(self.initial[pos])
                        if sentence[i] in self.emission[pos]
                        else (1 / float(10**10)) * np.exp(self.initial[pos])
                        for pos in self.speech
                    }

                prob_first = prob[sentence[i]]
                initial_gibbs = list(
                    np.random.choice(
                        [keys for keys in prob_first.keys()],
                        5500,
                        p=[
                            float(prob_first[keys]) / sum(prob_first.values())
                            for keys in prob_first.keys()
                        ],
                    )
                )
                initial_gibbs = initial_gibbs[3500:]
                part_of_speech_mcmc_dict["PartofSpeech_" + str(i)] = {
                    pos: (float(initial_gibbs.count(pos)) / len(initial_gibbs))
                    for pos in self.speech
                }
                sequence[i] = max(
                    part_of_speech_mcmc_dict["PartofSpeech_" + str(i)],
                    key=part_of_speech_mcmc_dict["PartofSpeech_" + str(i)].get,
                )
            else:

                if sentence[i] not in prob.keys():
                    prob[sentence[i]] = {
                        pos: np.exp(self.emission[pos][sentence[i]])
                        * (
                            float(
                                (self.transition[sequence[i - 1]][pos])
                                * np.exp(self.part_of_speech_prob[sequence[i - 1]])
                            )
                            / np.exp(self.part_of_speech_prob[pos])
                        )
                        * (
                            float(
                                (self.transition[sequence[i - 2]][pos])
                                * np.exp(self.part_of_speech_prob[sequence[i - 2]])
                            )
                            / np.exp(self.part_of_speech_prob[pos])
                        )
                        * np.exp(self.part_of_speech_prob[pos])
                        if sentence[i] in self.emission[pos]
                        else (1 / float(10**10))
                        * (
                            float(
                                (self.transition[sequence[i - 1]][pos])
                                * np.exp(self.part_of_speech_prob[sequence[i - 1]])
                            )
                            / np.exp(self.part_of_speech_prob[pos])
                        )
                        * (
                            float(
                                (self.transition[sequence[i - 2]][pos])
                                * np.exp(self.part_of_speech_prob[sequence[i - 2]])
                            )
                            / np.exp(self.part_of_speech_prob[pos])
                        )
                        * np.exp(self.part_of_speech_prob[pos])
                        for pos in self.speech
                    }
                prob_other = prob[sentence[i]]
                rest_of_gibbs = list(
                    np.random.choice(
                        [keys for keys in prob_other.keys()],
                        5500,
                        p=[
                            float(prob_other[keys]) / sum(prob_other.values())
                            for keys in prob_other.keys()
                        ],
                    )
                )
                rest_of_gibbs = rest_of_gibbs[3500:]
                part_of_speech_mcmc_dict["PartofSpeech_" + str(i)] = {
                    pos: (float(rest_of_gibbs.count(pos)) / len(rest_of_gibbs))
                    for pos in self.speech
                }
                sequence[i] = max(
                    part_of_speech_mcmc_dict["PartofSpeech_" + str(i)],
                    key=part_of_speech_mcmc_dict["PartofSpeech_" + str(i)].get,
                )

        return sequence

    #    code inspired by https://github.com/mjaglan/AI-Foundations/blob/master/5%20Part%20of%20Speech%20(NB%2C%20Viterbi%2C%20MCMC)/pos_solver.py
    #    and https://github.com/Chitz/Part-of-Speech-Tagger/ ends here

    def hmm_viterbi(self, sentence):
        part_of_speech = []
        p = 0
        maxstate = ""
        for i in range(len(sentence)):
            prior = []
            if i == 0:
                for j in self.speech:
                    if sentence[i] in self.emission[j]:
                        prior.append(self.initial[j] + self.emission[j][sentence[i]])

                    else:
                        prior.append(self.initial[j] + np.log(1 / 10**10))

                part_of_speech.append({
                    "word": sentence[i],
                    "tag": self.speech[np.argmax(prior)],
                    "prob": 100 + np.max(prior)
                })
                p = max(prior)
                maxstate = self.speech[np.argmax(prior)]
            else:

                for k in range(len(self.speech)):

                    if sentence[i] in self.emission[self.speech[k]]:
                        trans = np.log(self.transition[maxstate][self.speech[k]])
                        emission = self.emission[self.speech[k]][sentence[i]]
                        prior.append(p + emission + trans)
                    else:
                        prior.append(
                            p
                            + np.log(1 / 10**10)
                            + np.log(self.transition[maxstate][self.speech[k]])
                        )
                maxstate = self.speech[np.argmax(prior)]
                p = np.max(prior)


                # part_of_speech.append(self.speech[np.argmax(prior)])
                part_of_speech.append({
                    "word": sentence[i],
                    "tag": self.speech[np.argmax(prior)],
                    "prob": 100 + np.max(prior)
                })

        return part_of_speech

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        """
        :param sentence:    Stores each senetence in the dataset
        :param model:       Stores the type of model - simplified, viterbi or mcmc
        :return:            Returns the sequence of Part of Speech

        """
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")
