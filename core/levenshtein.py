
def distance(a,b):
    if not a:return len(b)
    if not b:return len(a)
    if a[-1]==b[-1]:
        return distance(a[:-1],b[:-1])
    return 1+min(
        distance(a[:-1],b),
        distance(a,b[:-1]),
        distance(a[:-1],b[:-1])
    )
