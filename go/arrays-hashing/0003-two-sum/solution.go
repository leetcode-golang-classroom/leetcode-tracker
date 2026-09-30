package main

func Solve(nums []int, target int) []int {
	visited := make(map[int]int)
	for idx, num := range nums {
		// lookup for target - num exists in the visited map
		matchedVal := target - num
		if matchedIdx, ok := visited[matchedVal]; ok {
			return []int{matchedIdx, idx}
		}
		// setup current value to visited map
		visited[num] = idx
	}
	return []int{}
}
