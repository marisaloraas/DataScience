# Author: Marisa Loraas
# 2/14/2021
# CSE489 Data Science
# HW 2
import sys


def print_output(k, my_bigram, f, s):
    if k > len(my_bigram):
        max_len = len(my_bigram) - 1
    else:
        max_len = k
    fi = open('marisa-result.csv', 'w')
    print("word1, word2, frequency, score", file = fi)
    new_bigram = sort_bigram(my_bigram, f)
    for pairs in range(0, max_len):
        check = ', '.join(list(new_bigram)[pairs])
        print(new_bigram[pairs][0] + ", " + new_bigram[pairs][1] + ", " + str(f[check]) + ", " + str(s[check]), file = fi)
    fi.close()


def sort_bigram(my_bigram, f):
    my_set = set(item for item in f)
    mysorted = sorted(my_set, key=lambda i: (-f[i], i))
    new_bigram = list()
    for item in mysorted:
        replaced = item.replace(',', '')
        new_bigram.append(replaced.split())
    return new_bigram


def sentiment_score(my_bigram):
    scores = dict()
    with open('part-AFINN-only-words.txt', "r") as f:
        x = [line[:-1].split('\t') for line in f]
        afinn = dict(map(lambda k: (k[0], int(k[1])), x))
    for pairs in list(my_bigram):
        count = 0
        if pairs[0] in afinn:
            count += afinn[pairs[0]]
        if pairs[1] in afinn:
            count += afinn[pairs[1]]
        if (pairs[0] == 'not') or (pairs[0] == 'no'):
            count = 0 - afinn[pairs[1]]
        newpairs = ', '.join(pairs)
        if newpairs in scores.keys():
            continue
        else:
            scores[newpairs] = count
    return scores


def num_occur(my_list):
    my_dict = dict()
    bigram = list()
    for i in range(0, len(my_list) - 1):
        bilist = [my_list[i], my_list[i + 1]]
        bigram.append(bilist)
    # print(bigram)
    for i in list(bigram):
        if i[0][len(i[0]) - 1] == ('.' or '!' or '?'):
            bigram.remove(i)
            continue
        if i[1][len(i[1]) - 1] == ('.' or '!' or '?'):
            i[1] = i[1].removesuffix('.')
        my_string = ', '.join(i)
        if my_string in my_dict.keys():
            my_dict[my_string] += 1
        else:
            my_dict[my_string] = 1
    return my_dict, bigram


def remove_stop_words(my_list):
    try:
        infile = open("stop-words.txt")
    except FileNotFoundError as no_file:
        print("Error: stop-words.txt not found", no_file)
    else:
        file = infile.read().splitlines()

        for i in list(my_list):
            if i in file:
                my_list.remove(i)
            elif i.isdigit():
                my_list.remove(i)
    return my_list


def make_words(file):
    final_list = []
    for line in file:
        lower_case = line.lower()
        words = lower_case.split()
        for i in words:
            new_i = i.strip(',;:')
            final_list.append(new_i.strip())
    final_list = remove_stop_words(final_list)
    return final_list


def main():
    try:
        infile = open(sys.argv[1], "r")
    except FileNotFoundError as no_file:
        print('Error: File not found', no_file)
    else:
        file = infile.readlines()
        wordlist = make_words(file)
        # print(wordlist)
        word_occur, bigram = num_occur(wordlist)
        #print(word_occur)
        #print(bigram)
        sentiment = sentiment_score(bigram)
        #print(sentiment)
        print_output(20, bigram, word_occur, sentiment)

if __name__ == '__main__':
    main()
