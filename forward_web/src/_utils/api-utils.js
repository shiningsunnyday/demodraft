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

  static async getThreadFromComment(id) {
    let response;
    try {
      response = await axios.get(`${ApiUtil.api_url}/thread/?thread_id=${id}`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data.splice(1);
  }

  static async policyLike(id) {
    let response;
    try {
      response = await axios.put(`${ApiUtil.api_url}/policy/`, {id: id});
    } catch (error) {
      console.error(error.message);
    }
    return response.data.likes;
  }

  static async commentLike(id) {
    let response;
    try {
      response = await axios.patch(`${ApiUtil.api_url}/comment/`, {comment_id: id});
    } catch (error) {
      console.error(error.message);
    }
    console.log(response.data);
    
    return response.data.likes;
  }

  static async addNewThread(data) {
    try {
      await axios.post(`${ApiUtil.api_url}/thread/`, data);
    } catch (error) {
      console.error(error.message);
    }
  }
}

