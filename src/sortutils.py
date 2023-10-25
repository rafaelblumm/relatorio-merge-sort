import time
import random
import pathlib
import numpy as np
import matplotlib.pyplot as plt

RESOURCES = pathlib.Path(__file__).parent.parent / "resources"

def _generate_sample(lst, file_suffix):
    # Ordem crescente
    lst.sort()
    with (RESOURCES / f"ascending-order-{file_suffix}.txt").open("w") as f:
        f.writelines(lst)

    # Ordem decrescente
    lst.reverse()
    with (RESOURCES / f"descending-order-{file_suffix}.txt").open("w") as f:
        f.writelines(lst)

    # Ordem aleatória
    random.shuffle(lst)
    with (RESOURCES / f"random-order-{file_suffix}.txt").open("w") as f:
        f.writelines(lst)

def generate_sample_int(qnt):
    ''' Gera amostras de dados aleatórios numéricos.
    '''
    lst = []
    for i in np.random.rand(qnt).tolist():
        lst.append(f"{(int(i * pow(10, 13)))}\n")
    _generate_sample(np.unique(lst).tolist(), qnt)

def generate_sample_str(file_suffix):
    ''' Gera amostras de dados a partir de dicionário de palavras.
    '''
    with (RESOURCES / f"ascending-order-{file_suffix}.txt").open("r") as f:
        _generate_sample(f.readlines(), file_suffix)

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

def _list_from_file(filename, is_numeric_val):
    with open(RESOURCES / filename, "r") as f:
        lst = f.readlines()
    if is_numeric_val:
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

def benchmark_merge_sort(name, is_numeric_val=False):
    res = []
    for f in get_data_filenames(name):
        res.append(_benchmark(_list_from_file(f, is_numeric_val)))
    return tuple(res)

def _truncate_float(num):
    mult = 10 ** 3
    return int(num * mult) / mult

def _calculate_plot_height(benchmarks):
    arr = []
    for v in benchmarks.values():
        arr.extend(list(v))
    return max(arr)

def plot(benchmarks, title_suffix):
    sort_order = ("Crescente", "Aleatório", "Decrescente")

    x = np.arange(len(sort_order))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in benchmarks.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Tempo (segundos)')
    ax.set_title(f"Benchmark merge-sort ({title_suffix})")
    ax.set_xticks(x + width, sort_order)
    ax.legend(loc='upper left', ncols=3)
    h = _calculate_plot_height(benchmarks)
    ax.set_ylim(0, h + 0.2 * h)
    
    plt.show()
