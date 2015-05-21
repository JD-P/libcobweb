# Libcobweb pre-version #

## Quick Start Guide: ##

I want to:

- Look for a search term in both the URL and title of a web page:

  (*) | 'search_term' IN urls OR 'search_term' IN titles;

- Look at all the pages between 2015-05-01 and 2015-05-19:

  (*) | <date_of_visit_token> >= 2015-05-01 AND <date_of_visit_token> <= 2015-05-19

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

%<alias_name>

Example: %ALIAS

Terms: None

Description: Is expanded from a map of alias strings out to the string aliased.

Notes: Aliases are not case sensitive. Only alphanumeric characters are allowed in
alias names.

### Parenthesis: ###

()

Example: ('dog' IN titles OR 'cat' IN titles) AND 'pet' IN titles

Terms: None

Description: Wrapping tokens in parenthesis lets you use flow control to 
manipulate order of operations. In the parse tree anything in parenthesis is
evaluated recursively as though it were a top level search query statement.

Notes: None

### NOT: ###

NOT

Example: NOT FALSE

(Would evaluate to TRUE.)

Terms: No left term, negates the value of the immediate right term.

Description: Negates an expression or value, TRUE becomes FALSE and FALSE
becomes TRUE. Can be used with parenthesis to negate large amounts of boolean
logic.

Notes: Negates the *most immediate* right term, so if you write:

NOT 0 OR 5

The NOT 0 will be evaluated before the 0 OR 5.

In this case, since anything not-zero is TRUE the evaluation of NOT 0
would be TRUE.

### Comparison operators: ###

< > <= >= = IN

Example: browser.table.date > browser.table.date

Terms: All comparison operators have a left term and a right term, the exact
mechanics of each is described below.

Description: Compares two values or expressions according to a logical operation.

Notes: This entry has sub-entries that start below.

#### Less than: ####

<

Example: 2 < 5

(Evaluates to TRUE.)

Terms: Evaluates to TRUE if left term is lesser than right term. FALSE otherwise.

Description: IBID.

Notes: None.

#### Greater than: ####

>

Example: 5 > 2

(Evaluates to TRUE.)

Terms: Evaluates to TRUE if left term is greater than right term. False otherwise.

Description: IBID

Notes: None.

#### Less than or equal to: ####

<= 

Example: 5 <= 5

(Evaluates to TRUE.)

Terms: Evaluates to TRUE if left term is less than or equal to right term.
False otherwise.

Description: Syntactic sugar for '5 < browser.table.column OR 5 = broswer.table.column'.

Notes: None.

#### Greater than or equal to: ####

>=

Example: 5 >= 5

(Evalutes to TRUE.)

Terms: Evaluates to TRUE if left term is greater than or equal to right term.
False otherwise.

Description: Syntactic sugar for '5 > browser.table.column OR 5 = browser.table.column'.

Notes: None.

#### Equals: ####

=

Example: 5 = 5

(Evaluates to TRUE.)

Terms: Evaluates to TRUE if left term and right term are the same. FALSE
otherwise.

Description: IBID.

Notes: None.

#### IN: ####

IN

Example: 'dog' in titles

(Evaluates to TRUE if dog is in the data for 'titles' in current row.)

Terms: Evaluates to TRUE if left term is 'in' the right term. FALSE otherwise.

Description: IBID. Exact details on what counts as 'in' are in the notes below:

Notes: The left term is 'in' the right term if:

For strings, the characters in the left term string are in the right term string.

For integers and numbers, the left number 'goes into' the right number as in
division. More prescisely if L mod R is L then it evaluates to FALSE. 

### AND: ###

AND

Example: 5 AND FALSE

(Evaluates to FALSE.)

Terms: Evaluates to TRUE if left term evaluates to TRUE and right term evaluates 
to TRUE.

Description: IBID.

Notes: None.

### OR: ###

OR

Example: 5 OR FALSE

(Evaluates to TRUE.)

Terms: Evaluates to TRUE if left term evaluates to TRUE or right term evaluates
to TRUE.

Description: IBID.

Notes: None.

