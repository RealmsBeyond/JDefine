# JDefine
> Look up definitions for multiple Japanese words at once and save them in tab-delimited format, allowing them to easily be converted into flashcards using your favorite SRS utility (e.g. Anki).

JDefine uses the Weblio dictionary (https://www.weblio.jp) to look up a list of words provided in a text file and extract the definitions into a text file in tab-delimited format, allowing the file to be imported directly into Anki or any other SRS (Spaced Repetition System) application that supports the importation of tab-delimited text files. This program was developed as a tool for language learners who need a quick way to look up lists of Japanese words and generate flashcards for review.

## Running the Program
Simply run the .exe file, or alternatively, run the JDefineMain.py file using a Python interpreter. Make sure whichever file you are running is located in the same directory as the other files.

## How to Use

1) Click the "Select Input File" button. Your input file should:
-Be a .txt document
-Have each vocabulary word on a separate line

2) Click the "Designate Output File" button and either choose an existing file to write to or designate a new file. If an existing file is chosen, the new definitions will automatically be placed beneath any existing text.

3) Click "Retrieve Definitions." Note that definition extraction may take some time depending on the length of the list.

## Usage Notes
Weblio may temporarily block your IP if too many requests are received in a short period of time. This response appears to be triggered at around the 200 - 250 word mark, though this is just a rough estimate, so results may vary. To get around this limitation, I recommend either using a VPN or limiting the number of words you look up per session.

## Built With
This project uses the TKinter and BeautifulSoup libraries along with the urllib and regex modules.

## Known Issues

<li>Nothing appears to be output when the search term contains certain combinations of numbers (e.g. 43423423). It is currently unclear why this occurs, but as it does not affect performance in any meaningful way, I have shelved searching for a solution for now.</li>

## Potential Future Features

<li>Support for more specialized dictionaries (such as a slang dictionary)</li>
<li>Support for additional input formats (.doc, .xml, etc.)</li>
<li>Support for additional output formats (comma-/semicolon-delimited files, etc.)</li>
<li>Add backup dictionaries for use when Weblio blocks requests from one's IP due to too many queries</li>
