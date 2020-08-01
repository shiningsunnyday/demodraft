import axios from "axios";

export class ApiUtil {
  static async getPolicies() {
    let response;

    try {
      response = await axios.get("https://jsonplaceholder.typicode.com/posts");
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getPolicy(id) {
    let response;

    try {
      response = await axios.get(
        `https://jsonplaceholder.typicode.com/posts/${id}`
      );
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }
}
