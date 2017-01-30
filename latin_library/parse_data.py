#!/usr/bin/python3

import os
import sqlite3
import codecs
import re
from bs4 import BeautifulSoup

# root shared by all collection urls
URL_ROOT = 'www.thelatinlibrary.com/'

# list of ends of all collection urls
URL_EXTENSIONS = ['cassiodorus',
                  'statius',
                  'verg',
                  'silius']


# download the given collection from 'www.thelatinlibrary.com/{collection}.html'
def download_collection(collection):
    os.system('wget -r -l 1 ' + URL_ROOT + collection + '.html')


# parse the 'cassiodorus' collection into database item attribute lists
def parse_cassiodorus():

    cassiodorus_items = []

    # first collection
    collection = URL_EXTENSIONS[0]

    # create beatiful soup object for initial page
    soup = BeautifulSoup(open(URL_ROOT + collection + ".html"), 'html.parser')

    # extract collection title from initial page
    title = soup.title.string.strip()

    # extract author and date information from defined 'pagehead' p tag
    author_dates = soup.select('.pagehead')[0].get_text().split('\n')
    author = author_dates[0]
    dates = author_dates[1][1:-1]

    # find all link tags on initial page
    link_tags = soup.find_all('a')

    # book titles and links locations
    books = []
    links = []

    # get the link strings and href content from all but the last 3 link tags
    for tag in link_tags[:-3]:
        books.append(tag.string)
        links.append(URL_ROOT + tag.get('href'))

    # iterate over books
    for book_num in range(len(books)):

        # create beautiful soup object for current book page
        with codecs.open(links[book_num], 
                         encoding='utf-8', 
                         errors='replace') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # update some book fields to more descriptive values
        if book_num < 13:
            books[book_num] = soup.title.string.strip()[13:]       

        # extract all p tags and remove irrelavant tags at beginning and end
        paragraphs = soup.find_all('p')[2:-2]

        # special parsing case for 'Orationum Reliquiae'
        if book_num == 14:
            
            # verse counter
            v_count = 1

            # iterate over relevant p tags
            for p in paragraphs:

                # intentionally ignore some meaningless p tags in this book
                if len(p.string.strip()) > 5:
                    
                    # set verse with counter and use content of p tag as passage        
                    verse = str(v_count)
                    passage = p.string.strip()

                    v_count += 1

                    # remove unexpected newline characters from some attributes
                    title = re.sub('\n', '', title)
                    books[book_num] = re.sub('\n', '', books[book_num])
                    author = re.sub('\n', '', author)
                    dates = re.sub('\n', '', dates)
                    chapter = re.sub('\n', '', chapter)

                    # add attribute list to items to return
                    cassiodorus_items.append([title, books[book_num], 
                                             'Latin', 
                                             author, 
                                             dates, 
                                             'null', 
                                             verse, 
                                             passage, 
                                             links[book_num]])
                
        # special parsing case for 'de Musica'
        elif book_num == 16:
            
            # iterate over relevant p tags
            for p in paragraphs:
                
                # extract chapter names
                if p.b is not None:
                    chapter = p.b.string.strip()

                # chapter content
                elif p.string is not None and p.string.strip() != '':
                    
                    paragraph = p.string.strip()  

                    # split content by 'x.' where x is a number (the verse num)
                    verses_passages = re.split('(\d+\.)', paragraph)

                    # ignore the first element (text before the first 'x.')
                    vp_count = 1
                    while vp_count < len(verses_passages) - 1:
                        
                        # extract verse number and passage text
                        verse = verses_passages[vp_count]
                        passage = verses_passages[vp_count+1].strip() 

                        # increment to next verse,passage group
                        vp_count += 2

                        # remove unexpected newline characters from attributes
                        title = re.sub('\n', '', title)
                        books[book_num] = re.sub('\n', '', books[book_num])
                        author = re.sub('\n', '', author)
                        dates = re.sub('\n', '', dates)
                        chapter = re.sub('\n', '', chapter)

                        # add attribute list to items to return
                        cassiodorus_items.append([title, books[book_num], 
                                                 'Latin', 
                                                 author, 
                                                 dates, 
                                                 chapter, 
                                                 verse, 
                                                 passage,  
                                                 links[book_num]])        
    
        # general parsing case for remaining books
        else:
            # track verse number in the case where a verse number is not given
            next_verse_num = 1  

            # iterate over relevant p tags
            for p in paragraphs:

                # extract chapter names
                if p.b is not None:                
                    chapter = p.b.string.strip()
                    next_verse_num = 1            # new chapter, reset verse num
                
                # chapter content
                elif p.string is not None and p.string.strip() != '':

                    paragraph = p.string.strip()

                    # if the paragraph does not begin with a verse number, 
                    # insert one using information about the current chapter 
                    # and previoius verse numbers        
                    if paragraph[0] != '[':

                        paragraph = '[' + str(next_verse_num) + '] ' + paragraph
                   
                    # split content by '[x]' where x is a number (the verse num)
                    verses_passages = re.split('(\[\d*\])', paragraph)

                    # ignore the first element (text before the first '[x]')
                    vp_count = 1
                    while vp_count < len(verses_passages) - 1:
                        
                        # extract verse number and passage text
                        verse = verses_passages[vp_count][1:-1]
                        passage = verses_passages[vp_count+1].strip()

                        # update next verse number in case 
                        # the next paragraph doesn't have one
                        next_verse_num = int(verse) + 1

                        # increment to next verse,passage group
                        vp_count += 2
            
                        # remove unexpected newline characters from attributes
                        title = re.sub('\n', '', title)
                        books[book_num] = re.sub('\n', '', books[book_num])
                        author = re.sub('\n', '', author)
                        dates = re.sub('\n', '', dates)
                        chapter = re.sub('\n', '', chapter)

                        # add attribute list to items to return
                        cassiodorus_items.append([title, books[book_num], 
                                                 'Latin', 
                                                 author, 
                                                 dates, 
                                                 chapter, 
                                                 verse, 
                                                 passage, 
                                                 links[book_num]])         

    return cassiodorus_items    


