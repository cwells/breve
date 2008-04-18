'''
soup2breve - Robert Leftwich

Requires BeautifulSoup - http://www.crummy.com/software/BeautifulSoup/
'''

import sys
import htmlentitydefs

from BeautifulSoup import BeautifulSoup, Tag, NavigableString, Comment

DEFAULT_ENCODING = 'utf-8'
INDENT = '   '
GUARD = '|||'

# flags to return from handlers
NOT_HANDLED = 0           # handler did nothing
CONTENT_NOT_HANDLED = 1   # handler only handled the tag, not the contents
CONTENT_HANDLED = 2       # handler handled everything

# a dictionary to translate unicode into HTML entities
codepoint2entity = dict([(c, u'%s[E.%s]%s' % (GUARD, n, GUARD)) for c,n in htmlentitydefs.codepoint2name.iteritems()])

# our own version of the beautiful soup parser
class BreveBeautifulSoup(BeautifulSoup):

    # define a dict for translate() that removes only *ascii* whitespace, not unicode whitespace.
    # (of course if you authored the original document in unicode and added genuine unicode whitespace
    # there is no way for this class to know that, but that is far less likely than the html entity 
    # to unicode conversion process occurring).
    # Remove TAB, LF, FF, CR, SPACE
    ASCII_STRIP = { 9: None, 10: None, 12: None, 13: None, 32: None, }

    # override the way the data is checked for whitespace to handle the case
    # where the data is in unicode and it has entites in it, such as nbsp
    def endData(self, containerClass=NavigableString):
        if self.currentData:
            currentData = ''.join(self.currentData)
            # replaced strip() with translate() - as we are looking
            # for empty strings that only contain ascii whitespace
            if len(currentData) > 0 and not currentData.translate(self.ASCII_STRIP):
                if '\n' in currentData:
                    # replace this with \n to preserve newlines
                    currentData = '\n'
                else:
                    currentData = ' '
            self.currentData = []
            if self.parseOnlyThese and len(self.tagStack) <= 1 and \
                   (not self.parseOnlyThese.text or \
                    not self.parseOnlyThese.search(currentData)):
                return
            o = containerClass(currentData)
            o.setup(self.currentTag, self.previous)
            if self.previous:
                self.previous.next = o
            self.previous = o
            self.currentTag.contents.append(o)

# helper for building the current indent string
def current_indent(indent):
    return INDENT*indent

# escape a quote if it si the last character in buffer,
# so triple quoted strings don't barf
def escape_last_quote(s):
    if s.endswith("'"):
        s = s[-1] + "\'"
    return s

# the real thing - convert an html tag to a breve equivalent
def convert(tag, output, indent=0, handlers=None):
    curr_indent_str = current_indent(indent)
    if isinstance(tag, NavigableString):
        s = tag.string
        # don't need substitutions in comments
        if not isinstance(tag, Comment):
            s = s.translate(codepoint2entity)

        # anything to output?
        if s:
            if isinstance(tag, Comment):
                output.append("%scomment(\n%s'''%s'''),\n" %(curr_indent_str, curr_indent_str, escape_last_quote(s)))
            else:
                # handle any entities
                guarded_strings = s.split(GUARD)
                for s in guarded_strings:
                    if s:
                        # is this a substituted entity?
                        if s[0] == '[' and s[-1] == ']':
                            s = s[1:-1]
                            output.append("%s%s,\n" %(curr_indent_str, s))
                        else:
                            output.append("%s'''%s''',\n" %(curr_indent_str, escape_last_quote(s)))
    else:
        if hasattr(tag, 'name'):
            # is there are a handler for this tag?
            tag_handled = NOT_HANDLED
            if handlers and handlers.has_key(tag.name):
                tag_handled = handlers[tag.name](tag, output, indent, handlers)

            # do we still need to handle the tag?
            if tag_handled == NOT_HANDLED:
                output.append('%s%s' %(curr_indent_str, tag.name))
                if hasattr(tag, 'attrs') and tag.attrs:
                    output.append(' ( ')
                    i = 0
                    for key, val in tag.attrs:
                        if i:
                            output.append(', ')
                        output.append('%s_="%s"' %(key, val))
                        i+= 1
                    output.append(' )')

            # do we need to handle any content?
            if tag_handled != CONTENT_HANDLED:
                if hasattr(tag, 'contents'):
                    if not tag.isSelfClosing:
                        if len(tag.contents) > 0:
                            output.append(' [\n')
                            l = len(tag)
                            for t in tag:
                                # if not the only tag and it is a newline
                                # then ignore it - this gets rid of the newline before/after tags
                                if l > 1 and (t=='\n' or t==' '):
                                    continue
                                # otherwise convert it
                                convert(t, output, indent+1, handlers=handlers)
                            output.append('%s]' %(curr_indent_str))
                    if indent:
                        output.append(',\n')

# ----- Tag handlers -----

# throw the tag and all its contents away
def null_handler(tag, output, indent, handlers):
    # throw out the tag
    return CONTENT_HANDLED

# ignore the tag, but process its contents
def content_handler(tag, output, indent, handlers):
    return CONTENT_NOT_HANDLED

# special handling for the http-equiv tag
def meta_handler(tag, output, indent, handlers):
    if tag.get('http-equiv', None):
        a = []
        for key, val in tag.attrs:
            # handle BeautifulSoup encoding substitution
            if "%SOUP-ENCODING%" in val:
                val = val.replace("%SOUP-ENCODING%", DEFAULT_ENCODING)
            a.append('"%s_":"%s"' %(key, val))
        output.append('%smeta ( **{ %s } ),\n' %(current_indent(indent), ', '.join(a)))
        return CONTENT_HANDLED
    else:
        return NOT_HANDLED

# -----

# convert the specified file using the supplied tag handlers
def convert_file(filename, handlers):
    soup = BreveBeautifulSoup(file ( filename, 'rU' ),
                              convertEntities=BeautifulSoup.HTML_ENTITIES)
    output = []
    convert(soup.html, output, handlers=handlers)
    return output

def usage ( ):
    print '''
        Usage:
            %s <htmlfile>
    ''' % sys.argv [ 0 ]
    
if __name__ == '__main__':
    if len ( sys.argv ) < 2:
        usage ( )
        raise SystemExit

    result = convert_file(sys.argv [ 1 ], dict(meta=meta_handler))
    print ''.join(result)
