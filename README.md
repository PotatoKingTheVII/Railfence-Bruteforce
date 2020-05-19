## Intro
Python implementation of railfence with offset included and bruteforce option.

The Bruteforce is done by ordering all combinations with a chi-squared statistic of their bigram frequencies compared to the expected English results. This is a basic approach and works best with a decently sized cipher-text.


## File usage
RailfenceEncDec provides two functions, encryptrail and decryptrail which take (textinput, rail, offset) and return the resulting string. RailforceBrute takes an input at the top of the file for "ciphert" and calculates all valid railfence settings for it (Pretty sure this is roughly O(n^2) so larger inputs will take a while) dumping them to "RawCombos.txt" firstly and then "OrderedList.csv" later.

## Credit
Original bigram frequencies from http://practicalcryptography.com/media/cryptanalysis/files/english_bigrams_1.txt

## Dependancies
 - numpy
