
class TrieNode:
    def __init__(self):
        self.children={}
        self.is_end=False

class Trie:
    def __init__(self):
        self.root=TrieNode()

    def insert(self, word):
        node=self.root
        for c in word.lower():
            node=node.children.setdefault(c, TrieNode())
        node.is_end=True

    def search(self, word):
        node=self.root
        for c in word.lower():
            if c not in node.children:
                return False
            node=node.children[c]
        return node.is_end

    def starts_with(self, prefix):
        node=self.root
        for c in prefix.lower():
            if c not in node.children:
                return False
            node=node.children[c]
        return True

    def _collect(self,node,prefix,out):
        if node.is_end:
            out.append(prefix)
        for c,n in node.children.items():
            self._collect(n,prefix+c,out)

    def get_suggestions(self,prefix):
        node=self.root
        for c in prefix.lower():
            if c not in node.children:
                return []
            node=node.children[c]
        out=[]
        self._collect(node,prefix.lower(),out)
        return out
