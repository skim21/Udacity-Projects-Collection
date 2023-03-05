import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)



    probabilities = []
    guesses = []

    for i in range(len(test_set.df)):
        current_sequences, current_length = test_set.get_item_Xlengths(i)

        word_log_likelyhood = {}
        for word,model in models.items():
            try:
                word_log_likelyhood[word] = model.score(current_sequences,current_length)
            except:
                word_log_likelyhood[word] = float('-inf')
                continue
        probabilities.append(word_log_likelyhood)
        guesses.append(max(word_log_likelyhood.items(), key=lambda x:x[1])[0])

    return probabilities, guesses