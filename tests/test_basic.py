
from core.trie import Trie

t=Trie()
t.insert('sanchai')

assert t.search('sanchai')
assert t.starts_with('san')
print('Tests passed')
