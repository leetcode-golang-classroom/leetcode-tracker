/**
 * @param {{s: string}} input
 * @returns {boolean}
 */
function solve({ s = "" }) {
  let [lp, rp] = [0, s.length - 1];
  while (lp < rp) {
    if (!isAlphaNum(s.charCodeAt(lp))) {
      lp++;
      continue;
    }
    if (!isAlphaNum(s.charCodeAt(rp))) {
      rp--;
      continue;
    }

    if (s.charAt(lp).toUpperCase().charCodeAt(0) !== s.charAt(rp).toUpperCase().charCodeAt(0)) {
      return false;
    }
    lp++;
    rp--;
  }
  return true;
}

function isAlphaNum(c=0) {
  return (
    (c >= 'a'.charCodeAt(0) && c <= 'z'.charCodeAt(0)) ||
    (c >= 'A'.charCodeAt(0) && c <= 'Z'.charCodeAt(0)) ||
    (c >= '0'.charCodeAt(0) && c <= '9'.charCodeAt(0))
  );
}
module.exports = { solve };
