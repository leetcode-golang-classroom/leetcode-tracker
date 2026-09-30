function solve({ nums = [], target }) {
  const length = nums.length;
  const visited = new Map();
  for (let idx = 0; idx < length; idx++) {
    // check target - nums[idx] exists in visited map
    const matchedValue = target - nums[idx];
    const matchedIdx = visited.get(matchedValue);
    if (matchedIdx !== undefined) {
      return [matchedIdx, idx];
    }

    // setup current value to visited map
    visited.set(nums[idx], idx);
  }
  return [];
}

module.exports = { solve };
