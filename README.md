## Latin Library

This repository contains a project, written in Python, that downloads, parses, and indexes Latin text documents from [thelatinlibrary.com](http://www.thelatinlibrary.com/) and builds a search & translation interface on top of the resulting text dataset. This work was done for a Text Analytics course at the University of Oklahoma (CS 5970) during the Spring 2016 semester. It has since been restructured.

### [Extracting & Parsing the Data](../master/latin_library/parse_data.py)

The general steps that went into this phase of the project include the following:
1. Download a set of inconsistently structured HTML files containing Latin text data
2. Parse the meaningful Latin text "verses" out of these files an store them in a sqlite database
    * "verses" = sentences, lines, or paragraphs depending on the context
3. Create an sqlite FTS4 table for the data to facilitate fast searching (next phase) 

### [Search & Translation Interface](../master/latin_library/search_interface.py)

This phase included the implementation of a simple command-line interface to give a user the following options:

1. Search for a Latin term in the dataset
2. Search for an English term in the dataset
3. Display a "Usage Chart" for a Latin term
4. Display a "Usage Chart" for an English term

When English terms are supplied by the user, a free translation API is used to translate the term to Latin. The dataset is then searched for that translated term.

A "Usage Chart" involves a simple matplotlib bar chart showing the frequency of the given term in each of the "books" of the dataset.


For a more detailed description of work that went into this project, see the included [summary doc](../master/docs/summary.md).

