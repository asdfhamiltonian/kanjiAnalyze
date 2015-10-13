# kanjiAnalyze

This python script analyzes several japanese text for the grade, JLPT, and frequency rank of the kanji they use. The first part of this script compiles and pickles a dictionary of Kanji characters with an assigned grade level from the Kanjidic cml file. The script can then reuse this pickled file later if needed.

After this, the script analyzes several texts including a wikipedia article, "I am Cat" by Natsume Soseki, "Oku no Hosomichi" by Matsuo Basho and a list of characters for names,

The average grade level of these different text samples was pretty narrowly in the range 3 - 4 (except for the list of characters for names). I thought there would be a much wider range in the average grade level, but there was definitely a higher standard deviation of character difficulty in the novels compared to the wikipedia articles. Matsu Basho's text (written in the late 1600s) had the highest grade level, which might be due to use of older, more difficult to understand characters.
