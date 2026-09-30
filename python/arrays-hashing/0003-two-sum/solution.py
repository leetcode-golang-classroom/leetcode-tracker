def solve(nums: list[int], target: int) -> list[int]:
    visited = {}
    for idx, num in enumerate(nums):
        matchedVal = target - num
        if matchedVal in visited:
            return [visited[matchedVal], idx]

        visited[num] = idx

    return []
