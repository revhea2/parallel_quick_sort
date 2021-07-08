from multiprocessing import Manager, Pool, cpu_count
from quickSort import quick_sort
from timer import Timer
from parallelQuickSort import perform_parallel_quick_sort
import random

if __name__ == '__main__':
    # number of cpu cores
    processor_count = cpu_count()

    print("Cpu count: ", processor_count)

    # timer
    main_timer = Timer("multiple_core")

    # length of the input list
    length = 12

    # generates list and shuffles them
    input_list = [x for x in range(length)]
    random.shuffle(input_list)

    print("Starting parallel quick sort")

    main_timer.start_for("multiple_core")
    debug_list = [7, 4, 8, 5, 3, 9, 2, 0, 1, 6, 10, 11]

    perform_parallel_quick_sort(debug_list, processor_count)

    main_timer.stop_for("multiple_core")
    print(f"Multiple Core elapsed time: {round(main_timer['multiple_core'], 10)}")
