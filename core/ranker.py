
import heapq

class Ranker:
    def __init__(self,freq):
        self.freq=freq

    def top_k(self,words,k=5):
        heap=[]
        for w in words:
            heapq.heappush(heap,(-self.freq.get(w),w))
        return [heapq.heappop(heap)[1] for _ in range(min(k,len(heap)))]
