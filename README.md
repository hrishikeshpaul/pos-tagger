# Part Of Speech Tagging

The underlying theme for the problem statement defined requires us to correctly return the part of speech for a given dataset. Every word in the dataset’s sentences must be correctly returned with its corresponding part of speech. For the purpose of classification. Our parts of speech in a global term have the following components : 'adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.'.

> A front-end application that makes use of the 'Complex' model
can be found [here](https://github.com/hrishikeshpaul/post)

## Probabilities
 In order to find the emission, transition and inital probabilities we define the values using a part_of_speech list.
 Initial Probability: By definition it is the ratio of the Number of times part of speech appears in the 1st positon to the Total number of sentences.
 Emission_Probability: By definition it is the probability of a word related to a particular part of speech to the probability of the appearance of the art of speech in the whole sentence.
 Transition Probability: By definition it is the ratio of the probability of one part of speech coming succeeding another part of speech to the probability of the occurrence of that part of speech.

## Simplified Bayes Net
The simplified Bayes net in a broader term can be calculated by
We multiple the initial probability of each part of speech occurring in the dataset and the emission probability of the part of speech. We take the max value argmax() of each part of speech and add that into the sentences individual part of speech list.

## Viterbi Algorithm
The tuple contains the transition probability of going from one pos to another. it contains the product of the initial and emission probability for the part of speech.
 Since we don't have the transition probabilities of the first word, we consider its emission and initial probabilities only. We take the max of these values.
For all the other words we consider the initial, transition and emission probability
of going from one part of speech to another. Thus, for the entire list of pos, we consider all its variations. At the end we return the key of the max probability value. We can then backtrack and take the path with the maximum probability from the last word to the first.

## Complex MCMC

In this we generate posterior samples by gibbs sampling , a statistical inference technique.
If its the first word of the sentence, we consider its emission and initial probabilities and for all the other words, we consider its emission,initial and transition probabilities from the previous word to the current word. If there exists a word not already present in the word_dictonary we assign it a very small value of 0.000000001.
We sample our code for 5500 iterations with a burnin period of 3500 samples.


### Challenges and Assumptions

  Everything is changed to lower case to make the comparisons case insensitive.
  One if the biggest challenges occurring in POS Tagging is when an unknown word
  is found in the dataset. In order to measure the transition probabilities of
  the unknown words we assign it a very small value of 10^-8

### Results


|   | Words   |   Sentences |   
|---|---|---|
| Simple  | 93.95%  |  47.62%  |
| HMM  | 93.61%  | 47.37%  |
| Complex  | 93.13%  | 44.52%  |
