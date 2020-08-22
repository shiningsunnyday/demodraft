import axios from 'axios';
import * as Config from '../config.json';

const apiClient = axios.create({
  baseURL: Config.API_URL,
  auth: Config.API_AUTH,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  }
});

export class ApiUtil {
  
  static async getPolicies() {
    const policiesPromise = await apiClient.get('/policies/');
    return policiesPromise.data;
  }

  static async getPolicy(id) {
    const policyPromise = await apiClient.get(`/policy/?id=${id}`);
    return policyPromise.data;
  }

  static async getPolicyComments(id) {
    const policyCommentsPromise = await apiClient.get(`/thread/?policy_id=${id}`);
    return policyCommentsPromise.data;
  }

  static async getThreadFromComment(id) {
    const threadPromise = await apiClient.get(`/thread/?thread_id=${id}`);
    return {
      data: threadPromise.data,
      replies: threadPromise.data.slice(1),
      leadComment: threadPromise.data[0]
    };
  }

  static async deleteThread(thread_id, username) {
    let response;
    try {
      let payload = {thread_id: thread_id, username: username};
      console.log(payload);
      response = await axios.delete(`${Config.API_URL}/thread/`, { data: payload });
    } catch (error) {
      console.error(error.message);
    }
    return response.data;
  }

  static async deleteComment(comment_id, username) {
    let response;
    try {
      let payload = {prev_comment_id: comment_id, username: username};
      console.log(payload);
      response = await axios.delete(`${Config.API_URL}/comment/`, { data: payload });
    } catch (error) {
      console.error(error.message);
    }
    // return response.data;
  }

  static async putPolicyLike(id) {
    try {
      const policyLikePromise = await apiClient.put(`/policy/`, { id: id });
      return policyLikePromise.data.likes;
    } catch (error) {
      console.error(error.message);
    }
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
    const putCampaignPromise = await apiClient.put('/campaign/', data);
    return putCampaignPromise.data;
  }

  static async getCampaign(politician_id) {
    let response;

    try {
      response = await axios.get(`${Config.API_URL}/campaign/?politician_id=${politician_id}`);
    } catch (error) {
      console.error(error.message);
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
    return await axios({
      method: 'get',
      url: `${Config.API_URL}/stance/`,
      params: { politician_id: data },
      headers: { "content-type": "application/json" },
      auth: Config.API_AUTH
    });
  }

  static async getModifiedPolitician(req) {
    const { user } = req;

    if (!user) {
      alert('Missing req for getModifiedPolitician');
      return;
    }

    try {
      const politician = await ApiUtil.getSelectedPolitician(user.politician_id);
      const stancePromise = await ApiUtil.getStance(user.politician_id);
      const campaign = await ApiUtil.getCampaign(user.politician_id);
      const allPoliticianStances = stancePromise.data;
      return {
        id: politician.id,
        firstName: politician.first,
        lastName: politician.last,
        state: politician.state,
        actblue: campaign.actblue,
        fundraiseGoal: campaign.fundraise_goal,
        fundraised: campaign.fundraised,
        position: campaign.name,
        approved: politician.approved,
        endorsed: allPoliticianStances,
      };
    } catch (error) {
      alert('Oops, something went wrong modifying a politician!');
      console.error(error);
    }
  }
}
