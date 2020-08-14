import axios from 'axios';
import * as Config from '../config.json';
export class ApiUtil {
  static async getPolicies() {
    let response;

    try {
      response = await axios.get(`${Config.API_URL}/policies/`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getPolicy(id) {
    let response;
    try {
      response = await axios.get(`${Config.API_URL}/policy/?id=${id}`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getPolicyComments(id) {
    let response;
    try {
      response = await axios.get(`${Config.API_URL}/thread/?policy_id=${id}`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getThreadFromComment(id) {
    let response;
    try {
      response = await axios.get(`${Config.API_URL}/thread/?thread_id=${id}`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data.splice(1);
  }

  static async policyLike(id) {
    let response;
    try {
      response = await axios.put(`${Config.API_URL}/policy/`, { id: id });
    } catch (error) {
      console.error(error.message);
    }
    return response.data.likes;
  }

  static async commentLike(id) {
    let response;
    try {
      response = await axios.patch(`${Config.API_URL}/comment/`, {
        comment_id: id,
      });
    } catch (error) {
      console.error(error.message);
    }

    return response.data.likes;
  }

  static async addNewThread(data) {
    try {
      await axios.post(`${Config.API_URL}/thread/`, data);
    } catch (error) {
      console.error(error.message);
    }
  }

  static async addNewReply(data) {
    try {
      await axios.post(`${Config.API_URL}/comment/`, data);
    } catch (error) {
      console.error(error.message);
    }
  }

  static async getAllPoliticians() {
    let response;

    try {
      response = await axios.get(`${Config.API_URL}/politician/`);
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async getSelectedPolitician(id) {
    let response;

    try {
      response = await axios.get(
        `${Config.API_URL}/politician/?politician_id=${id}`
      );
    } catch (error) {
      console.error(error.message);
    }

    return response.data;
  }

  static async postAddress(data) {
    try {
      return await axios({
        method: 'post',
        url: `${Config.API_URL}/address/`,
        data: data,
        headers: { "content-type": "application/json" },
        auth: Config.API_AUTH
      });
    } catch (error) {
      console.error(error.message);
    }
  }

  static async submitCampaign(data) {
    try {
      return await axios({
        method: 'post',
        url: `${Config.API_URL}/politician/`,
        data: data,
        headers: { "content-type": "application/json" },
        auth: Config.API_AUTH
      });
    } catch (error) {
      console.error(error.message);
    }
  }

  static async putCampaign(data) {
    try {
      return await axios({
        method: 'put',
        url: `${Config.API_URL}/campaign/`,
        data: data,
        headers: { "content-type": "application/json" },
        auth: Config.API_AUTH
      });
    } catch (error) {
      console.error(error.message);
    }
  }

  static async getCampaign(politician_id) {
    let response;

    try {
      response = await axios.get(`${Config.API_URL}/campaign/?politician_id=${politician_id}`);
    } catch (error) {
      console.error(error.message);
      alert(error.message);
    }
    return response.data;
  }

  static async postStance(data) {
    try {
      return await axios({
        method: 'post',
        url: `${Config.API_URL}/stance/`,
        data: data,
        headers: { "content-type": "application/json" },
        auth: Config.API_AUTH
      });
    } catch (error) {
      console.error(error.message);
    }
  }

  static async getStance(data) {
    try {
      return await axios({
        method: 'get',
        url: `${Config.API_URL}/stance/`,
        params: { politician_id: data },
        headers: { "content-type": "application/json" },
        auth: Config.API_AUTH
      });
    } catch (error) {
      console.error(error.message);
    }
  }
}
