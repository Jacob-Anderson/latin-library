#!/usr/bin/python3

import subprocess
import sqlite3
import json
import numpy as np
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

# prompt to display to user during input loop
input_prompt = 'Enter the corresponding number to choose an action:' + '\n'
input_prompt += '1. Latin term search' + '\n'
input_prompt += '2. English term search' + '\n' 
input_prompt += '3. Usage chart - Latin term' + '\n'
input_prompt += '4. Usage chart - English term' + '\n'
input_prompt += '5. Quit' + '\n\n'
input_prompt += '>> '


# translate an english phrase to an appropriate latin phrase
def translate(english_phrase):

    # wget command using free translation api
    # returns json object with possible translations
    c1 = ['wget', '-q', '-O', '-', 'http://mymemory.translated.net/api/get?q=' 
                                   + english_phrase + '&langpair=en|la']
    p1 = subprocess.Popen(c1, stdout=subprocess.PIPE)

    # use python json.tool to get json object in a usable form
    c2 = ['python', '-m', 'json.tool']
    p2 = subprocess.Popen(c2, stdin=p1.stdout, stdout=subprocess.PIPE)    

    # decode result of above command and create json object from it
    result = json.loads(p2.stdout.read().decode('utf-8'))

    # extract 'best' translation - if no appropriate translation is found, 
    # the english phrase will be returned unchanged (handles many error cases) 
    return result['responseData']['translatedText']  


# search the created fts table for a latin phrase
# return results paired with their locations in their original documents
def search(search_term):

    # command line formatting
    print('\nSearch Term: ' + search_term + '\n')

    # create database connection
    db = sqlite3.connect('latin_library.db')
    c = db.cursor()

    # execute sqlite3 statement to obtain search results
    c.execute('SELECT * FROM latin_fts WHERE passage MATCH ?', [search_term])
    results = c.fetchall()
    
    # search term found case
    if len(results) > 0:

        # iterate over search results
        for result in results:
            
            # display search result
            print('Search Result')
            print('-----------------------------------------------------------')
            print(result[0] + '\n')
            
            # display location of search result in its original document
            print('Full Text: ' + result[1])
            
            # additional location info = collection
            print('Collection: ' + result[2])

            # additional location info = book
            print('Book: ' + result[3])

            # additional location info - chapter (optional)
            if result[4] != 'null':
                print('Chapter: ' + result[4])

            # additional location info - verse
            print('Verse: ' + str(result[5]) + '\n\n')

    # search term not found case
    else:
        print('\nNo Results\n')

    # commit changes and close db connection
    db.commit()
    db.close()


# create and display a usage chart for the given search term 
# across all books in which the search term occurs
def usageChart(search_term):

    # create database connection
    db = sqlite3.connect('latin_library.db')
    c = db.cursor()

    # command line formatting
    print('\nUsage Chart: ' + search_term)
    
    # statement to obtain counts of search results by book along with book names
    c.execute('''SELECT book, COUNT(*), title 
                 FROM latin_fts 
                 WHERE passage MATCH ? 
                 GROUP BY book''', [search_term]);
    results = c.fetchall()

    # search term found case
    if len(results) > 0:

        unsorted_data = []
        x_data = []
        y_data = []
        colors = []
        max_y = 0

        # iterate over search results
        for i in range(len(results)):
    
            # track max y value for plot formatting later
            if results[i][1] > max_y:
                max_y = results[i][1]
            
            # set colors of bars to group them by collection
            if results[i][2] == 'Cassiodorus':
                color = 'r'

            elif results[i][2] == 'Statius':
                color = 'g'

            elif results[i][2] == 'Vergil':
                color = 'b'

            elif results[i][2] == 'Silius':
                color = 'y'

            # add book name, occurence count, and bar color to list of data
            unsorted_data.append((results[i][0], results[i][1], color))
         
        # sort unsorted_data by decreasing occurence count
        sorted_data = sorted(unsorted_data, key=lambda x: x[1], reverse=True)
        
        # add sorted values to data lists for plotting
        for x,y,c in sorted_data:
            x_data.append(x)
            y_data.append(y)
            colors.append(c)

        # plot bar chart using search term occurences
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.canvas.set_window_title('Usage Chart for \'' + search_term + '\'')
        ys = np.arange(len(y_data))
        barlist=plt.bar(ys, y_data, width=.4)
        plt.xticks(ys + .4 / 2, x_data)

        # x and y labels for usage chart
        plt.xlabel('Books with at least 1 occurence of \'' + search_term + '\'')
        plt.ylabel('Number of occurrences of \'' + search_term + '\'')

        # set colors of bars depending on collection
        for i in range(len(barlist)):
            barlist[i].set_color(colors[i])

        # create legend for bars
        labels = ['R', 'G', 'B', 'Y']
        l_vals = ['Cassiodorus', 'Statius', 'Vergil', 'Silius']
        pls = [Line2D([0], [0], linestyle='none', 
               marker=r'$\mathregular{{{}}}$'.format(l)) for l in labels]
        plt.legend(pls, l_vals, numpoints=1, markerscale=2, loc='upper right')
        
        # format the xlabels for readability
        fig.autofmt_xdate()

        # set y range to be 0 through the max value + 1 for visual appeal
        plt.ylim([0, max_y+1])
        
        # display barplot
        plt.show() 

    # search term not found case
    else:
        print('\nNo Results\n')

    # commit changes and close db connection
    db.commit()
    db.close()


def main():

    user_input = ''

    # loop until user selects quit option
    while user_input != '5':

        # user selection
        user_input = input(input_prompt)
        
        # latin term search case
        if user_input == '1':
            search(input('\nEnter a Latin search term: '))

        # english term search case
        elif user_input == '2':
            search(translate(input('\nEnter an English search term: ')))

        # usage chart latin term case
        elif user_input == '3':
            usageChart(input('\nEnter a Latin search term: '))

        # usage chart english term case
        elif user_input == '4':
            usageChart(translate(input('\nEnter an English search term: ')))

        # quit case
        elif user_input != '5':
            print('Invalid Input')

        # output formatting
        print('')

if __name__ == '__main__':
    main()
