import pytest
import os
import subprocess
import json
import sqlite3

# paths to expected directories after collections have been downloaded
paths = ['./www.thelatinlibrary.com/cassiodorus/',
         './www.thelatinlibrary.com/silius/',
         './www.thelatinlibrary.com/vergil/',
         './www.thelatinlibrary.com/statius/']

# expected number of files (html pages, one for each book) 
# in the directories found at the above paths (in order)
expected_file_counts = [17, 17, 26, 19]

# expected names of created sqlite tables
expected_table_name = 'latin_text'
expected_fts_table_name = 'latin_fts'

# expected column names of created sqlite tables
expected_columns = ['title', 'book', 'language', 'author', 
                    'dates', 'chapter', 'verse', 'passage', 'link']
expected_fts_columns = ['passage', 'link', 'title', 'book', 'chapter', 'verse']


# test that files have been correctly download by checking that actual number of
# files in each directory in 'paths' is equal to the expected number
def test_files_downloaded():

    # iterate over paths and expected file counts
    for path, expected_file_count in zip(paths, expected_file_counts):
        
        # count number of files in the directory found at the current path
        file_count = len([f for f in os.listdir(path) 
                          if os.path.isfile(os.path.join(path, f))])

        # test that actual file count is equal to the expected file count
        assert file_count == expected_file_count


# test that database has been created correctly by checking that tables exist w/
# the expected names and that the tables have the expected number of columns and
# appropriate column names
def test_database_schema():

    # establish database connection
    db = sqlite3.connect('latin_library.db')
    c = db.cursor()

    # test that expected table names are in list of all sqlite tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    assert (expected_table_name,) in tables
    assert (expected_fts_table_name,) in tables

    # test that the number of columns in the main table is as expected
    columns = c.execute("pragma table_info('latin_text')").fetchall()
    assert len(columns) == len(expected_columns)

    # test that each column is one of the expected columns
    for column in columns:
        assert column[1] in expected_columns

    # test that the number of columns in the fts table is as expected
    columns = c.execute("pragma table_info('latin_fts')").fetchall()
    assert len(columns) == len(expected_fts_columns)

    # test that each column is one of the expected columns
    for column in columns:
        assert column[1] in expected_fts_columns


# test that data was correctly inserted into the database by checking that the 
# number of distinct title and book field values are as expected 
def test_database_insertion():

    # establish database connection
    db = sqlite3.connect('latin_library.db')
    c = db.cursor()

    # count the number of distinct title values in the database 
    # (number of collections correctly inserted)
    c.execute('''select count(distinct title) from latin_text;''')
    title_count = c.fetchone()[0]

    # count the number of distinct book values in the database 
    # (number of books correctly inserted)
    c.execute('''select count(distinct book) from latin_text;''')
    book_count = c.fetchone()[0]

    # test that the title and book counts are equal to the expected numbers
    assert title_count == len(expected_file_counts)
    assert book_count == sum(expected_file_counts)

    # count the number of distinct title values in the database 
    # (number of collections correctly inserted) - fts table
    c.execute('''select count(distinct title) from latin_text;''')
    title_count = c.fetchone()[0]

    # count the number of distinct book values in the database 
    # (number of books correctly inserted) - fts table
    c.execute('''select count(distinct book) from latin_text;''')
    book_count = c.fetchone()[0]

    # test that the title and book counts are equal to the expected numbers
    assert title_count == len(expected_file_counts)
    assert book_count == sum(expected_file_counts)


# test that the translation service is behaving as expected by giving it a word 
# to translate and asserting that the translation returned is an expected value
def test_translation_service():
    
    # wget command using free translation api
    # returns json object with possible translations
    c1 = ['wget', '-q', '-O', '-',  
          'http://mymemory.translated.net/api/get?q=death&langpair=en|la']
    p1 = subprocess.Popen(c1, stdout=subprocess.PIPE)

    # use python json.tool to get json object in a usable form
    c2 = ['python', '-m', 'json.tool']
    p2 = subprocess.Popen(c2, stdin=p1.stdout, stdout=subprocess.PIPE)    

    # decode result of above command and create json object from it
    result = json.loads(p2.stdout.read().decode('utf-8'))

    # extract 'best' translation
    # test that the translated value is 'necro' in this case - the expected value
    assert result['responseData']['translatedText'] == 'necro' 

