from multiprocessing import Manager, Pool, cpu_count
from contextlib import contextmanager

from quickSort import quick_sort
from timer import Timer


class LowHigh:
    def __init__(self, low_list=[], high_list=[]):
        self.low_list = low_list
        self.high_list = high_list

    def reset(self):
        self.low_list = []
        self.high_list = []

    def __repr__(self):
        strs = "bitches: "
        for l in self.low_list:
            strs += l + " "
        for l in self.high_list:
            strs += l + " "
        return strs


@contextmanager
def process_pool(size):
    """Create a process pool and block until
    all processes have completed."""
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()


def parallel_quick_sort(chunk, results, process_id, pivot):
    low_list = []
    high_list = []

    for number in chunk:
        if number <= pivot:
            low_list.append(number)
        else:
            high_list.append(number)

    results[process_id] = [low_list, high_list]


def swap(results, process_count):
    for n in range(process_count // 2):
        left_process = results[n]
        right_process = results[n + process_count // 2]
        left_process[1], right_process[0] = right_process[0], left_process[1]
        results[n] = left_process
        results[n + process_count // 2] = right_process


def parallel_sort_multiple(results, chunk, process_id, pivot):
    parallel_quick_sort(chunk, results, process_id, pivot)


def merge(results, process_count):
    new_list = []
    for n in range(process_count):
        new_list.append(results[n][0] + results[n][1])

    return new_list


def perform_parallel_quick_sort(array, process_count):
    global_arrangement = []

    if process_count > 1:
        length = len(array)
        # Divide the list in chunks
        step = length // process_count

        # Instantiate a multiprocessing.Manager object to
        # store the output of each process.
        manager = Manager()
        results = manager.dict()

        with process_pool(size=process_count) as pool:

            for n in range(process_count):
                if n < process_count - 1:
                    chunk = array[n * step:(n + 1) * step]
                else:
                    # Get the remaining elements in the list
                    chunk = array[n * step:]

                pool.apply_async(parallel_sort_multiple, (results, chunk, n, array[0]))

        swap(results, process_count)
        new_list = merge(results, process_count)
        print(new_list)

        _perform_parallel_quick_sort(new_list[:process_count // 2], process_count // 2, global_arrangement)
        _perform_parallel_quick_sort(new_list[process_count // 2:], process_count // 2, global_arrangement)

        # print(global_arrangement)


def _perform_parallel_quick_sort(array, process_count, global_arrangement):

    if process_count > 1:

        # Instantiate a multiprocessing.Manager object to
        # store the output of each process.
        manager = Manager()
        results = manager.dict()

        with process_pool(size=process_count) as pool:

            for n in range(process_count):
                if array[n]:
                    pool.apply_async(parallel_sort_multiple, (results, array[n], n, array[0][0]))

        swap(results, process_count)
        new_list = merge(results, process_count)

        print(new_list)

        _perform_parallel_quick_sort(new_list[:process_count // 2], process_count // 2, global_arrangement)
        _perform_parallel_quick_sort(new_list[process_count // 2:], process_count // 2,global_arrangement)

    else:
        arr = array[0]
        quick_sort(0, len(arr) - 1, arr)
        global_arrangement.extend(arr)