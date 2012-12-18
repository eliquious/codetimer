
CodeTimer
=========

A small but versatile timer for python code snippets. Unlike Python's built-in ``timer`` module, ``codetimer`` allows you to time callables and setup different args/kwargs for each timer instance. CodeTimer also performs summary statistics on each code block.

Example
-------

.. code-block:: python

    from codetimer import CodeTimer

    if __name__ == '__main__':

        def append(n):
            l = []
            for x in xrange(n):
                l.append(x)

        timer = CodeTimer(append, num=10, args=[1000]).run()

        # <append - <Stats: count: 1000; min: 0.000004749s; max: 0.000010616s; sum: 0.005611607s; mean: 0.000005612s; stdev: 0.000000000s>>
        print timer
