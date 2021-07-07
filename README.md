# SO2DataManager
Program developed during my research work in the air lab at LCSC

This program is the newest iteration of the Sulfur Stats Calculator I had created last year.
I have now included almost an entire overhaule of the functionality by replacing most of the commands
with buttons with the same functionality. This will allow for the user to simply press a button in order to
run the processes on a merged file rather than remember all the terminal command prompts.

CONTROLS:
1. The Open button allows the user to select a .txt or .csv file to display in the white space to the right of the buttons
2. The Save button allows the user to save what contents are displayed to the right.
3. The Readme button will display this file to the right
4. The merge button will prompt the user with 3 areas to enter text. The first one is for the first file to be merged is entered,
with it starting earlier than the second file. The second input is then the second file to combine together, with the last input
for the name of the newly merged file. One just has to hit the "Submit" button to merge the file after which you may close with the quit button.
5. Run All will run through the next 5 button's actions one after another with prompts for the text file to run calculations on,
the calculation setting, and the start date/time and end date/time should the user choose the Slice or Custom setting for calculations.
If a setting you chose to calculate is not what you want, simply click the clear stat button to clear the text from the calc setting form. When all settings are
to your specifications, hit Run and the program will compute all the stat processes on the file.
6. Label calibrations prompts the user to enter a .txt file and then creates a column with each row labeled as a calibration or sample when
confirm is hit. The result file will share the same name as the .txt file, but have the .csv extension instead.
7. Mark Holds prompts the user to enter a .csv file to create a column indicating if the SO2 or TRS concentrations are held values or not. Please be sure to use a .csv file
that has the calibrations from the previous step already part of it.
8. Format button asks for a .csv file and then formats the file so that it can be used in the stat calculation part of the program
9. Calculate prompts the user with the .csv file and then allows the user to hit a button at the bottom to determine which stat calulation will be done on the data.
If it happens to be Slice or Custom, a StartTime and StartDate and an EndTime and EndDate need to be specified. Otherwise they may remain on the default if hourly or daily
calculations are run. The stats option form can be cleared by pressing clear stat, should the user change their mind on what calculation to run. Please be sure
to select the file with the "modified" added to the filename, as this is the version that is properly formatted to run through this function.
10. The delete button allows the user to select a file to delete, once done, it will display the location of the file that was deleted.
11. The quit button allows the user to quit the program.

OPERATION:

There are 2 effective ways to run the program based on the condition of the data.

1: The data is at the beginning and either is all merged, or needs to be merged together into 1 text file.
2: The data is somewhere in the middle with a .csv file that needs to pick up from where it last ran.

Method 1.
1. If the file is merged alrady go to step 2, otherwise continue to 1a.
1a. Select the Merge button
1b. Enter the first file to merge
1c. Enter the second file to merge
1d. Enter a name for the file with both contents merged together
1e. Repeat steps 1b-1c until all files are merged into 1 text file.
1d. Hit Quit in the file merger window not the red button quit.
2. Select "Run All"
3. Enter the Name of the merged .txt file
4. Select the desired calc setting from the buttons: Daily, Hourly, Slice or Custon
4a. If Slice or Custom was selected Enter values for the Start Date&Time and End Date&Time
5. Hit the run button
6. The finished result file will include text in the name based on the calculation type selected.

Method 2.
1. Open the file
2. Based on either the extension or the last column in the file determin which step needs to be run next.
2a. If it is a text file, then either do merges until fully merged or simply hit run all
2b. If the last column in the file is Calibrations, then hit the Mark Holds button and enter the name of the .csv file name
2c. If the last column in the file is TRS Hold AND there are commas separating each column, hit the format button and enter the .csv file name
2d. If the last column in the file is TRS Hold and the columns and the file includes the word "modified" at the end of the filename then hit the Calculate button
and enter the name of the .csv file and choose the desired calculation setting to run.
2e. If the file ends in: Daily, hourly, custom, or slice then the file is a results file and does not need to be run through the program.
