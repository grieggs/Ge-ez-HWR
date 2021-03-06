import numpy as np
from torch.nn.modules.loss import CTCLoss
import torch




def str2label(value, characterToIndex={}, unknown_index=None):
    if unknown_index is None:
        unknown_index = len(characterToIndex)

    label = []
    for v in value:
        # print(v)
        if v not in characterToIndex:
            continue
        label.append(characterToIndex[v])
    return np.array(label, np.uint32)

def label2input(value, num_of_inputs, char_break_interval):
    idx1 = len(value) * (char_break_interval + 1) + char_break_interval
    idx2 = num_of_inputs + 1
    print(idx1)
    print(idx2)
    input_data = [[0 for i in range(idx2)] for j in range(idx1)]

    cnt = 0
    for i in range(char_break_interval):
        input_data[cnt][idx2-1] = 1
        cnt += 1

    for i in range(len(value)):
        if value[i] == 0:
            input_data[cnt][idx2-1] = 1
        else:
            input_data[cnt][value[i]-1] = 1
        cnt += 1

        for i in range(char_break_interval):
            input_data[cnt][idx2-1] = 1
            cnt += 1

    return np.array(input_data)

def label2str(label, indexToCharacter, asRaw, spaceChar = "~"):
    string = u""
    for i in range(len(label)):
        if label[i] == 0:
            if asRaw:
                string += spaceChar
            else:
                break
        else:
            val = label[i]
            string += indexToCharacter[val]
    return string

def naive_decode(output):
    rawPredData = np.argmax(output, axis=1)
    predData = []
    for i in range(len(output)):
        if rawPredData[i] != 0 and not ( i > 0 and rawPredData[i] == rawPredData[i-1] ):
            predData.append(rawPredData[i])
    return predData, list(rawPredData)

def lexicon_decode(output,  naive, raw_naive, lexicon, k=10, char_to_idx = None):
    out= ""
    criterion = CTCLoss(reduction='none')
    word_splits = np.argwhere(np.array(raw_naive)==1)
    words = naive.split(" ")
    index = 0
    prevIndex = -1
    for word in words:
        predlength = 0
        while predlength < len(word):
            if prevIndex == -1:
                pred = output[:word_splits[index,0]]
                predlength = pred.shape[0]
                prevIndex = index
                index = index+1
            else:
                pred = output[word_splits[prevIndex,0]:word_splits[index, 0]]
                predlength = pred.shape[0]
                prevIndex = index
                index = index + 1
        options = lexicon.query_k(word, k=k)
        gt_labels = []
        label_lengths = []

        for option in options:
            gt_labels.append(str2label(option, char_to_idx))
            label_lengths.append(len(option))
        preds = pred.repeat((1, len(label_lengths),1))
        gt_labels = torch.IntTensor(np.concatenate(gt_labels).astype(np.int32))
        label_lengths = torch.IntTensor(np.array(label_lengths).astype(np.int32))
        preds_size = torch.IntTensor([preds.size(0)] * preds.size(1))
        loss = criterion(preds, gt_labels, preds_size, label_lengths)
        print(word)
        print(options[torch.argmax(loss)])
        print(loss[torch.argmax(loss)])
        print("---------------------------------")
        out = out + options[torch.argmax(loss)] + " "

    return out

import re
from collections import Counter


