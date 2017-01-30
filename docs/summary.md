## Parsing

In general, I parsed each collection by first creating a BeautifulSoup object out of the initial 
'collection.html' page and extracting the 'title', 'author', and 'dates' values to be used throughout the collection.

Next, I found all of the <a> tags on the initial page and extracted the 'link' values for each book from the href
of each tag and an initial 'book' value from the content/string of each tag.

After obtaining all links/books, I iterated over them, creating BeautifulSoup objects out of each book page. At this
point in some collections I handled a few edge cases by editing the html formatting (described in detail below). For 
each book page, I extracted a more descriptive 'book' value if one existed, and parsed the content of the page into
passages while detecting chapters and keeping track of a verse number (more detail below).

#### title

For 3 of my collections (all but Silius), I extracted the string of the <title> tag from the initial 
'collection.html' page and used this value as the title throughout that collection. For the Silius
collection, the content of this tag was slightly different from the others so for the sake of consistency
I hard-coded the title to be 'Silius'.

#### book

As described above, I first took the string from the link to the book page to be the book field value. Then, 
if a more descriptive value was found on the actual book page (in a <title> or <h1> tag usually), I extracted
this and updated the book value. In two special cases, the most descriptive, consistent value available was 
'Liber x' where x is a number. Because I believe 'Liber' means 'Book' in Latin, I manually replaced it with a
more descriptive, appropriate value (Liber III --> Punica III, for example).

#### language

As far as I can tell, all of my collections were Latin, so I used 'Latin' in all cases. 

#### author

I believe all of my collections were works of a particular author so I extracted the full name of each from
the initial 'collection.html' page (usually from an h1 tag) and used it as the author for that collection. 

#### dates

For all of my collections, there was a date under the 'author' name (see above) on the initial 
'collection.html' page. I believe these are actually just the birth/death years of the author, but none of 
the books in my collections contained any other date information, so I used this value instead of 'null'
because it at least gives a range that the date must be in (book can't be written before/after the birth/death
of the author, right?).   

#### chapter

Some books (all in the Silius collection, for example) seemed to have a simple poem structure with no chapters.
In these cases I used the value 'null' for chapters. In cases where chapters were present in my collections, 
they were nearly always containing in a <b> tag, making them fairly easy to detect and extract. In one special 
case (Silvae III, Statius collection), text that I believed to be a chapter name was not contained in a <b> tag,
which I handled as a special case.

#### verse

My general strategy for verse numbers was to keep a running count of the verses, and when an explicit verse number 
was given I updated my verse counter to the explicit value. I believe this was a good compromise between giving each
verse its own unique value (using just the simple verse number) and relying completely on the file for all verse
numbers. With my strategy, some consecutive verses may have the same verse number (due incorrect/unexpected explicitly
defined numbers) but verses will be extremely close to the explicitly defined values, making them much easier to find
in the original text.  

#### passage

In general, for the 'poem' pages I treated each line as a verse and extracted the text as the passage value. In 
the cassiodorus collection, nearly all sentences began with a number that I treated as the verse number, so I
extracted each sentence text as the passage. In all other cases I extracted the text of entire paragraphs as the 
passage value.

#### link

All link values were obtained from the href value of the appropriate <a> tag on the initial 'collection.html' page
for each collection.


### Special Parsing - Cassiodorus

The books 'Orationum Reliquiae' and 'de Musica' required their own specific parsing code due to unique format.


### Special Parsing - Statius

For the books 'Silvae II' and 'Silvae V', text following a <br> or <BR> tag was not placed on the next line. This was
inconsistent with all other html files and caused problems with the way I was parsing. Instead of writing unique parsing
code to handle these cases, I took the html text, inserted newline characters after each <br> and <BR> tag, and created
a BeautifulSoup object from the edited/fixed string. This allowed me to parse these files in the same way as all others
in this collection.

Additionally, for all of the 'Silvae' books, an additional chapter and paragraph were located at the top of the file. For
these files I extracted these items, parsed them appropriately, and then parsed the rest of the file in the same way as 
every other file in this collection. 


### Special Parsing - Virgil

For 8 books in this collection, I added newlines after <br> and <BR> tags as I did for some books in the Statius collection.
The reasoning was the same as above.

A special parsing case arose in the 'Ecloga' books where what I believe to be the names of the speaking character (I think
this is a play or something similar) were found on significantly indented lines in the middle of the typical 'poem' structure.
Because I didn't believe these values were relevant to any searching we may perform in the next phase and they were
ignored by the explicit verse numbers given, I ignored them. Because of the structure of some of the html files this proved 
to be a fairly time consuming task. 


#### Special Parsing - Silius

For the last 2 books in this collection, verse numbers that were typically on the end of the line were instead on their own
separate line because of inconsistent html structure. Instead of adding unique parsing code for these books, I iterated through
the lines concatenating the verse numbers with the previous lines before parsing. This allowed me to parse the files in the same
way as all other files in this collection.


## Translation

For English->Latin translation, I used mymemory.translated.net. The json object returned contains multiple possible translations, 
but only one is contained in the "translatedText" field. In my testing, this value seemed to consistently be the best choice, so 
I used it for all translations. If no translation is found, the inputted search term is returned, handling various edge cases.


## Search Interface

I implemented a simple command-line interface that allows user to repeatedly search/visualize based on an English or Latin search term.
The search results are returned with their surrounding context (passage) and a link to their location in the original document along 
with some information (chapter, verse) to point the user to the exact location of their search term.


## Usage Chart

For my usage chart/visualization, I created a bar chart with one bar for each book in the database. I only have 4 collections, so 
I thought it best to break the search term occurrences up by book instead. This allows me to fit more data on the screen, and I preserved
the collection data by color-coding the bars by collection. I also added a legend and performed some basic formatting on the plot.

