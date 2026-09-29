function solve({nums=[], target}) {
  const len = nums.length;
  result = []
  const map = new Map();
  for (let i = 0; i < len; i++) {
    const want = target - nums[i];
    const idx = map[want];
    if (idx != undefined) {
      return (idx > i)? [i, idx]: [idx, i]
    }
    map[nums[i]] = i 
  }
  return result
}

module.exports = {solve}