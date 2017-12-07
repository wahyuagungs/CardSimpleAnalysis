from core.deck import Deck
from matplotlib import pyplot
from collections import Counter
import numpy as np
import time
import datetime
import math


# returns True if all suits in a card list are identical (e.g. all hearts)
def is_flush(cards):
    assert not len(cards) == 0, "Empty cards hand cannot be determined"
    # This is a list comprehension to get all suits in a list
    suits = [x.getSuit() for x in cards]

    # how many variance of suits in a list? if it is 5 then it's a flush
    return suits.count(suits[0]) == len(suits)  # take the first item and count it to the length of occurrences


# returns True if all suits is Heart in which this will be represented using number '0' of suit
def is_royal_flush(cards):
    # Let 0 is the Heart
    if any(x.getSuit() != 0 for x in cards):
        return False
    else:
        # get the face number of the cards
        faces = [x.getFace() for x in cards]
        royal_flush = [1, 10, 11, 12, 13]
        if set(royal_flush) == set(faces):  # compare faces list to a royal flush model using set No repetition allowed
            return True
        else:
            return False


# returns True if there are one or two pair in a set of cards
def is_pair(cards):
    assert not len(cards) == 0 or len(cards) > 5, "Empty cards input is not valid"
    # Using List comprehensions to get all faces (number of cards)
    # Counter method from collections library is being used for finding the occurrences of an item in a list
    occurrences = dict(Counter([x.getFace() for x in cards]))  # returns a dictionary object

    # if the length is less than 3, the possible sets are {[n,1],[n,4]} and {[n,5]} which n is the face number
    # if the length is more than 4, then no repetition in the set
    if len(occurrences) < 3 or len(occurrences) > 4:
        return False
    # using dict comprehension to determine if there is a value more than 2 (which is a 3 of a kind)
    if any(value > 2 for key, value in occurrences.items()):
        return False
    else:
        return True


# This is a helper method to write down the results from any function
def save_log(text, file_name):
    file = open(file_name + '-' + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + '.log', 'w')
    for i in text:
        file.write(i + '\n')
    file.close()


