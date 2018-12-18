# importing libraries

import os
import sys
import random
import subprocess as sub
from decimal import Decimal

# current working path

path = '/media/sourav/Tree/libraries/a4/EVALB/'

# files to work with

berkeley_file = path + 'Berkeley.overall.parse'
stanford_file = path + 'Stanford.overall.parse'
gold_file = path + 'Overall.gold'

# function to create list of sentences from
# the test files

def create_list_from_file(file_path):
    result_list = []
    with open(file_path, 'r') as input_file:
        for line in input_file:
            result_list.append(line)
    return result_list

# function to randomly flip the data between sources based on 
# threshold probability

def flip_data_randomly(berkeley_list, stanford_list, prob):
    with open('berkeley_out', 'w') as berk, open('stanford_out', 'w') as stan:
        for i in range(length):
            berkeley_sent, stanford_sent = berkeley_list[i], stanford_list[i]
            if random.random() < prob:
                berk.write(stanford_sent)
                stan.write(berkeley_sent)
            else:
                berk.write(berkeley_sent)
                stan.write(stanford_sent)

# function that returns the f-score from the EVALB calculation

def return_fscore(line):
    return float(str(line)[31:36].strip('\\'))

# function that appends the results of f-score differences
# to a single file for comparison

def append_results(file_name, berkeley_fscore_difference, stanford_fscore_difference):
    with open(file_name, 'a') as results_file:
        results_file.write(str(berkeley_fscore_difference) + '\t' + str(stanford_fscore_difference) + '\n')

# golden standard parse tree data file

gold = create_list_from_file(gold_file)
length = len(gold)

# loading the unlabeled results

line = sub.check_output(['tail', '-20', 'Result.Berkeley.overall.Unlabeled'])
fscore_gold_berkeley_unlabeled = float(str(line)[31:36].strip('\\'))
line = sub.check_output(['tail', '-20', 'Result.Stanford.overall.Unlabeled'])
fscore_gold_stanford_unlabeled = float(str(line)[31:36].strip('\\'))

# loading the labeled results

line = sub.check_output(['tail', '-20', 'Result.Berkeley.overall'])
fscore_gold_berkeley_labeled = float(str(line)[31:36].strip('\\'))
line = sub.check_output(['tail', '-20', 'Result.Stanford.overall'])
fscore_gold_stanford_labeled = float(str(line)[31:36].strip('\\'))

# Number of iterations for the approximate randomization significance test
NUMBER_OF_TURNS = 1000

# Threshold probability to flip data
# (Change this to 0.05 and 0.01 as needed)
PROBABILITY = 0.5

# constants for significance test file names

SIG_TEST_RESULTS_UNLABELED_PROB0_5 = 'sig_test_results_unlabeled_prob0_5'
SIG_TEST_RESULTS_UNLABELED_PROB0_05 = 'sig_test_results_unlabeled_prob0_05'
SIG_TEST_RESULTS_UNLABELED_PROB0_01 = 'sig_test_results_unlabeled_prob0_01'

SIG_TEST_RESULTS_LABELED_PROB0_5 = 'sig_test_results_labeled_prob0_5'
SIG_TEST_RESULTS_LABELED_PROB0_05 = 'sig_test_results_labeled_prob0_05'
SIG_TEST_RESULTS_LABELED_PROB0_01 = 'sig_test_results_labeled_prob0_01'

# this is the loop of iterations which run the approximate randomization
# process

for j in range(NUMBER_OF_TURNS):

    # list of data created

    berkeley = create_list_from_file(berkeley_file)
    stanford = create_list_from_file(stanford_file)

    # remove the previous files if present
     
    try:
        os.remove(path + 'berkeley_out')
        os.remove(path + 'stanford_out')
    except FileNotFoundError:
        print('File not present. Please try again.')

    # randomly flip the data based on probability

    flip_data_randomly(berkeley, stanford, PROBABILITY)

    # perform the EVALB evaluation

    berkeley_cmd = './evalb -p new.prm Overall.gold berkeley_out > berkeley_result'
    stanford_cmd = './evalb -p new.prm Overall.gold stanford_out > stanford_result'
    os.system(berkeley_cmd)
    os.system(stanford_cmd)

    # extract the f-scores from the EVALB results

    line = sub.check_output(['tail', '-20', 'berkeley_result'])
    fscore_berkeley_unlabeled = return_fscore(line)
    line = sub.check_output(['tail', '-20', 'stanford_result'])
    fscore_stanford_unlabeled = return_fscore(line)

    # remove the temporary files

    os.remove(path + 'berkeley_result')
    os.remove(path + 'stanford_result')

    # calculate the f-score differences

    berkeley_fscore_difference = fscore_gold_berkeley_unlabeled - fscore_berkeley_unlabeled
    stanford_fscore_difference = fscore_gold_stanford_unlabeled - fscore_stanford_unlabeled

    # append the results to a file

    append_results(SIG_TEST_RESULTS_LABELED_PROB0_5, berkeley_fscore_difference, stanford_fscore_difference)