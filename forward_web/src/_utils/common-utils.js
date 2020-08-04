export class CommonUtils {
  static removeFilterDuplicates(arr) {
    arr.splice(0, arr.length, ...new Set(arr));

    return arr;
  }
}