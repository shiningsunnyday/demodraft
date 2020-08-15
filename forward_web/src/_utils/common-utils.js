export const simulateApiCall = async () => {
  const delay = ms => new Promise(res => setTimeout(res, ms));
  return await delay(500);
};