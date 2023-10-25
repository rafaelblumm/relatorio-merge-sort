import time
import random
import pathlib
import numpy as np
import matplotlib.pyplot as plt

RESOURCES = pathlib.Path(__file__).parent.parent / "resources"

def generate_sample_int(qnt):
    lst = np.random.rand(qnt).tolist()
    for i in range(0, len(lst)):
        lst[i] = str(int(lst[i] * pow(10, 13)))
    lst = np.unique(lst).tolist()

    # Ordem crescente
    with (RESOURCES / f"ascending-order-{qnt}.txt").open("w") as f:
        f.write(str("\n".join(lst)))

    # Ordem decrescente
    lst.reverse()
    with (RESOURCES / f"descending-order-{qnt}.txt").open("w") as f:
        f.write("\n".join(lst))

    # Ordem aleatória
    random.shuffle(lst)
    with (RESOURCES / f"random-order-{qnt}.txt").open("w") as f:
        f.write("\n".join(lst))

def _merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def __merge_sort(arr, l, r):
    if l < r:
        m = l + (r-l)//2

        __merge_sort(arr, l, m)
        __merge_sort(arr, m+1, r)
        _merge(arr, l, m, r)

def _list_from_file(filename, isNumericVal):
    with open(RESOURCES / filename, "r") as f:
        lst = f.readlines()
    if isNumericVal:
        for i in range(0, len(lst)):
            lst[i] = int(lst[i])
    return lst

def get_data_filenames(name):
    return [
        f"ascending-order-{name}.txt",
        f"random-order-{name}.txt",
        f"descending-order-{name}.txt"
    ]

def _benchmark(lst):
    start = time.perf_counter()
    __merge_sort(lst, 0, len(lst) - 1)
    end = time.perf_counter()
    return _truncate_float(end - start)

def benchmark_merge_sort(name, isNumericVal=False):
    res = []
    for f in get_data_filenames(name):
        res.append(_benchmark(_list_from_file(f, isNumericVal)))
    return tuple(res)

def _truncate_float(num):
    mult = 10 ** 3
    return int(num * mult) / mult

def _calculate_plot_height(benchmarks):
    arr = []
    for v in benchmarks.values():
        arr.extend(list(v))
    return max(arr)

def plot(benchmarks):
    sortOrder = ("Crescente", "Aleatório", "Decrescente")

    x = np.arange(len(sortOrder))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in benchmarks.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Tempo (segundos)')
    ax.set_title('Benchmark _merge-sort (int)')
    ax.set_xticks(x + width, sortOrder)
    ax.legend(loc='upper left', ncols=3)
    h = _calculate_plot_height(benchmarks)
    ax.set_ylim(0, h + 0.2 * h)
    
    plt.show()
