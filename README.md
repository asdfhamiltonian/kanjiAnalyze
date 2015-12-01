# kanjiAnalyze

This python script analyzes several Japanese texts for the grade, JLPT level, and frequency rank of the kanji they use. The first part of this script builds and pickles a dictionary of Kanji characters from an XML data set (EDRDG's Kanjidic XML file). The XML file includes information about the grade, JLPT level, and frequency of use for each character. The script can then reuse this pickled file later if needed.

Next, the script analyzes several Japanse texts including two wikipedia articles, "I am Cat" by Natsume Soseki, "Oku no Hosomichi" by Matsuo Basho and a list of characters for names,

The average grade level of these different text samples was pretty narrowly in the range 3 - 4 (except for the list of characters for names). I had expected there to be a much wider range in the average grade level, but I did find a higher standard deviation of character difficulty in the novels compared to the Wikipedia articles. Matsu Basho's text (written in the late 1600s) had the highest grade level, which may have been due to his use of older, more difficult to understand characters.

This package uses the KANJIDIC dictionary file. This file is the property of the Electronic Dictionary Research and Development Group, and is used in conformance with the Group's licence. (see http://www.csse.monash.edu.au/~jwb/kanjidic.html)