'''
Evan Hansen
CS 540
P4: Math and AI
'''

import os
import numpy as np


def create_vocabulary(training_directory, cutoff):
    v_dict = {}
    for dir, subdir, filelist in os.walk(training_directory):
        for file in filelist:
            f = open(os.path.join(dir, file), 'r', encoding='utf-8')
            for word in f:
                word = word.rstrip('\n')
                if word in v_dict:
                    v_dict[word] += 1
                else:
                    v_dict[word] = 1

    # Culls vocab list based on cutoff value
    v_dict = {k: v for k, v in v_dict.items() if v >= cutoff}

    return sorted(v_dict.keys())


def create_bow(vocab, filepath):
    bow = {}
    oov = 0
    f = open(filepath, 'r', encoding='utf-8')
    for word in f:
        word = word.rstrip('\n')

        # Existing word in bow
        if word in vocab and word in bow:
            bow[word] += 1

        # New word in bow
        elif word in vocab:
            bow[word] = 1

        # OOV word
        else:
            oov += 1

    # Add OOV to None Key
    if oov > 0:
        bow[None] = oov

    return bow


def load_training_data(vocab, directory):
    data = []
    for dir, subdir, filelist in os.walk(directory):
        for file in filelist:
            filepath = os.path.join(dir, file)
            label = os.path.basename(dir)
            bow = create_bow(vocab, filepath)

            data.append({'label': label, 'bow': bow})

    return data


def prior(training_data, label_list):
    ret_dict = {}
    for l in label_list:
        count = 0
        for e in training_data:
            if e['label'] == l:
                count += 1
        ret_dict[l] = count

    total = sum(ret_dict.values())
    ret_dict = {k: np.log(v / total) for k, v in ret_dict.items()}

    return ret_dict


def p_word_given_label(vocab, training_data, label):
    ret_dict = {k: 0 for k in vocab}
    ret_dict[None] = 0

    for bow in training_data:
        if bow['label'] != label:
            continue

        for k, v in bow['bow'].items():
            ret_dict[k] += v

    vocab_sum = len(ret_dict.keys())
    word_sum = sum(ret_dict.values())
    denom = vocab_sum + word_sum
    ret_dict = {k: np.log((v + 1) / denom) for k, v in ret_dict.items()}

    return ret_dict


def train(training_directory, cutoff):
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    log_prior = prior(training_data, ['2016', '2020'])
    log_word_2016 = p_word_given_label(vocab, training_data, '2016')
    log_word_2020 = p_word_given_label(vocab, training_data, '2020')

    d = {'vocabulary': vocab,
         'log prior': log_prior,
         'log p(w|y=2016)': log_word_2016,
         'log p(w|y=2020)': log_word_2020}
    return d


def classify(model, filepath):
    bow = create_bow(model['vocabulary'], filepath)

    p_2016 = model['log prior']['2016']
    p_2020 = model['log prior']['2020']

    # Sum log probabilities for each word in bow
    for word in bow:
        p_2016 += model['log p(w|y=2016)'][word]
        p_2020 += model['log p(w|y=2020)'][word]

    pred_y = '2016' if p_2016 > p_2020 else '2020'

    d = {'predicted y': pred_y,
         'log p(y=2016|x)': p_2016,
         'log p(y=2020|x)': p_2020}

    return d


# For Testing
#
# m = train('corpus/training',1)
#
# correct_2016 = 0
# total_2016 = 0
# for dir, subdir, filelist in os.walk('corpus/test/2016'):
#     for file in filelist:
#         total_2016 += 1
#         filepath = os.path.join(dir, file)
#         out = classify(m, filepath)
#         if out['predicted y'] == '2016':
#             correct_2016 += 1
#
# correct_2020 = 0
# total_2020 = 0
# for dir, subdir, filelist in os.walk('corpus/test/2020'):
#     for file in filelist:
#         total_2020 += 1
#         filepath = os.path.join(dir, file)
#         out = classify(m, filepath)
#         if out['predicted y'] == '2020':
#             correct_2020 += 1
#
# print('2016:',correct_2016/total_2016)
# print('2020:',correct_2020/total_2020)
