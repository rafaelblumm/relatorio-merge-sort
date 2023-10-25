import time
import random
import pathlib
import numpy as np
import matplotlib.pyplot as plt

RESOURCES = pathlib.Path(__file__).parent.parent / "resources"

def _generate_sample(lst, file_suffix):
    '''
    Gera e grava amostras de dados em ordens crescente, decrescente e aleatória.
    :param lst: Lista de dados.
    :param file_suffix: Sufixo do arquivo de dados.
    '''
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
    '''
    Gera amostras de dados numéricos aleatórios.
    :param qnt: Tamanho do conjunto de dados.
    '''
    lst = []
    for i in np.random.rand(qnt).tolist():
        lst.append(f"{(int(i * pow(10, 13)))}\n")
    _generate_sample(np.unique(lst).tolist(), qnt)

def generate_sample_str(file_suffix):
    '''
    Gera amostras de dados a partir de dicionário de palavras.
    :param file_suffix: Sufixo do arquivo de dados.
    '''
    with (RESOURCES / f"ascending-order-{file_suffix}.txt").open("r") as f:
        _generate_sample(f.readlines(), file_suffix)

def _merge(lst, l, m, r):
    '''
    Método auxiliar do algoritmo de ordenação merge-sort.
    :param lst: Conjunto de dados.
    :param l: Posição a esquerda da lista.
    :param m: Posição central da lista.
    :param r: Posição a direita da lista.
    '''
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = lst[l + i]

    for j in range(0, n2):
        R[j] = lst[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            lst[k] = L[i]
            i += 1
        else:
            lst[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        lst[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        lst[k] = R[j]
        j += 1
        k += 1

def _merge_sort(lst, l, r):
    '''
    Ordena lista de dados utilizando o algoritmo merge-sort.
    :param lst: Conjunto de dados.
    :param l: Posição a esquerda da lista.
    :param r: Posição a direita da lista.
    '''
    if l < r:
        m = l + (r-l) // 2

        _merge_sort(lst, l, m)
        _merge_sort(lst, m + 1, r)
        _merge(lst, l, m, r)

def _list_from_file(filename, is_numeric_val):
    '''
    Gera lista a partir de arquivo de conjunto de dados.
    :param filename: Nome do arquivo.
    :param is_numeric_val: Se o conjunto de dados é numérico.
    :return list[str]
    '''
    with open(RESOURCES / filename, "r") as f:
        lst = f.readlines()
    if is_numeric_val:
        for i in range(0, len(lst)):
            lst[i] = int(lst[i])
    return lst

def _get_data_filenames(file_suffix):
    '''
    Recupera nome completo de arquivos de determinado conjunto de dados.
    :param file_suffix: Sufixo do arquivo de dados.
    :return list[str]
    '''
    return [
        f"ascending-order-{file_suffix}.txt",
        f"random-order-{file_suffix}.txt",
        f"descending-order-{file_suffix}.txt"
    ]

def _benchmark(lst):
    '''
    Avalia o desempenho do algoritmo merge-sort em segundos.
    Obs.: truncado em 3 casas decimais.
    :param lst: Conjunto de dados.
    :return float
    '''
    start = time.perf_counter()
    _merge_sort(lst, 0, len(lst) - 1)
    end = time.perf_counter()
    return _truncate_float(end - start)

def benchmark_merge_sort(file_suffix, is_numeric_val=False):
    '''
    Avalia o desempenho do algoritmo merge-sort em diversos conjuntos de dados.
    :param file_suffix: Sufixo do arquivo de dados.
    :param is_numeric_val: Se o conjunto de dados é numérico.
    :return tuple(float, float, float)
    '''
    res = []
    for f in _get_data_filenames(file_suffix):
        res.append(_benchmark(_list_from_file(f, is_numeric_val)))
    return tuple(res)

def _truncate_float(num):
    '''
    Trunca float em 3 casas decimais.
    :num Número a ser truncado.
    :return float
    '''
    mult = 10 ** 3
    return int(num * mult) / mult

def _calculate_plot_height(benchmarks):
    '''
    Calcula altura do gráfico.
    :param benchmarks: Resultados do benchmark.
    :return float
    '''
    arr = []
    for v in benchmarks.values():
        arr.extend(list(v))
    return max(arr)

def plot(benchmarks, title_suffix):
    '''
    Exibe gráfico de benchmarks.
    :param benchmarks: Resultados dos benchmarks.
    :param title_suffix: Informações adicionais do título.
    '''
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
