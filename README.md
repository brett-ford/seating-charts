# Seats 

In my classroom, there are four large tables instead of individual desks. My students often work in groups. I like to 
change the seating assignments weekly so that, over the course of the school year, students have an opportunity to work 
with everyone and experience the dynamics of many combinations of people working together. 

This project automates the process of creating and maintaining the seating charts. The app accomplishes the following:

1. Reads my students' names from my grade books, which are stored in Google Sheets files, using the Google
Sheets API.
2. Reads the existing seating charts from a Google Sheet that I use to communicate the seating to the students. (Again 
using the Google Sheets API.)
3. Creates new seating charts for the periods requested by the user. (The seats are randomly chosen.) 
4. Updates the existing seating chart, and writes the seating chart to the spreadsheet referenced in step 2.
5. Records the new seating chart in a json file. (See sample.json, a file that shows the storage
format with names of well-known people substituted for my students' names, for confidentiality.)
 
When a student adds or drops my class, this app adjusts automatically. It's also possible to add student pairings that
should or shouldn't work together so that those preferences are taken into account. This is achieved by storing such
pairs in a csv file. (This file is ignored to hide students' names.)

