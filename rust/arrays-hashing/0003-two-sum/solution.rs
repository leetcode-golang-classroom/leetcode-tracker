use std::collections::HashMap;

fn solve(nums: Vec<i64>, target: i64) -> Vec<i64> {
    let mut visited: HashMap<i64, i64> = HashMap::new();

    for (i, &num) in nums.iter().enumerate() {
        let complement = target - num;

        if let Some(&prev_index) = visited.get(&complement) {
            return vec![prev_index as i64, i as i64];
        }

        visited.insert(num, i as i64);
    }
    vec![]
}
