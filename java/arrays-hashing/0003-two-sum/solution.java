import java.util.HashMap;

class Solution {
    static int[] solve(int[] nums, int target) {
        HashMap<Integer, Integer> visited = new HashMap<>();
        int length = nums.length;
        for (int idx = 0; idx < length; idx++) {
            int matchedValue = target - nums[idx];
            if (visited.containsKey(matchedValue)) {
                return new int[] {visited.get(matchedValue), idx};
            }
            visited.put(nums[idx], idx);
        }

        return new int[] {};
    }
}
