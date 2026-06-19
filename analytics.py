
class Analytics:
    def __init__(self,freq):
        self.freq=freq

    def report(self):
        total=len(self.freq.frequency)
        return {
            "total_words":total,
            "top_words":sorted(
                self.freq.frequency.items(),
                key=lambda x:x[1],
                reverse=True
            )[:10]
        }
