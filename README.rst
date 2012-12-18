
CodeTimer
=========

A small but versatile timer for python code snippets. Unlike Python's built-in ``timer`` module, ``codetimer`` allows you to time callables and setup different args/kwargs for each timer instance. CodeTimer also performs summary statistics on each code block.

For Windows machines, the statistics use ``time.clock()``, all other machines use ``time.time()``. The statistics can be retrieved using the ``get_stats()`` function. CodeTimer also has a ``record`` option to pass the constructor which records all the times for each run. These times can begotten by using the ``get_times()`` method.

Example
-------

.. code-block:: python

    from codetimer import CodeTimer

    if __name__ == '__main__':

        # define the function (any callable will do)
        def append(n, mult=1):
            l = []
            for x in xrange(n):
                l.append(n*mult)

        # setup CodeTimer with args and kwargs
        # 'num' defines the number of executions
        # then call 'run()'
        # outputs: "<append - <Stats: count: 10; min: 16 ms; max: 21 ms; sum: 196 ms; mean: 20 ms; stdev: 55 us;>>"
        print CodeTimer(append, args=[100000], num=10, kwargs={"mult":5}).run()

        # You can also specify the precision of the output
        # outputs: "<append - <Stats: count: 10; min: 0.016s; max: 0.017s; sum: 0.161s: mean: 0.016s; stdev: 0.000s;>>"
        print CodeTimer(append, args=[100000], num=10, precision=3).run()