# parse the 'statius' collection into database item attribute lists
def parse_statius():

    statius_items = []

    # second collection
    collection = URL_EXTENSIONS[1]

    # create beatiful soup object for initial page
    soup = BeautifulSoup(open(URL_ROOT + collection + ".html"), 'html.parser')

    # extract collection title from initial page
    title = soup.title.string.strip()

    # extract author information from first h1 tag of page
    author = soup.find_all('h1')[0].string.strip()

    # extract date information from 'date' h1 tag
    dates = soup.select('.date')[0].get_text().strip()[1:-1]

    # find all link tags on initial page
    link_tags = soup.find_all('a')

    # book titles and links locations
    books = []
    links = []

    # get the link strings and href content from all but the last 2 link tags
    for tag in link_tags[:-2]:
        books.append(tag.string)
        links.append(URL_ROOT + tag.get('href'))

    # iterate over books
    for book_num in range(len(books)):
        
        # create beautiful soup object for current book page
        with codecs.open(links[book_num], 
                         encoding='utf-8', 
                         errors='replace') as f:

            # insert neccessary formatting to html of 2 books
            if book_num == 13 or book_num == 16:
                text = re.sub('<br>', '<br>\n', f.read())
                text = re.sub('<BR>', '<BR>\n', text)
                soup = BeautifulSoup(text, 'html.parser')

            else:
                soup = BeautifulSoup(f, 'html.parser')

        # update book field to a more descriptive value
        books[book_num] = soup.title.string.strip()[9:]

        # default chapter value
        chapter = 'null'

        # verse counter
        verse = 1

        # special parsing case for beginning of these 4 files
        if book_num >= 12 and book_num <= 16:

            # all relevant p tags
            p_tags = soup.find_all('p')[2:-1]

            # beginning of these files is a chapter, verse combo
            chapter = p_tags[0].get_text().strip()
            passage = p_tags[1].get_text().strip()

            # remove unexpected newline characters from attributes
            title = re.sub('\n', '', title)
            books[book_num] = re.sub('\n', '', books[book_num])
            author = re.sub('\n', '', author)
            dates = re.sub('\n', '', dates)
            chapter = re.sub('\n', '', chapter)

            # add attribute list to items to return
            statius_items.append([title, books[book_num], 
                                 'Latin', 
                                 author, 
                                 dates, 
                                 chapter, 
                                 verse, 
                                 passage, 
                                 links[book_num]])

            # update p_tags
            p_tags = p_tags[2:]

        # general case for all other files
        else:
            # only relevant p tag
            p_tags = soup.find_all('p')[2:3]
    
        # iterate over p tags
        for p in p_tags:

            # extract chapter names
            if p.b is not None:
                chapter = p.get_text().strip()
                verse = 1

            # chapter content
            else:
                # extract relevant p tag text
                p_text = p.get_text()

                # split the relevant text into lines
                p_lines = re.split('\n', p_text)

                # iterate over relevant lines
                for i in range(1, len(p_lines) - 1):

                    # ignore blank lines
                    if p_lines[i].strip() != '':

                        # attempt to split the line by 'x' 
                        # where x is any number of digits (the verse number)
                        split_line = re.split('(\d+)', p_lines[i].strip())
                        
                        # split success - verse number explicitly given                
                        if len(split_line) > 1:

                            # set verse number to explicitly given value 
                            # in case simple line counter is off
                            verse = int(split_line[1].strip())

                        # extract passage text
                        passage = split_line[0].strip()                   

                        # remove unexpected newline characters from attributes
                        title = re.sub('\n', '', title)
                        books[book_num] = re.sub('\n', '', books[book_num])
                        author = re.sub('\n', '', author)
                        dates = re.sub('\n', '', dates)
                        chapter = re.sub('\n', '', chapter)

                        # add attribute list to items to return
                        statius_items.append([title, books[book_num], 
                                             'Latin', 
                                             author, 
                                             dates, 
                                             chapter, 
                                             verse, 
                                             passage, 
                                             links[book_num]])

                        # increment verse counter
                        verse += 1

    return statius_items