# creates bar charts image using matplotlib
def create_barchart(obj_dict, desc, file_name):
    try:
        assert len(desc) != 0 or len(obj_dict) != 0, 'Arguments cannot be empty'
        # pyplot figure must have a new instance number to work on with everytime this method is called
        pyplot.figure()
        interval = 5 if len(obj_dict) > 50 else 1  # this is the interval code, this will trick the xticks just to print which numbers needed
        x = np.arange(len(obj_dict))  # create np array for x label, for the interval x-axis label
        ticks = np.arange(1, len(obj_dict) + 1)  # this is the actual value of each bar
        pyplot.bar(range(len(obj_dict)), obj_dict.values(), align='center')
        pyplot.xticks(x[::interval], ticks[::interval])
        pyplot.xlabel(desc['xlabel'])
        pyplot.ylabel(desc['ylabel'])
        pyplot.title(desc['title'])
        pyplot.tight_layout()
        pyplot.savefig(file_name + '-' + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
    except AssertionError:
        raise AssertionError
    except Exception as e:
        print(e)


# create scatter plot image using matplotlib library
def create_scatterplot(x, y, desc, file_name):
    try:
        assert len(desc) != 0 or len(y) != 0 or len(x) != 0, 'Arguments cannot be empty'
        # pyplot figure must have a new instance number to work on with everytime this method is called
        pyplot.figure()
        pyplot.scatter(x, y, s=3, c='red', alpha=0.75)  # size 3 using red color not too big using 0.75 alpha transparency
        pyplot.xlabel(desc['xlabel'])
        pyplot.ylabel(desc['ylabel'])
        pyplot.title(desc['title'])
        pyplot.savefig(file_name + '-' + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
    except AssertionError:
        raise AssertionError
    except Exception as e:
        print(e)


# This experiments are intended to find the average (mean) distribution of all faces
def proving_fairness(**kwargs):
    try:
        # start timer
        start = time.time()
        # creates a deck of card with 52 cards
        deck = Deck(1, 13, 4)
        deck.shuffle()
        mean_list = []
        # init variables for iteration process
        attempts = kwargs["attempts"] if ("attempts" in kwargs) else 1000
        experiments = kwargs["experiments"] if ("experiments" in kwargs) else 100
        n = 0
        while n < experiments:
            counter, total = 0, 0
            while counter < attempts:
                card = deck.drawCard()  # get a card
                total += card.getFace()  # increment the number of faces from a card
                deck.placeCardTop(card)  # after done with the card, put it back again
                deck.shuffle()
                counter += 1
            mean_list.append(total / attempts)
            n += 1
        # create scatter plot and bar graph
        desc = {'title': 'Mean Distribution', 'xlabel': 'Experiment times', 'ylabel': 'Mean'}
        create_scatterplot(np.arange(1, 101), mean_list, desc, 'proving-fairness-scatterplot')
        # Here I am trying to create dict object from range and the mean itself for creating barchart
        keys = range(0, len(mean_list))
        d_mean = dict(zip(keys, mean_list))
        create_barchart(d_mean, desc, 'proving-fairness-barchart')

        # To describe only image without the actual results are vague, we need the actual results
        # for translating those figures
        arr = np.array(mean_list)
        std = np.std(arr, ddof=1)
        variance = np.var(arr)
        delta = time.time() - start
        max_val, min_val = np.amax(arr), np.amin(arr)
        logs = ['Final Average from 100 trials is {0}'.format(np.mean(mean_list)),
                'Standard Deviation for this model from 100 mean average is ' + str(std),
                'Variance for this model from 100 mean is ' + str(variance),
                'Min value : ' + str(min_val) + " and max value : " + str(max_val),
                'Time to complete calculation ' + str(math.ceil(delta * 100) / 100) + ' seconds']
        save_log(logs, 'proving-fairness')
        print('Proving Fairness has completed in', math.ceil(delta*100)/100, 'seconds')
    except Exception as e:
        print(e)
        save_log([e], 'error-proving-fairness')


# This experiments are intended to find 5 royal flush of hearts hands from 4 suits (Suit no. 0)
def royal_flush_chance(suit=4):
    # creates deck and shuffle the cards
    deck = Deck(1, 13, suit)
    deck.shuffle()
    probability_list = []  # this is the result container
    text = []
    experiment = 0
    # 5 experiment of finding royal flush from 4 suits
    while experiment < 5:
        # start timer
        start = time.time()
        attempts = 0
        is_found = False
        while not is_found:
            # take 5 cards from top
            cards = deck.draw_cards()
            # put back 5 cards into the deck
            deck.place_cards(cards)
            deck.shuffle()
            # determine if the drawn cards are royal flush
            if is_royal_flush(cards):
                is_found = True
            attempts += 1
        probability_list.append(1 / attempts)
        end = time.time()
        text.append('Found Royal Flush in ' + str(math.floor(end - start)) + ' s in attempts number: ' + str(attempts))
        experiment += 1
    # this section is for creating scatter plot  
    desc = {'title': 'Probability Distribution', 'xlabel': 'Experiment Number', 'ylabel': 'Probability'}
    create_scatterplot(np.arange(1, 6), probability_list, desc, 'royal-flush')
    save_log(text, 'royal-flush')  # saves the log
    print('Royal Flush Experiment has completed')


# This experiments are for finding pair and flush when drawing 5 cards from a deck
def chances_of_hands(suit=4, dynamic_suit=False, **kwargs):
    try:
        # start timer
        start = time.time()
        # init all the neccessary objects e.g. deck, mean, and counters
        deck = Deck(1, 13, suit)
        mean_pair, mean_flush = [], []
        attempts = kwargs["attempts"] if ("attempts" in kwargs) else 1000
        experiments = kwargs["experiments"] if ("experiments" in kwargs) else 100
        counter = 0
        # there will be 100 experiments conduct each to get 100 data of pair and flush from 1000 attempts
        while counter < experiments:
            i, pair_counter, flush_counter = 0, 0, 0
            while i < attempts:  # when i equals to 1000 attempt the iteration will stop
                deck.shuffle()
                # take 5 cards from top
                cards = deck.draw_cards()
                # put back the cards
                deck.place_cards(cards)
                # determine the drawn cards are pair or flush
                # this will reduce the computational cost :
                # Pair and Flush cannot be intersect, (a card hand can be pair or flush but CANNOT AT THE SAME TIME)
                if is_flush(cards):  # if it is a card then it CANNOT be a pair
                    flush_counter += 1
                elif is_pair(cards):  # if if is a pair then it CANNOT be a flush
                    pair_counter += 1
                i += 1
            # saves all the results into a list
            mean_pair.append(pair_counter / attempts)  # there will be 100 items here
            mean_flush.append(flush_counter / attempts)  # there will be 100 items here
            counter += 1

        # to avoid any unnecessary repetition code,
        # I'm using the same function but create a flag in this function to avoid plot creation
        if dynamic_suit:
            # when dynamic suit mode is Active (True) this function will stop here
            # this will returns a dictionary object contains both mean for pair and flush
            return {'pair': np.mean(mean_pair), 'flush': np.mean(mean_flush)}

        desc_pair = {'title': 'Probability Distribution of Pair Hand', 'xlabel': 'Number of Experiments',
                     'ylabel': 'Probability'}
        create_scatterplot(range(1, 101), mean_pair, desc_pair, 'chances-of-pair-scatter')
        # Here I am trying to create dict object from range and the mean itself for creating barchart
        keys = range(0, len(mean_pair))
        d_pair = dict(zip(keys, mean_pair))
        create_barchart(d_pair, desc_pair, 'chance-of-pair-bar')

        desc_flush = {'title': 'Probability Distribution of Flush Hand', 'xlabel': 'Number of Experiments',
                     'ylabel': 'Probability'}
        create_scatterplot(range(1, 101), mean_flush, desc_flush, 'chances-of-flush-scatter')
        # Here I am trying to create dict object from range and the mean itself for creating barchart
        keys = range(0, len(mean_flush))
        d_flush = dict(zip(keys, mean_flush))
        create_barchart(d_flush, desc_flush, 'chance-of-flush-bar')

        # To describe only image without the actual results are vague, we need the actual results
        # for translating those figures
        arr_pair, arr_flush = np.array(mean_pair), np.array(mean_flush)
        std_pair, std_flush = np.std(arr_pair, ddof=1), np.std(arr_flush, ddof=1)
        variance_pair, variance_flush = np.var(arr_pair), np.var(arr_flush)
        delta = time.time() - start
        max_pair, min_pair = np.amax(arr_pair), np.amin(arr_pair)
        max_flush, min_flush = np.amax(arr_flush), np.amin(arr_flush)
        logs = ['Mean values for pair and flush are {0}, {1} respectively'.format(str(np.mean(mean_pair)), str(np.mean(mean_flush))),
                'Standard Deviation for pair and flush are {0}, {1} respectively'.format(str(std_pair), str(std_flush)),
                'Variance for for pair and flush are {0}, {1} respectively'.format(str(variance_pair), str(variance_flush)),
                'Minimum and maximum value for pair are {0}, {1}'.format(str(min_pair), str(max_pair)),
                'Minimum and maximum value for flush are {0}, {1}'.format(str(min_flush), str(max_flush)),
                'Time to complete calculation ' + str(math.ceil(delta * 100) / 100) + ' seconds']
        save_log(logs, 'chances-of-hands')

        print('Chances of hands has completed in ', str(math.ceil(delta * 100) / 100), 'seconds')
    except Exception as e:
        print(e)
        save_log([e], 'error-chances-of-hands')


# This experiment will compute the mean probability of n in the range from 1 to 10 suit
def changes_in_chance(trials=10):
    try:
        start = time.time()  # start timer
        result, mean_pair, mean_flush = [], [], []  # initialize lists
        d_pair, d_flush = {}, {}  # initialize dict objects
        # do experiments 10 times from 1 to 10 suit
        for i in range(1, trials + 1):
            # each suit will be run
            d_mean = chances_of_hands(i, dynamic_suit=True)  # this will take the dict obj of result
            result.append(d_mean)
            mean_pair.append(d_mean['pair'])
            mean_flush.append(d_mean['flush'])
            d_pair[str(i)] = d_mean['pair']
            d_flush[str(i)] = d_mean['flush']

        # This just labels
        desc_pair = {'title': 'Probability Distribution of Pair Hand', 'xlabel': 'Number of Suit',
                      'ylabel': 'Probability'}
        # create scatter and bar plot for each experiment
        create_scatterplot(range(1, 11), mean_pair, desc_pair, 'changes-pair')
        create_barchart(d_pair, desc_pair, 'change-pair-bar')
        # creates log
        mean_pair = ['Probability index: ' + str(x) for x in mean_pair]
        save_log(mean_pair, 'changes_in_chance_pair')

        # This just labels
        desc_flush = {'title': 'Probability Distribution of Flush Hand', 'xlabel': 'Number of Suit',
                      'ylabel': 'Probability'}
        create_scatterplot(range(1, 11), mean_flush, desc_flush, 'changes-flush')
        create_barchart(d_flush, desc_flush, 'change-flush-bar')
        # creates log
        mean_flush = ['Probability index: ' + str(x) for x in mean_flush]
        save_log(mean_flush, 'changes_in_chance_flush')

        end = time.time()
        print('Changes in chance has completed in', math.floor(end-start), 'second')
    except Exception as e:
        print(e)
        save_log([e], 'error-changes-in-chance')


# this function is to validate input from the user
def input_validator(message, number=False, blank=False):
    val = input(message)
    if val.strip() == '' and not blank:
        print("You haven't type anything here")
        return input_validator(message, True)
    if number:
        if not val.isdigit():
            print("Your input is incorrect, Please type in numbers only")
            return input_validator(message, True)
        return int(val)
    else:
        return str(val)


# This is the main function to navigate from one experiment to another
def main():
    print("Welcome to the Gavin Experiment")
    is_finished = False
    while not is_finished:
        print('Choose experiment')
        print('1. Proving Fairness')
        print('2. Chances of Hands')
        print('3. Change in Chance')
        print('4. Quit')
        val = input_validator('Choice : ', number=True)
        if val == 1:
            print('You chose Proving Fairness Experiment', 'Please wait for the calculation is being processed')
            proving_fairness()
        elif val == 2:
            print('1. Royal Flush Experiment')
            print('2. Pair and Flush Experiment')
            print('3. Back')
            val = input_validator('Choice : ', number=True)
            if val == 1:
                print('You chose Royal Flush Experiment', 'The process will take a very long time to finish')
                royal_flush_chance()
            elif val == 2:
                print('You chose Pair and Flush Experiment', 'Please wait for the calculation is being carried out')
                chances_of_hands()
            else:
                continue
        elif val == 3:
            print('You chose Change in chance Experiment', 'Please wait for the calculation is being carried out')
            changes_in_chance()
        elif val == 4:
            is_finished = True
        else:
            print('unrecognized choice')


if __name__ == "__main__":
    main()
