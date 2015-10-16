# kanjiAnalyze

This python script calculates stats for the grade, JLPT, and frequency rank kanji characters used in Japanese text. The first part of this script compiles and pickles a kanji dictionary of characters with a known grade level from the kanjidic xml file. The script can then reuse this pickled file later if needed.

Next, the script analyzes several texts including wikipedia articles, "I am Cat" by Natsume Soseki, "Oku no Hosomichi" by Matsuo Basho and a list of kanji characters used in names.

The average grade level of these different text samples ranged from 3 - 4 (except for the list of characters for names). I thought there would be a much wider range in the average grade level, but there was definitely a higher standard deviation of character difficulty in the novels compared to the wikipedia articles. Matsu Basho's text (written in the late 1600s) had the highest grade level, which might be because he used older, more difficult to understand characters.
