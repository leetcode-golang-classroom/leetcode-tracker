package main

func Solve(nums []int, target int) []int {
	seen := make(map[int]int, len(nums))
	result := []int{}
	for i := range nums {
		// 每次都先查詢補數是否有出現
		find := target - nums[i]
		if val, ok := seen[find]; ok {
			if i > val {
				return []int{val, i}
			}
			return []int{i, val}
		}

		// 當補數不存在才繼續加入
		seen[nums[i]] = i
	}
	return result
}
