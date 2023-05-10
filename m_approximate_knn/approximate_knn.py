from collections import OrderedDict, defaultdict
from typing import Callable, Tuple, Dict, List

import numpy as np
from tqdm.auto import tqdm


def distance(pointA: np.ndarray, documents: np.ndarray) -> np.ndarray:

    return np.sqrt(np.sum((documents - pointA) ** 2, axis=1)).reshape(-1, 1)


def create_sw_graph(
        data: np.ndarray,
        num_candidates_for_choice_long: int = 10,
        num_edges_long: int = 5,
        num_candidates_for_choice_short: int = 10,
        num_edges_short: int = 5,
        use_sampling: bool = False,
        sampling_share: float = 0.05,
        dist_f: Callable = distance
    ) -> Dict[int, List[int]]:

    # Инициализация выходного словаря
    res_graph = OrderedDict()
    # Получение количества точек
    sz_data = data.shape[0]

    for p in tqdm(range(sz_data)):
        if use_sampling:
            # Формируем выборку размером sampling_share от всей data по координатам
            p_coords = np.random.choice(sz_data, size=int(sampling_share * sz_data), replace=False)
            # Вычисление всех дистанций от точки p до всех точек в data[p_coords]
            # Сортировка получнных дистанций и получение индексов данных точек того, как
            # они могли бы быть отсортированы относительно исходного
            # массива с дистанциями(data[p_coords])
            coords = p_coords[np.argsort(dist_f(data[p], data[p_coords]), axis=0).reshape(-1)]
        else:
            # Вычисление всех дистанций от точки p до всех точек в data
            # Сортировка получнных дистанций и получение индексов данных точек того, как
            # они могли бы быть отсортированы относительно исходного массива с дистанциями
            coords = np.argsort(dist_f(data[p], data), axis=0).reshape(-1)
        # Исключение точки p из массива с индексами, так как растояние до исходной точки
        # нам не нужно
        coords = coords[coords != p]

        # На случай, если num_edges_long < cur_sz и num_edges_short < cur_sz(для random.choice)
        cur_sz = coords.shape[0]
        num_edges_long = min(num_edges_long, cur_sz)
        num_edges_short = min(num_edges_short, cur_sz)

        # Выбор первых num_candidates_for_choice_short точек минимальных дистанций
        # Выбор num_edges_short точек случайно
        for_short = np.random.choice(coords[:num_candidates_for_choice_short],
                                     size=num_edges_short, replace=False)

        # Выбор топ num_candidates_for_choice_long точек максимальных дистанций
        # Выбор num_edges_long точек случайно
        for_long = np.random.choice(coords[-num_candidates_for_choice_long:],
                                    size=num_edges_long, replace=False)

        res_graph[p] = list(np.concatenate((for_short, for_long)))
    return res_graph

def return_all_indx(or_dct, indxs):
    out_ind = []
    for i in indxs:
        out_ind += or_dct[i] + [i]

    return np.array(list(set(out_ind)))

def nsw(query_point: np.ndarray, all_documents: np.ndarray,
        graph_edges: Dict[int, List[int]],
        search_k: int = 10, num_start_points: int = 5,
        dist_f: Callable = distance) -> np.ndarray:

    # Определяем размер входного массива с документами
    sz_dt = all_documents.shape[0]

    # Выбираем num_start_points точек из np.arange(sz_dt)
    n_pt = np.random.choice(sz_dt, size=num_start_points, replace=False)

    # Собираем все точки с которыми соседствуют входные точки + сами точки
    n_points = return_all_indx(graph_edges, n_pt)

    # Определяем дистанцию между query_point и документами с координатами n_points
    n_pt_dist = dist_f(query_point, all_documents[n_points]).reshape(-1)

    # Записываем search_k ближайших точек их дистанций к query_point и их
    # среднюю дистанцию до query_point
    sorted_pt = np.argsort(n_pt_dist)
    prev_pt = n_points[sorted_pt][:search_k]
    prev_dist = n_pt_dist[sorted_pt][:search_k]
    prev_avg = prev_dist.mean()

    while True:

        # Собираем все точки с которыми соседствуют входные точки + сами точки
        n_points = return_all_indx(graph_edges, prev_pt)

        # Определяем дистанцию между query_point и документами с координатами n_points
        n_pt_dist = dist_f(query_point, all_documents[n_points]).reshape(-1)

        # Записываем search_k ближайших точек их дистанций к query_point и их
        # среднюю дистанцию до query_point
        sorted_pt = np.argsort(n_pt_dist)
        cur_pt = n_points[sorted_pt][:search_k]
        cur_dist = n_pt_dist[sorted_pt][:search_k]
        cur_avg = cur_dist.mean()

        if prev_avg <= cur_avg:
            break

        # Перезаписываем search_k ближайших точек их дистанций к query_point и их
        # среднюю дистанцию до query_point
        prev_pt = cur_pt.copy()
        prev_dist = cur_dist.copy()
        prev_avg = cur_avg

    return prev_pt
