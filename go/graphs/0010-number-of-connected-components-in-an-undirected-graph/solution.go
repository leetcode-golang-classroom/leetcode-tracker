package main

func Solve(n int, edges [][]int) int {
	// 1 建立 adjacency list 來紀錄每個節點相連的狀況
	// 2 透過 DFS 逐個節點透過 adjacency list 來走訪節點，只要每次走完就把 counter 加一
	adjacencyMap := make(map[int][]int, n)
	for _, edge := range edges {
		adjacencyMap[edge[0]] = append(adjacencyMap[edge[0]], edge[1])
		adjacencyMap[edge[1]] = append(adjacencyMap[edge[1]], edge[0])
	}
	// 紀錄走訪過得
	visited := make(map[int]struct{}, n)

	var dfs func(node int)
	dfs = func(node int) {
		if _, ok := visited[node]; ok {
			return
		}
		visited[node] = struct{}{}
		adjacencyNodes := adjacencyMap[node]
		for _, adjacencyNode := range adjacencyNodes {
			if _, ok := visited[adjacencyNode]; !ok {
				dfs(adjacencyNode)
			}
		}
	}

	result := 0
	for i := 0; i < n; i++ {
		if _, ok := visited[i]; !ok {
			dfs(i)
			result++
		}
	}
	return result
}
