import axios from "axios";

export class ApiUtil {
  static async getPolicies() {
    let response;

    try {
      response = await axios.get("http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/policies/");
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getPolicy(id) {
    let response;
    try {
      response = await axios.get(`http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com/policy/?id=${id}`);
      console.log(response);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }
}
