# Libra

> Documenting my progress and explaining my work.

### Models
Along with the `Book`, `Member`, and `Loan` models, I added one more model: `Genre`. Since we needed to keep track of books under a genre, I simplified this process by using another class.

Default functions were provided to generate default genres, members, and books to populate the initial library. These default values were named "No Title", "No Author", "No Genre", etc.

In the `Loan` class, we threw a ValidationError if there existed a previous loan that was within 14 days of the current loan. I used `timedelta` and other `datetime` functions to build this checking function. If it didn't throw an exception, the loan would be saved. If not, a  `ValidationError` that said "Previous loan has not ended." would be thrown and the loan would not be saved.


### Views
All appropriate connections were made in the views. 

The Loan Form only saved the submission into a loan if the form was given valid arguments (i.e. start of loan is at least 14 days from the previous loan of that same book). 

All views were linked to their respective .html files. 


### Styling
I utilized Bootstrap for my styling. 

I created a toggle navigation bar (the square/rectangle) that linked to multiple useful pages. 

### Other things

Testing and Debugging: I created a superuser to create a few books, members, and genres to test out the loan form. I tested whether the form would appropriately throw an error if within 14 days from the previous loan of the same book, whether it would redirect to the loan detail page after creating the loan, etc. During this time, I also figured out potential edge test cases (e.g. making a loan, then making a second loan that had a start date that was beyond 14 days BEFORE is still valid.)
