from autobean_refactor import models, parser

p = parser.Parser()

# Most commonly, you'll want to parse a file
file = p.parse('2000-01-01 open Assets:Foo\n2000-01-02 close Assets:Foo', models.File)

# You can parse into other models as well
close = p.parse('2000-01-02 close Assets:Foo', models.Close)

# Token needs to be parsed with `parse_token` instead.
comment = p.parse_token('; comment', models.BlockComment)
string1 = p.parse_token(r'"foo\n"', models.EscapedString)
string2 = p.parse_token('"foo\n"', models.EscapedString)
number = p.parse_token('1,234.56', models.Number)
