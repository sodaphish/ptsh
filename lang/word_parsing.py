import nltk, re, string
from feedparser import parse

def strip_tags(value):
        return re.sub(r'<[^>]*?>', '', value)

def strip_punc(value):
        for c in string.punctuation:
                value = value.replace( c, "" )
        return value


url = "http://feeds.foxnews.com/foxnews/world?format=atom"
feed = parse( url )


for e in feed['entries']:
        words = []
        for w in nltk.word_tokenize( strip_punc( strip_tags( e['title'] ) ) ):
                words.append( w.lower() )
        for w in nltk.word_tokenize( strip_punc( strip_tags( e['summary'] ) ) ):
                words.append( w.lower() )

        words.sort()

        wc = list()
        for word in words:
                wc[word] = wc[word] + 1

        for word in wc:
                print "%s %s" % ( word, wc[word] )


