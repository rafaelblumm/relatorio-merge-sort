import time
import random
import pathlib
import numpy as np
import matplotlib.pyplot as plt

RESOURCES = pathlib.Path(__file__).parent.parent / "resources"
RESOURCES_TMP = RESOURCES / "tmp"

def _generate_sample(lst, file_suffix, is_numeric=False):
    '''
    Gera e grava amostras de dados em ordens crescente, decrescente e aleatória.
    :param lst: Lista de dados.
    :param file_suffix: Sufixo do arquivo de dados.
    '''
    # Ordem crescente
    res = RESOURCES_TMP
    if not is_numeric:
        res = RESOURCES
        lst.sort()
    with (res / f"ascending-order-{file_suffix}.txt").open("w") as f:
        f.writelines(lst)

    # Ordem decrescente
    lst.reverse()
    with (RESOURCES_TMP / f"descending-order-{file_suffix}.txt").open("w") as f:
        f.writelines(lst)

    # Ordem aleatória
    random.Random(7).shuffle(lst)
    with (RESOURCES_TMP / f"random-order-{file_suffix}.txt").open("w") as f:
        f.writelines(lst)

def generate_sample_int(qnt):
    '''
    Gera amostras de dados numéricos.
    :param qnt: Tamanho do conjunto de dados.
    '''
    lst = []
    for i in range(1, qnt + 1):
        lst.append(f"{i}\n")
    _generate_sample(lst, qnt, is_numeric=True)

def generate_sample_str(file_suffix):
    '''
    Gera amostras de dados a partir de dicionário de palavras.
    :param file_suffix: Sufixo do arquivo de dados.
    '''
    with (RESOURCES / f"ascending-order-{file_suffix}.txt").open("r") as f:
        _generate_sample(f.readlines(), file_suffix)

def _merge(a, aux, lo, mid, hi):
    '''
    Método auxiliar do algoritmo de ordenação merge-sort. Retorna quantidade
    de trocas realizadas para a ordenação
    :param a: Array a ser ordenado.
    :param lo: Posição a esquerda da lista.
    :param mid: Posição central da lista.
    :param hi: Posição a direita da lista.
    :return int
    '''
    iter = 0
    for k in range(lo, hi + 1):
        aux[k] = a[k]
    i = lo
    j = mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            a[k] = aux[j]
            j += 1
            iter += 1
        else:
            a[k] = aux[i]
            i += 1
    return iter

def _merge_sort(a, aux, lo, hi):
    '''
    Ordena lista de dados utilizando o algoritmo merge-sort, retornando
    quantidade de trocas realizadas para a ordenação
    :param a: Conjunto de dados.
    :param lo: Posição a esquerda da lista.
    :param hi: Posição a direita da lista.
    :return int
    '''
    iter = 0
    if hi <= lo:
        return iter
    mid = lo + (hi - lo) // 2
    iter += _merge_sort(a, aux, lo, mid)
    iter += _merge_sort(a, aux, mid + 1, hi)
    iter += _merge(a, aux, lo, mid, hi)
    return iter

def _list_from_file(filename, is_numeric_val):
    '''
    Gera lista a partir de arquivo de conjunto de dados.
    :param filename: Nome do arquivo.
    :param is_numeric_val: Se o conjunto de dados é numérico.
    :return list[str]
    '''
    with open(RESOURCES / filename, "r") as f:
        lst = f.readlines()
    return [int(i) for i in lst] if is_numeric_val else lst

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
    :return tuple(float, int)
    '''
    start = time.perf_counter()
    iter = _merge_sort(lst, [0] * len(lst), 0, len(lst) - 1)
    end = time.perf_counter()
    return (_truncate_float(end - start), iter)

def benchmark_merge_sort(file_suffix, is_numeric_val=True):
    '''
    Avalia o desempenho do algoritmo merge-sort em diversos conjuntos de dados.
    :param file_suffix: Sufixo do arquivo de dados.
    :param is_numeric_val: Se o conjunto de dados é numérico.
    :return tuple(float, float, float)
    '''
    res = [[], []]
    for f in _get_data_filenames(file_suffix):
        bm = _benchmark(_list_from_file(f, is_numeric_val))
        res[0].append(bm[0])
        res[1].append(bm[1])
    return [tuple(res[0]), tuple(res[1])]

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

def process_bm_data(bm, labels):
    '''
    Processa dados de benchmark para plotagem.
    :param bm: Resultados dos benchmarks.
    :param labels: Labels dos dados.
    :return list[dict]
    '''
    a = []
    for i in range(0, 2):
        aux = {
            labels[0]: bm[0][i],
            labels[1]: bm[1][i],
            labels[2]: bm[2][i]
        }
        a.append(aux)
    return a

def _plot(benchmarks, title_suffix, y_label):
    '''
    Exibe gráfico de benchmarks.
    :param benchmarks: Resultados dos benchmarks.
    :param title_suffix: Informações adicionais do título.
    :param y_label: Label do eixo Y
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

    ax.set_ylabel(y_label)
    ax.set_title(f"Benchmark merge-sort ({title_suffix})")
    ax.set_xticks(x + width, sort_order)
    ax.legend(loc='upper left', ncols=3)
    h = _calculate_plot_height(benchmarks)
    ax.set_ylim(0, h + 0.2 * h)
    
    plt.show()


def plot_time(benchmarks, title_suffix):
    '''
    Exibe gráfico de benchmarks de tempo de execução.
    :param benchmarks: Resultados dos benchmarks.
    :param title_suffix: Informações adicionais do título.
    '''
    _plot(benchmarks, title_suffix, "Tempo (segundos)")

def plot_switch(benchmarks, title_suffix):
    '''
    Exibe gráfico de benchmarks de trocas para ordenação.
    :param benchmarks: Resultados dos benchmarks.
    :param title_suffix: Informações adicionais do título.
    '''
    _plot(benchmarks, title_suffix, "Trocas")
