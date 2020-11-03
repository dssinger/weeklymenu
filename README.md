Create an HTML version of a week's menu as exported from Paprika

Requirements:

* Python 3
* icalevents (pip install icalevents)
* An Apple icloud public calendar whose URL is in the file 'calendar.url'
* Paprika 3

How to use it:

1. Create the week's menu in Paprika
2. Export the menu to the calendar
3. Run the makemenu script
4. Print the resulting HTML file.

Notes:

Menu items beginning with 'Defrost ', 'defrost ', 'Marinate ', or 'marinate ' will be printed on separate lines.  Paprika export does not distinguish between menu items, so put these last.


