from multiprocessing import Manager, Pool, cpu_count
from quickSort import quick_sort
from timer import Timer
from parallelQuickSort import perform_parallel_quick_sort
import random

if __name__ == '__main__':
    # number of cpu cores
    processor_count = cpu_count()

    # timer
    main_timer = Timer('single_core', "multiple_core")

    # length of the input list
    length = 100000

    # generates list and shuffles them
    input_list = [x for x in range(length)]
    random.shuffle(input_list)
    # copies the input list for single core evaluation
    single_core_input_list = input_list[:]

    # Start timing the single-core procedure
    main_timer.start_for('single_core')

    # do serial quick sort
    quick_sort(0, length - 1, single_core_input_list)

    # stops timing the single-core procedure
    main_timer.stop_for('single_core')

    # prints all the data from the serial quick sort
    print("Verification of quick sort: ", single_core_input_list == sorted(input_list))
    print(f"Single Core elapsed time: {round(main_timer['single_core'], 10)}")

    # main_timer.start_for('multiple_cores')
    print("Starting parallel quick sort")

    main_timer.start_for("multiple_core")
    # debug_list = [7, 4, 8, 5, 3, 9, 2, 0, 1, 6, 10, 11]
    perform_parallel_quick_sort(input_list, processor_count)
    main_timer.stop_for("multiple_core")
    print(f"Multiple Core elapsed time: {round(main_timer['multiple_core'], 10)}")