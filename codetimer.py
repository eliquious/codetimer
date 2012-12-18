from time import clock
from collections import namedtuple

class Stats(object):
    """docstring for Stat"""
    def __init__(self):
        super(Stats, self).__init__()
        self.count , self.sum, self.min, self.max, self.mean, self.m2, self.stdev = 0, 0, 2**32, 0, 0, 0, 0

    def __iadd__(self, duration):
        self.count += 1
        self.sum += duration
        delta = duration - self.mean
        self.mean += delta / self.count
        self.m2 += delta**2
        if self.count > 1:
            self.stdev = self.m2 / (self.count - 1)
        if duration < self.min:
            self.min = duration
        elif duration > self.max:
            self.max = duration
        return self

    def __str__(self):
        return "<Stats: count: %i; min: %0.9fs; max: %0.9fs; sum: %0.9fs; mean: %0.9fs; stdev: %0.9fs>" % \
            (self.count, self.min, self.max, self.sum, self.mean, self.stdev)

class CodeTimer(object):
    """docstring for CodeTimer"""
    def __init__(self, callable, num=1, args=[], kwargs={}, record=False):
        super(CodeTimer, self).__init__()

        if not hasattr(callable, "__call__"):
            raise Exception("First argument must be callable.")
        if num < 1:
            raise Exception("Number of runs must be positive.")

        self.callable = callable
        self.number = num
        self.args = args
        self.kwargs = kwargs
        self.record = record
        self.times = []
        self.stats = Stats()

    def run(self):
        for i in xrange(self.number):
            start = clock()
            self.callable(*self.args, **self.kwargs)
            duration = clock() - start
            self.stats += duration
            if self.record:
                self.times.append(duration)
        return self

    def __str__(self):
        return "<%s - %s>" % (self.callable.func_name, str(self.stats))

if __name__ == '__main__':

    def append(l, n):
        for x in xrange(n):
            l.append(n)

    print CodeTimer(append, args=[[], 5], num=10).run()
    print "Done."
