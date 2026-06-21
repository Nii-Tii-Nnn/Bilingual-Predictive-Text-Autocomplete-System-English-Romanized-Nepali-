
import heapq

class Ranker:
    """
    Ranks suggestions by frequency using heap-based Top-K algorithm.
    Higher frequency words appear first.
    """
    def __init__(self, freq_engine):
        self.freq_engine = freq_engine

    def top_k(self, words, k=5):
        """
        Return top k words ranked by frequency (descending).
        Words not in frequency dictionary get frequency 0.
        """
        heap = []
        for w in words:
            freq_score = self.freq_engine.get(w)
            # Use negative frequency for max heap (heapq is min heap by default)
            heapq.heappush(heap, (-freq_score, w))
        
        result = []
        for _ in range(min(k, len(heap))):
            result.append(heapq.heappop(heap)[1])
        return result
