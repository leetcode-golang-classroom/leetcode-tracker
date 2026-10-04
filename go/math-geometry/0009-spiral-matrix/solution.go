package main

func Solve(matrix [][]int) []int {
	// 紀錄當下還沒完成的邊界，每次從每個邊線去把每個元素加入陣列
	// 需要判斷是否有重複讀取到已經處理的元素
	left, right := 0, len(matrix[0])
	top, bottom := 0, len(matrix)
	result := make([]int, 0, right*bottom)
	for left < right && top < bottom {
		// top, left -> right -1
		for col := left; col < right; col++ {
			result = append(result, matrix[top][col])
		}
		top++

		// top -> bottom-1, right-1
		for row := top; row < bottom; row++ {
			result = append(result, matrix[row][right-1])
		}
		right--

		// check duplicate
		if right == left || top == bottom {
			break
		}

		// bottom-1, right-1 -> left
		for col := right - 1; col >= left; col-- {
			result = append(result, matrix[bottom-1][col])
		}
		bottom--

		// bottom-1 -> top, left
		for row := bottom - 1; row >= top; row-- {
			result = append(result, matrix[row][left])
		}
		left++
	}
	return result
}
