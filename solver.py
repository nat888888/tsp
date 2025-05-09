#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# ベクトルPQとベクトルQRのクロスプロダクトを計算
def cross_product(P, Q, R):
    return (Q[0] - P[0]) * (R[1] - P[1]) - (Q[1] - P[1]) * (R[0] - P[0])

# 2-opt (return boolean)
def two_opt(a, b, c, d, array):
    P1 = array[a]
    P2 = array[b]
    Q1 = array[c]
    Q2 = array[d]

    # P1P2の端点Q1とQ2が異なる側にあるかを判定
    d1 = cross_product(P1, P2, Q1)
    d2 = cross_product(P1, P2, Q2)
    
    # Q1Q2の端点P1とP2が異なる側にあるかを判定
    d3 = cross_product(Q1, Q2, P1)
    d4 = cross_product(Q1, Q2, P2)
    
    # それぞれ異なる側にあるかを確認
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return False


def solve(cities):
    # N: number of cities
    N = len(cities)

    # calculate each distance O(N)?
    dist = [[0] * N for i in range(N)] #??
    for i in range(N):
        for j in range(i, N): #i<j<N
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

# current city に一番近い場所を next city とする
    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

#交差している道順を交換する
    for k in range(N-1):
        for m in range(k,N-1):
            if two_opt(tour[k], tour[k+1], tour[m], tour[m+1], cities) == True: 
                temp = tour[k+1]
                tour[k+1] = tour[m]
                tour[m] = temp
    print('total_distance:',total_distance(tour,cities,N))
    return tour

# calculate total distance
def total_distance(tour, cities, N): 
    total_distance = 0
    for i in range(N-1):
        total_distance += distance(cities[tour[i]], cities[tour[i+1]])
    total_distance += distance(cities[tour[N-1]], cities[tour[0]])
    return total_distance

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    # print_tour(tour)