# parse the 'virgil' collection into database item attribute lists
def parse_virgil():
    
    virgil_items = []

    # third collection
    collection = URL_EXTENSIONS[2]

    # create beatiful soup object for initial page
    soup = BeautifulSoup(open(URL_ROOT + collection + ".html"), 'html.parser')

    # extract collection title from initial page
    title = soup.title.string.strip()

    # extract author information from first h1 tag of page
    author = soup.find_all('h1')[0].string.strip()

    # extract date information from 'date' h1 tag
    dates = soup.find_all('h2')[0].string.strip()[1:-1]

    # find all link tags on initial page
    link_tags = soup.find_all('a')

    # book titles and links locations
    books = []
    links = []

    # get the link strings and href content from all but the last 2 link tags
    for tag in link_tags[:-2]:
        books.append(tag.string)
        links.append(URL_ROOT + tag.get('href'))  

    # replace some book names with a more desciptive version
    for i in range(len(books)):
        if 'Liber' in books[i]:
            books[i] = re.sub('Liber', 'Georgicon', books[i]) 

    # iterate over books
    for book_num in range(len(books)):

        # create beautiful soup object for current book page
        with codecs.open(links[book_num], 
                         encoding='utf-8', 
                         errors='replace') as f:    

            # insert neccessary formatting to html of 8 books
            if ((book_num >= 16 and book_num <= 21) 
                or book_num == 24 or book_num == 25):

                text = re.sub('<br>', '<br>\n', f.read())
                text = re.sub('<BR>', '<BR>\n', text)
                soup = BeautifulSoup(text, 'html.parser')

            else:
                soup = BeautifulSoup(f, 'html.parser')      

        # split text of html page into lines, ignoring the first 9 and last 5
        p_lines = soup.get_text().strip().split('\n')[9:-5]

        # default chapter value
        chapter = 'null'

        # verse counter
        verse = 1  

        # iterate over relevant lines
        for i in range(len(p_lines)):

            # special case in 'ecloga' books 
            # line is significantly indented and contains unwanted data
            if re.match(r'^\s{10,}', p_lines[i]):

                # strip to remove indentation
                p_lines[i] = p_lines[i].strip()                   
            
                # beginning with the 2nd letter, 
                # find the end of the current 'word' (it's a name in this case)
                j = 1
                while j < len(p_lines[i]) and p_lines[i][j].islower():
                    j += 1
            
                # remove leading 'word' from line
                p_lines[i] = p_lines[i][j:].strip()


            # ignore blank lines and lines beginning with whitespace
            if p_lines[i].strip() != '':

                # attempt to split the line by 'x'
                # where x is any number of digits (the verse number)
                split_line = re.split('(\d+)', p_lines[i].strip())
                
                # split success - verse number explicitly given                
                if len(split_line) > 1:

                    # set verse number to explicitly given value 
                    # in case simple line counter is off
                    verse = int(split_line[1].strip())

                # extract passage text
                passage = split_line[0].strip()                   

                # remove unexpected newline characters from attributes
                title = re.sub('\n', '', title)
                books[book_num] = re.sub('\n', '', books[book_num])
                author = re.sub('\n', '', author)
                dates = re.sub('\n', '', dates)
                chapter = re.sub('\n', '', chapter)

                # add attribute list to items to return
                virgil_items.append([title, books[book_num], 
                                    'Latin', 
                                    author, 
                                    dates, 
                                    chapter, 
                                    verse, 
                                    passage, 
                                    links[book_num]])

                # increment verse counter
                verse += 1
            
    return virgil_items


