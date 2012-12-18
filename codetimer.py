from collections import namedtuple
import sys

if "win" in sys.platform:
    from time import clock
else:
    from time import time as clock

class Stats(object):
    """docstring for Stat"""
    def __init__(self, precision=0):
        super(Stats, self).__init__()
        self.count, self.sum, self.min, self.max, self.mean, self.m2, self.stdev = 0, 0, 2**32, 0, 0, 0, 0
        self.precision = precision
        self.format = "<Stats: count: {count}; min: {min:.{precision}f}s; max: {max:.{precision}f}s; sum: {sum:.{precision}f}s: mean: {mean:.{precision}f}s; stdev: {stdev:.{precision}f}s;>"

    def _format(self):
        if self.precision > 0:
            return self.format.format(**self.__dict__)
        else:
            d = dict(self.__dict__)
            format = "<Stats: count: {:.0f};".format(self.count)
            for attr in ["min", "max", "sum", "mean", "stdev"]:
                value = getattr(self, attr)
                if value > 1:
                    format += " {attr}: {0:.3f} s;".format(value, attr=attr)
                elif value > 0.001:
                    format += " {attr}: {0:.0f} ms;".format(value * 1000, attr=attr)
                elif value > 0.000001:
                    format += " {attr}: {0:.0f} us;".format(value * 1000000, attr=attr)
                elif value > 0.000000001:
                    format += " {attr}: {0:.0f} ns;".format(value * 1000000000, attr=attr)
                else:
                    format += " {attr}: {0:.3f} ns;".format(value * 1000000000, attr=attr)
            format += ">"
            return format

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
        return self._format()

class CodeTimer(object):
    """docstring for CodeTimer"""
    def __init__(self, callable, num=1, args=[], kwargs={}, record=False, precision=0):
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
        self.stats = Stats(precision)

    def set_precision(self, value):
        self.precision = value
        self.stats.precision = value

    def get_times(self):
        return self.times

    def get_stats(self):
        return self.stats

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

    def append(n, mult=1):
        l = []
        for x in xrange(n):
            l.append(n*mult)

    print CodeTimer(append, args=[100000], num=10, kwargs={"mult":5}).run()
    print CodeTimer(append, args=[100000], num=10, precision=3).run()

    print "Done."
