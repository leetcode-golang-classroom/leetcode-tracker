def solve(n: int, edges: list[list[int]]) -> int:
    # union find algorithm
    parents = [i for i in range(n + 1)]
    ranks = [1] * n

    def find(v: int) -> int:
        p = parents[v]
        while p != parents[p]:
            parents[p] = parents[parents[p]]
            p = parents[p]

        return p

    def union(v1, v2: int) -> int:
        p1, p2 = find(v1), find(v2)

        if p1 == p2:
            return 0

        if ranks[p2] > ranks[p1]:
            parents[p1] = p2
            ranks[p2] += 1
        else:
            parents[p2] = p1
            ranks[p1] += 1

        return 1

    res = n
    for edge in edges:
        res -= union(edge[0], edge[1])

    return res
