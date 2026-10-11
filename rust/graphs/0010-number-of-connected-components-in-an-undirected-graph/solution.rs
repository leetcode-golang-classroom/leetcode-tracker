fn solve(n: i64, edges: Vec<Vec<i64>>) -> i64 {
    // union-find 驗算法
    // 1 針對每個節點定義自己節點的 parent
    // 2 對每個邊做 union 動作
    //     2.1 找到各自節點的 root
    //     2.2 如果 root 相同代表已經是 connected component 直接回傳 0 代表沒有執行 union
    //     2.3 如果不相同，把 ranks 比較大的 root 設定為另一個的 root，並且 root 的 rank +1 回傳 1
    // 1. 型態轉換：將核心陣列大小與索引轉為 usize
    let n_usize = n as usize;

    // 初始化 parent 和 rank 陣列
    let mut parent: Vec<usize> = (0..n_usize).collect();
    let mut rank: Vec<usize> = vec![0; n_usize];
    let mut component_count = n; // 範例：用來記錄連通元件（集合）的數量

    // find 找出 i 的 root
    fn find(i: usize, parent: &mut Vec<usize>) -> usize {
        if parent[i] == i {
            i
        } else {
            parent[i] = find(parent[i], parent);
            parent[i]
        }
    }

    // merge
    for edge in edges {
        let u = edge[0] as usize;
        let v = edge[1] as usize;

        let root_u = find(u, &mut parent);
        let root_v = find(v, &mut parent);

        if root_u != root_v {
            if rank[root_u] > rank[root_v] {
                parent[root_v] = root_u;
                rank[root_u] += 1;
            } else {
                parent[root_u] = root_v;
                rank[root_v] += 1;
            }
            component_count -= 1;
        }
    }

    component_count
}