# parse the 'silius' collection into database item attribute lists
def parse_silius():
    
    silius_items = []

    # fourth collection
    collection = URL_EXTENSIONS[3]

    # create beatiful soup object for initial page
    soup = BeautifulSoup(open(URL_ROOT + collection + ".html"), 'html.parser')

    # define collection title
    title = 'Silius'

    # extract author information from first h1 tag of page
    author = soup.find_all('h1')[0].string.strip()

    # extract date information from 'date' h1 tag
    dates = soup.find_all('h2')[0].string.strip()[1:-1]

    # find all link tags on initial page
    link_tags = soup.find_all('a')

    # book titles and links locations
    books = []
    links = []

    # get the link strings and href content from all but the last 2 link tags
    for tag in link_tags[:-2]:
        books.append(tag.string)
        links.append(URL_ROOT + tag.get('href'))  

    # replace book names with a more desciptive version
    for i in range(len(books)):
        if 'Liber' in books[i]:
            books[i] = re.sub('Liber', 'Punica', books[i]) 

    # iterate over books
    for book_num in range(len(books)):
    
        # create beautiful soup object for current book page
        with codecs.open(links[book_num], 
                         encoding='utf-8', 
                         errors='replace') as f:
                soup = BeautifulSoup(f, 'html.parser')

        # split text of html page into lines, ignoring first 9 and last 6 lines
        p_lines = soup.get_text().strip().split('\n')[9:-6]

        # fix special parsing issue for 2 books 
        # verse numbers on their own line instead of at the end of the right line
        if book_num == 15 or book_num == 16:
            
            j = 0
            while True:

                # exit loop condition
                if j >= len(p_lines):
                    break

                # if this is a verse number line, 
                # concatenate it with the previous line 
                # and delete the verse number line    
                if re.match(r'\d+', p_lines[j]):
                    p_lines[j-1] = p_lines[j-1] + p_lines[j]
                    del p_lines[j]

                j += 1

        # default chapter value
        chapter = 'null'

        # verse counter
        verse = 1  

        # iterate over relevant lines
        for i in range(len(p_lines)):

            # ignore blank lines
            if p_lines[i].strip() != '':

                # attempt to split the line by 'x' 
                # where x is any number of digits (the verse number)
                split_line = re.split('(\d+)', p_lines[i].strip())
                
                # split success - verse number explicitly given                
                if len(split_line) > 1:

                    # set verse number to explicitly given value 
                    # in case simple line counter is off
                    verse = int(split_line[1].strip())

                # extract passage text
                passage = split_line[0].strip()              

                # remove unexpected newline characters from attributes
                title = re.sub('\n', '', title)
                books[book_num] = re.sub('\n', '', books[book_num])
                author = re.sub('\n', '', author)
                dates = re.sub('\n', '', dates)
                chapter = re.sub('\n', '', chapter)

                # add attribute list to items to return
                silius_items.append([title, books[book_num], 
                                    'Latin', 
                                    author, 
                                    dates, 
                                    chapter, 
                                    verse, 
                                    passage, 
                                    links[book_num]])

                # increment verse counter
                verse += 1

    return silius_items


# parse the downloaded collections,
# creating a list of attribute lists to insert into a database later
def parse_collections():

    # list of attribute lists for database insertion later
    passage_items = []

    # parse individual collections and build list of attribute lists
    passage_items.extend(parse_cassiodorus())
    passage_items.extend(parse_statius())
    passage_items.extend(parse_virgil())
    passage_items.extend(parse_silius())

    return passage_items


# create and populate a sqlite3 database with a pre-defined schema 
# given a list of attribute lists
def populate_database(items):

    # create database connection
    db = sqlite3.connect('latin_library.db')
    c = db.cursor()

    # create latin_text table with appropriate attributes
    c.execute('''CREATE TABLE latin_text (title text, 
                                          book text, 
                                          language text, 
                                          author text, 
                                          dates text, 
                                          chapter text, 
                                          verse integer, 
                                          passage text, 
                                          link text)''')

    # insert table row for each set of passage attributes
    for index in range(0, len(items)):
        c.execute('INSERT INTO latin_text VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                  items[index])

    # commit changes and close db connection
    db.commit()
    db.close()


# create and populate an fts4 table from the previously created latin_text table
def create_fts_table():

    # create database connection
    db = sqlite3.connect('latin_library.db')
    c = db.cursor()

    # create latin_fts table with appropriate attributes
    c.execute('''CREATE VIRTUAL TABLE latin_fts USING fts4(passage, 
                                                           link, 
                                                           title, 
                                                           book, 
                                                           chapter, 
                                                           verse)''')
    
    # populate latin_fts table
    c.execute('''INSERT INTO latin_fts 
                 SELECT passage, link, title, book, chapter, verse 
                 FROM latin_text''')

    # commit changes and close db connection
    db.commit()
    db.close()


def main():

    # download all collections
    for extension in URL_EXTENSIONS:
        download_collection(extension)
    
    # parse the collections into 'items' corresponding to database rows
    items = parse_collections()

    # create and populate a database with the parsed items
    populate_database(items)

    # create and populate an fts table for use in phase 2
    create_fts_table()
    
if __name__ == "__main__":
    main()
