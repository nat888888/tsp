#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input

#calculate distance
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

#citiesを４分割する
def divide_cities(cities):
    M = len(cities)
    # print('M:',M)

    # max_x = cities[0][0]
    # min_x = cities[0][0]
    # max_y = cities[0][1]
    # min_y = cities[0][1]
    # for i in range(1,M):
    #     if max_x < cities[i][0]:
    #         max_x = cities[i][0]
    #     if min_x > cities[i][0]:
    #         min_x = cities[i][0]
    #     if max_y < cities[i][1]:
    #         max_y = cities[i][1]
    #     if min_y > cities[i][1]:
    #         min_y = cities[i][1]
    max_x = max(cities, key=lambda city: city[0])[0]
    min_x = min(cities, key=lambda city: city[0])[0]
    max_y = max(cities, key=lambda city: city[1])[1]
    min_y = min(cities, key=lambda city: city[1])[1]

    mid_x = (max_x + min_x) / 2
    mid_y = (max_y + min_y) / 2

    cities1 = []
    cities1_index = []
    cities2 = []
    cities2_index = []
    cities3 = []
    cities3_index = []
    cities4 = []
    cities4_index = []

    for i in range(M):
        if cities[i][0] < mid_x and cities[i][1] < mid_y:
            cities1.append(cities[i])
            cities1_index.append(i)
        elif cities[i][0] >= mid_x and cities[i][1] < mid_y:
            cities2.append(cities[i])
            cities2_index.append(i)
        elif cities[i][0] < mid_x and cities[i][1] >= mid_y:
            cities3.append(cities[i])
            cities3_index.append(i)
        else: 
            cities4.append(cities[i])
            cities4_index.append(i)
    print('cities1:',cities1_index)
    print('cities2:',cities2_index)
    print('cities3:',cities3_index)
    print('cities4:',cities4_index)
    return cities1, cities2, cities3, cities4, cities1_index, cities2_index, cities3_index, cities4_index

def solve(cities, cities_index):
    # if cities == []:
    #     return []
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
        # print(current_city)

#2-opt 交差している道順を交換する
    for k in range(N-1):
        for m in range(k+2,N-1):
            if two_opt(tour[k], tour[k+1], tour[m], tour[m+1], cities) == True: 
                temp = tour[k+1]
                tour[k+1] = tour[m]
                tour[m] = temp
#tourのindexを入れ替える
    new_tour = [0]*N
    for m in range(N):
        new_tour[m] = cities_index[tour[m]]
    this_distance = total_distance(tour,cities,N)
    print('total_distance:', this_distance)
    return new_tour, this_distance

# calculate total distance
def total_distance(tour, cities, N): 
    total_distance = 0
    for i in range(N-1):
        total_distance += distance(cities[tour[i]], cities[tour[i+1]])
    total_distance += distance(cities[tour[N-1]], cities[tour[0]])
    return total_distance

if __name__ == '__main__':
    assert len(sys.argv) > 1
    city1, city2, city3, city4, cities1_index, cities2_index, cities3_index, cities4_index = divide_cities(read_input(sys.argv[1]))
    final_tour = []

    tour1, distance1 = solve(city1, cities1_index)
    final_tour.extend(tour1)
    # print('final_tour:', final_tour)
    
    tour2, distance2= solve(city2, cities2_index)
    final_tour.extend(tour2)
    distance12 = distance(city1[-1], city2[0]) if city1 and city2 else 0
    # print('final_tour:', final_tour)
    
    tour3, distance3 = solve(city3, cities3_index)
    final_tour.extend(tour3)
    distance23 = distance(city2[-1], city3[0]) if city2 and city3 else 0
    # print('final_tour:', final_tour)
    
    tour4, distance4 = solve(city4, cities4_index)
    final_tour.extend(tour4)
    distance34 = distance(tour3[len(tour3)], tour4[0])
    # print('final_tour:', final_tour)

    sum_distance = distance1 + distance2 + distance3 + distance4 + distance12 + distance23 + distance34
    print('distance:', sum_distance)
    
    # print_tour(final_tour)