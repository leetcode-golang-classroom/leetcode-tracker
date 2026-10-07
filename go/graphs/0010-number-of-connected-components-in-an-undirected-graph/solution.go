package main

func Solve(n int, edges [][]int) int {
	// union find 演算法
	// 分為兩大步驟
	// 1. 針對每個節點定義自己的 parent
	// 2. 每次目前的作 union 動作
	//     2.1 找到各自節點的 root
	//     2.2 如果 root 相同代表已經是 connected component 直接回傳 0 代表沒有執行 union
	//     2.3 如果不相同，把 ranks 比較大的 root 設定為另一個的 root，並且 root 的 rank +1 回傳 1

	parents, ranks := make([]int, n), make([]int, n)
	for i := range n {
		parents[i] = i
		ranks[i] = 1
	}

	// find the root of v
	var find func(v int) int
	find = func(v int) int {
		p := parents[v]
		for p != parents[p] {
			parents[p] = parents[parents[p]]
			p = parents[p]
		}
		return p
	}

	// union v1, v2
	var union func(v1, v2 int) int
	union = func(v1, v2 int) int {
		p1, p2 := find(v1), find(v2)
		if p1 == p2 {
			return 0
		}
		if ranks[p2] > ranks[p1] {
			parents[p1] = p2
			ranks[p2]++
		} else {
			parents[p2] = p1
			ranks[p1]++
		}
		return 1
	}

	res := n
	// for each edge union
	for _, edge := range edges {
		res -= union(edge[0], edge[1])
	}
	return res
}
