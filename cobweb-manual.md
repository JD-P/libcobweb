# Libcobweb pre-version #

## Search Statement: ##

The first portion of a cobweb search statement is a division between the columns
that will be returned by the search and the actual search query:

     (<COLUMNS>) | <QUERY>

The syntax is exactly as shown with '<COLUMNS>' and '<QUERY>' replaced with the
appropriate syntax for columns and the appropriate syntax for a query.

## Columns: ##

Most important columns in cobweb are 'top level', meaning that they can simply
be named as themselves with no issues, for example if you were searching the text
of URL's for the string 'dog' you could type:

   'dog' IN url

(The capitalization of 'in' is not strictly necessary, but as shall become 
apparent later it makes it much easier to distinguish between language portions
and actual data being manipulated.)

This is because the columns in the meta-table are 'special' from the programs 
perspective, they're the first ones that the program goes to when it searches
for columns to pull data from. Other columns that are specific to a certain
browser must be referred to with a *fully qualified* name. That is, starting
with the name of the browser you must specify a path that leads to the column:

     browser.table.column

For an example:

    abc.def.ghi

Would get you the column 'ghi' in the table 'def' in the database of the browser
'abc'. 

## Aliases: ##

Before continuing, it's important to note that when writing out a single query
that fully qualified names or other elements might get long. Cobweb lets you 
define aliases in your query. An alias is a piece of text that the search engine
will 'expand' out to become another piece of text. For example, the alias:

     alias:browser.table.column

Would turn every unquoted instance of the term '%alias' into 
'browser.table.column'. This lets you significantly cut down on the length of
search queries if you find yourself writing out the same long names over and
over. Aliases must always come at the start of a search query. 

Aliases must be referred to in search queries with the % symbol prepended to
so that the program does not confuse them for column names or logical operators.

## Column declaration: ##

The first portion of a cobweb search statement is to declare what columns the
search should return data from. To return every column in every row of every
table involved in the search you use the asterick like so:

      (*)

Otherwise the syntax for column declarations is as follows. Each column is 
declared as its qualified name and seperated by commas. The entire set of 
declarations is enclosed in parenthesis, like so:

	     (titles, urls)

Columns are returned in the order that they're given in the declarations.

## Queries: ##

Searches in databases rely on the fact that you can ask True or False questions
about data in the columns of each row. Search queries in cobweb are one long yes
or no question about the data that is chained together using boolean logic and
other logical operators. For example:

      (*) | 'search_term' IN urls AND 'search_term' IN titles;

Will ask a single yes or no question, which is whether the search term is in
urls AND in titles, if either of these is false then the entire statement is
false and the row is not returned as a result.

There is a defined order of operations for cobweb search queries, so that there
is no ambiguity as to which parts of the statement should be evaluated first:

1. Aliases.

2. Parenthesis.

3. NOT

4. Comparison operators: < > <= >= = IN

5. AND

6. OR

## Advanced language spec: ##

### Alias token: ###



## Quick Start Guide: ##

I want to:

- Look for a search term in both the URL and title of a web page:

  (*) | 'search_term' IN urls OR 'search_term' IN titles;

- Look at all the pages between 2015-05-01 and 2015-05-19:

  (*) | <date_of_visit_token> >= 2015-05-01 AND <date_of_visit_token> <= 2015-05-19