import axios from "axios";

export class ApiUtil {

  static api_url = "http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com";

  static async getPolicies() {
    let response;

    try {
      response = await axios.get(`${ApiUtil.api_url}/policies/`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getPolicy(id) {
    let response;
    try {
      response = await axios.get(`${ApiUtil.api_url}/policy/?id=${id}`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getPolicyComments(id) {
    let response;
    try {
      response = await axios.get(`${ApiUtil.api_url}/thread/?policy_id=${id}`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async policyLike(id) {
    let response;
    try {
      response = await axios.put(`${ApiUtil.api_url}/policy/`, {data: {id: id}});
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async commentLike(id) {
    let response;
    try {
      response = await axios.patch(`${ApiUtil.api_url}/comment`, {data: {comment_id: id}});
    } catch (error) {
      console.error(error.message);
    }
    let data = response.data;
    
    return data.likes;
  }
}
