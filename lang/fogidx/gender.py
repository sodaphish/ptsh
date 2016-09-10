'''Guess author gender

Implements the Koppel-Argamon algorithm for guessing
an author gender.  The algorithm was invented by Moshe Koppel
(Bar-Ilan University, Israel) and Shlomo Argamon (Illinois Institute
of Technology). The current version uses the algorithm described at:

http://www.nytimes.com/2003/08/10/magazine/10wwln-test.html

See Also:

McGrath, Charles.  "Sexed Texts."  I<New York Times Magazine>, August
10, 2003.  http://www.nytimes.com/2003/08/10/magazine/10WWLN.html

Ball, Philip.  "Computer program detects author gender."  I<Nature>,
July 18, 2003.  http://www.nature.com/nsu/030714/030714-13.html

For each appearance of the following words, add the points indicated:

  "the"                    17
  "a"                       6
  "some"                    6
  number, written or digits 5
  "it"                      2
  "with"                  -14

  possessives,
    ending in "s"          -5
    pronouns               -3

  "for"                    -4
  "not"                    -4
  word ending with "n\'t"    4
 
If the total score is greater than the total number of words, the
author is probably a male.  Otherwise, the author is probably a
female.  The original authors estimate the system is 80% accurate.

This implementations follows on the perl version available at:
http://www.eekim.com/software/Lingua-EN-Gender/, with the following
copyright notice:

  Eugene Eric Kim, E<lt>eekim@blueoxen.orgE<gt>
  Copyright (c) Blue Oxen Associates 2003.  All rights reserved.
  This library is free software; you can redistribute it and/or modify
  it under the same terms as Perl itself.

So, naturally, the Python version is:
Written by Elf M. Sternberg (elf@drizzle.com)
(c) Copyright Elf M. Sternberg.

This library is free software; you can redistribute it and/or modify
it under the same terms as Python itself.

Usage, Example 1:
import gender
print gender.gender( someText )

Usage, Example 2:
import gender

G = gender.Gender()
G.addText( someText )
print G.gender()
G.addText( someMoreText )
print G.gender()

Usage, Example 3 (from the shell):
cat someText.txt | python gender.py
'''

import string
import exceptions

_wordScores = { "the" : 17, "a" : 6, "some" : 6, "it" : 2, "with" : -14, 
                "for" : -4, "not" : -4, "mine" : -3, "yours" : -3, 
                "his" : -3, "hers" : -3, "its" : -3, "ours" : -3 }

_numbers = dict( map( lambda a: (a, 1), [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
    'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
    'twenty', 'thirty', 'forty', 'fourty', 'fifty', 'sixty',
    'seventy', 'eighty', 'ninety', 'hundred', 'thousand', 'million',
    'billion', 'trillion'] ) )


class Gender:

    def __init__( self, text = '' ):
        '''Construct a Gender object ready to perform analysis.  Requires
        a complete copy of the text.'''

        self.text = text
        self.words = wordSplit( self.text )
        self.score = None

    # Note that adding more text invalidates your score.

    def addText( self, text ):
        '''Analyze a new text document.
        '''
        self.text = self.text + ' ' + text
        self.words = wordSplit( self.text )
        self.score = None
        return self


    def getWords( self ):
        '''Returns the array of words split out of
        the document in the order in which they appear.
        '''
        return self.words


    def getCount( self ):
        '''Returns the count of words in the document.
        '''
        return len( self.words )


    def getScore( self ):
        '''Returns the score if it has already been calculated, or
        calculates the score and returns the value.
        '''
        if self.score:
            return self.score

        if not len(self.words):
            raise exceptions.RuntimeError, "No text supplied to score."
        
        score = 0
        lastSawNumber = 0

        for word in self.words:
            if isANumber( word ) and not lastSawNumber:
                score = score + 5
                lastSawNumber = 1

            elif isPossessive( word ):
                score = score - 5
                lastSawNumber = 0
        
            elif isNT( word ):
                score = score - 4
                lastSawNumber = 0

            else:
                score = score + _wordScores.get( word, 0 )
                lastSawNumber = 0

        self.score = score
        return self.score


    def getGender( self ):
        '''Returns the gender of the author according to the score.'''
        if not self.score:
            self.score = self.getScore()

        igen = cmp( self.getScore(), self.getCount() )
        if igen == 0:
            return 'androgynous'

        if igen == 1:
            return 'male'

        return 'female'



def wordSplit( text ):
    okay = string.digits + string.letters + "'"
    words = []
    word = ''
    for i in text:
        if i not in okay:
            if word:
                words.append( word )
                word = ''
            continue
        word = word + string.lower( i )

    return map( lambda a: a[0] == "'" and a[1:] or a, map( lambda a: a[-1] == "'" and a[0:-1] or a, words ) )


def isANumber( word ):
    if word.isdigit():
        return 1

    return _numbers.get( word, 0 )

def isPossessive( word ):
    if word == "it's":
        return 0

    if len( word ) < 2:
        return 0

    if word[-2:] == "'s'":
        return 1

    return 0


def isNT( word ):
    if len( word ) < 3:
        return 0

    if word[-3:] == "n't":
        return 1

    return 0


def gender( text ):
    '''A very simplified function that takes a copy of your text and
    returns the best-guess gender of the author.
    '''
    cGender = Gender( text )
    return cGender.getGender()


if __name__ == '__main__':
    import sys
    if not sys.argv[1:]:
        input = sys.stdin
    else:
        input = open(sys.argv[1], 'r')

    print gender(input.read())
