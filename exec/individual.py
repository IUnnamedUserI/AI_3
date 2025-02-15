#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt


# Пример входных данных (можно заменить своими)
cities = {
    'Лонгфорд': {'Ньюнхем': 31.4, 'Экстон': 37.1, 'Бреона': 51.4, 'Конара': 43.2, 'Дерби': 111.9},
    'Конара': {'Сент-Мэрис': 73.9, 'Кэмпбелл-Таун': 12.5},
    'Кэмпбелл-Таун': {'Танбридж': 27.1, 'Лейк Лик': 34.8},
    'Лейк Лик': {'Бичено': 57, 'Суонси': 33.8},
    'Ньюнхем': {'Джордж Таун': 44.3, 'Лилидейл': 21.3},
    'Джордж Таун': {},
    'Лилидейл': {'Лебрина': 8.7},
    'Лебрина': {'Пайперс Брук': 13.3, 'Бридпорт': 27},
    'Экстон': {'Элизабет Таун': 18.4, 'Мол Крик': 30.8, 'Бреона': 38.4},
    'Элизабет Таун': {'Шеффилд': 28, 'Девонпорт': 42.5},
    'Девонпорт': {},
    'Шеффилд': {'Мойна': 31.7},
    'Мойна': {},
    'Бреона': {'Рейнольдс Лейк': 11.2, 'Шеннон': 26.5, 'Ботуэлл': 66.7},
    'Рейнольдс Лейк': {'Миена': 18.5},
    'Мол Крик': {'Шеффилд': 51.5},
    'Миена': {'Тарралия': 59.2},
    'Шеннон': {'Миена': 17.2},
    'Тарралия': {'Уэйятина': 16.5},
    'Уэйятина': {} ,
    'Ботуэлл': {},
    'Танбридж': {},
    'Литл Суонпорт': {},
    'Суонси': {'Литл Суонпорт': 27.7},
    'Сент-Мэрис': {'Гарденс': 55.8},
    'Гарденс': {'Дерби': 61.1},
    'Дерби': {},
    'Пайперс Брук': {},
    'Бридпорт': {},
}

start_city = 'Гарденс'  # Исходный город
end_city = 'Мойна'    # Целевой город

# Создание симметричного графа
def create_symmetric_graph(cities):
    symmetric_cities = {}
    for city, neighbors in cities.items():
        if city not in symmetric_cities:
            symmetric_cities[city] = {}
        for neighbor, distance in neighbors.items():
            symmetric_cities[city][neighbor] = distance
            if neighbor not in symmetric_cities:
                symmetric_cities[neighbor] = {}
            symmetric_cities[neighbor][city] = distance
    return symmetric_cities

symmetric_cities = create_symmetric_graph(cities)

# Поиск маршрута с учётом расстояния с использованием поиска в глубину (DFS)
def dfs_shortest_path(cities, start, end):
    visited = set()
    shortest_path = None
    shortest_distance = float('inf')

    def dfs(current, path, current_distance):
        nonlocal shortest_path, shortest_distance
        if current == end:
            if current_distance < shortest_distance:
                shortest_path = path
                shortest_distance = current_distance
            return
        visited.add(current)
        for neighbor, distance in cities.get(current, {}).items():
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor], current_distance + distance)
        visited.remove(current)

    dfs(start, [start], 0)
    return shortest_path, shortest_distance

# Построение графа и отображение маршрутов
def plot_graph(cities, routes, shortest_route):
    G = nx.DiGraph()
    
    # Добавление рёбер с весами
    for city, neighbors in cities.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(city, neighbor, weight=weight)

    pos = nx.spring_layout(G)  # Позиционирование узлов
    
    # Отображение графа
    plt.figure(figsize=(12, 8))
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Подсветка самого короткого маршрута
    if shortest_route:
        shortest_edges = [(shortest_route[i], shortest_route[i + 1]) for i in range(len(shortest_route) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=shortest_edges, edge_color='red', width=2)

    plt.title("Граф маршрутов")
    plt.show()

# Основной код
shortest_route, shortest_distance = dfs_shortest_path(symmetric_cities, start_city, end_city)

# Вывод самого короткого маршрута
if shortest_route:
    print(f"\nСамый короткий маршрут: {' -> '.join(shortest_route)}, Расстояние: {round(shortest_distance, 1)} км")
    plot_graph(symmetric_cities, [shortest_route], shortest_route)
else:
    print("Путь не найден")
