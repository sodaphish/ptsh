#!/usr/bin/env python
'''
fogidx.py v0.2.0 by C.J. Steele <coreyjsteele@yahoo.com>

Portions of this program are copyright Shlomo Yona (author of
Lingua::EN::Sentences), and Greg Fast (author of Lingua::EN::Syllable), all
other portions are Copyright 2006, Corey J. Steele, all rights reserved.

A program to determine the approximate number of years of formal education
needed to read and comprehend a given text as well as to try to determine the
gender of the text's author.  Reading comprehension levels are determined
according to the Fog Index while gender is determined via the Koppel-Argamon
algorithm.  

Though this is intended to be used mostly for entertainment value, there is
real science behind these things... science that is interesting yet ellusive to
me.

The Fog Index implementation is my own, based on a paper found on-line at
http://www.fpd.finop.umn.edu/groups/ppd/documents/information/writing_tips.cfm

The Koppel-Argamon algorithm is implemented in PyGender, a module by Elf
Sternberg which is available from: http://www.drizzle.com/~elf/code/pygender/
'''

import re, sys
import gender

def countSentences( fulltext ):
	''' 
	The Abbr arrays, below, are mostly ripped from the belly of Perls'
	Lingua::EN::Sentences module, though they were missing a few titles, such
	as: hon., fr., br., and msgr.  As for the logic, it is based very loosly on
	the same perl module, but with a few short-cuts taken because I'm a lazy
	git.
	
	'''
	Abbr = [ 'fr', 'msgr', 'br', 'jr', 'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'sens', 'reps', 'gov', 'attys', 'supt', 'det', 'rev', 'hon' ]
	Abbr += [ 'col','gen', 'lt', 'cmdr', 'adm', 'capt', 'sgt', 'cpl', 'maj' ]
	Abbr += [ 'dept', 'univ', 'assn', 'bros' ]
	Abbr += [ 'inc', 'ltd', 'co', 'corp' ]
	Abbr += [ 'arc', 'al', 'ave', 'blv', 'blvd', 'cl', 'ct', 'cres', 'dr', 'expy', 'dist', 'mt', 'ft', 'fw?y', 'hwy', 'hway', 'la', 'pde', 'pl', 'plz', 'rd', 'st', 'tce', 'Ala' , 'Ariz', 'Ark', 'Cal', 'Calif', 'Col', 'Colo', 'Conn', 'Del', 'Fed' , 'Fla', 'Ga', 'Ida', 'Id', 'Ill', 'Ind', 'Ia', 'Kan', 'Kans', 'Ken', 'Ky' , 'La', 'Me', 'Md', 'Is', 'Mass', 'Mich', 'Minn', 'Miss', 'Mo', 'Mont', 'Neb', 'Nebr' , 'Nev', 'Mex', 'Okla', 'Ok', 'Ore', 'Penna', 'Penn', 'Pa'  , 'Dak', 'Tenn', 'Tex', 'Ut', 'Vt', 'Va', 'Wash', 'Wis', 'Wisc', 'Wy', 'Wyo', 'USAFA', 'Alta' , 'Man', 'Ont', 'Qu', 'Sask', 'Yuk' ]
	Abbr += [ 'jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','sept' ]
	Abbr += [ 'vs', 'etc', 'no', 'esp' ]
	Punc = [ '.', '!', '?' ]
	sentenceCount = 0
	for word in fulltext.split():
		for abr in Abbr: 
			if word.count( "%s." % (abr) ):
				sentenceCount -= 1
		for p in Punc:
			if word.count( p ):
				# don't account for multiples such as "..." or "???" or "!!!"
				sentenceCount += 1
	return sentenceCount


def countSyllables( word ):
	''' 
	this is almost a verbatum rip of Perl's Lingua::EN::Syllable I only cleaned
	it up for use in python.  
	'''
	SubSyl = [ 'cial', 'tia', 'cius', 'cious', 'giu', 'ion', 'iou', 'sia$', '.ely$' ]
	AddSyl = [ 'ia', 'riet', 'dien', 'iu', 'io', 'ii', '[aeiouym]bl$', '[aeiou]{3}', '^mc', 'ism$', '([^aeiouy])\1l$', '[^l]lien', '^coa[dglx].', '[^gq]ua[^auieo]', 'dnt$' ]

	word = word.lower()
	word = word.replace( "'", "" )
	if word.endswith( "e" ):
		word = word[:-1] 
	q = re.compile( '[^aeiouy]+' )
	scrugg = []
	for s in q.split( word ):
		if s:
			scrugg.append( s )
	syl = 0
	for ss in SubSyl:
		p = re.compile( ss )
		if p.search( word ):
			syl -= 1
	for as in AddSyl:
		p = re.compile( as )
		if p.search( word ):
			syl += 1
	if len( word ) == 1:
	    syl += 1 
	syl += len( scrugg )
	if not syl:
		syl = 1
	return syl


totalWordCount = 0
totalSentenceCount = 0
totalComplexWordCount = 0
readingLevel = 0.0
fullText = ""

fd = open( sys.argv[1] )
for line in fd.readlines():
	line = line.strip()
	r = re.compile( '\s' )
	words = []
	for word in r.split( line ):
		totalWordCount += 1
		if countSyllables( word ) >= 3:
			totalComplexWordCount += 1
	fullText += line
fd.close() 

totalSentenceCount = countSentences( fullText )
readingLevel = ( (totalWordCount/totalSentenceCount)+(100*(totalComplexWordCount/totalWordCount)) ) * .4

#print "totalWordCount: %d" % ( totalWordCount )
#print "totalSentenceCount: %d" % ( totalSentenceCount )
#print "totalComplexWordCount: %d" % ( totalComplexWordCount )
print "approximate reading level: %f" % ( readingLevel )
print "author's gender: %s" % ( gender.gender( fullText ) )
