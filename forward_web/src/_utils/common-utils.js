export const simulateApiCall = async () => {
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));
  return await delay(500);
};

// temporary splitting descriptions into hard arbitrary num of paragraphs
export const splitDescription = (description) => {
  const toSplit = description;
  let prevPointer = 0;
  let sentence = 0;
  const result = [];

  for (let i = 0; i < toSplit.length; i++) {
    if (
      (description[i] === '.' &&
        description[i + 1] === ' ' &&
        description[i - 1] !== 'S') ||
      description[i] === '?'
    ) {
      sentence++;
    }

    if (sentence > 2) {
      // i+1 to include period
      const paragraph = toSplit.slice(prevPointer, i + 1);
      result.push(paragraph);
      // i+2 to exclude space after period
      prevPointer = i + 2;
      sentence = 0;
    }
  }

  result.push(toSplit.slice(prevPointer, toSplit.length));

  return result;
};
