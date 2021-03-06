from HTMLParser import HTMLParser


class HTMLPassThrough(HTMLParser):
    """Maintains a stack of tags and returns the same HTML it parses - base
       class for more interesting parsers in markup.py.
    """
    def reset(self):
        HTMLParser.reset(self)
        self.stack = []
        self.out = []

    def emit(self, data):
        self.out.append(data)

    def close(self):
        HTMLParser.close(self)
        return ''.join(self.out)

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1] == tag
        self.stack.pop()
        self.out.append('</%s>' % tag)

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        if attrs:
            self.out.append("<%s %s>" % (tag, ' '.join('%s="%s"' % (k, v) for k, v in attrs)))
        else:
            self.out.append("<%s>" % tag)

    def handle_data(self, data):
        self.out.append(data)

    def handle_entityref(self, name):
        self.out.append('&%s;' % name)

    def handle_charref(self, name):
        return self.handle_entityref('#' + name)
