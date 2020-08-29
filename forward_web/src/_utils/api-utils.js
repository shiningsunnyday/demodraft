import axios from 'axios';
import * as Config from '../config.json';
axios.defaults.baseURL = Config.API_URL;
axios.defaults.auth = Config.API_AUTH;
axios.defaults.headers.post['Content-Type'] = 'application/json';

export class ApiUtil {
  
  static async getPolicies() {
    const policiesPromise = await axios.get('/policies/');
    return policiesPromise.data;
  }

  static async getPolicy(id) {
    const policyPromise = await axios.get(`/policy/?id=${id}`);
    return policyPromise.data;
  }

  static async getPolicyComments(id) {
    const policyCommentsPromise = await axios.get(`/thread/?policy_id=${id}`);
    return policyCommentsPromise.data;
  }

  static async getPoliticianComments(id) {
    const polCommentsPromise = await axios.get(`/thread/?politician_id=${id}`);
    return polCommentsPromise.data;
  }

  static async getThreadFromComment(id) {
    const threadPromise = await axios.get(`/thread/?thread_id=${id}`);
    return {
      data: threadPromise.data,
      replies: threadPromise.data.slice(1),
      leadComment: threadPromise.data[0],
      lastComment: threadPromise.data[threadPromise.data.length - 1]
    };
  }

  static async deleteThread(thread_id, username) {
    const payload = { thread_id: thread_id, username: username };
    const deleteThreadPromise = await axios.post(`/thread/`, payload );
    return deleteThreadPromise.data;
  }

  static async deleteComment(comment_id, username) {
    const payload = { prev_comment_id: comment_id, username: username };
    const deleteCommentPromise = await axios.post(`/comment/`, payload );
    return deleteCommentPromise.data;
  }

  static async putPolicyLike(id) {
    const policyLikePromise = await axios.put(`/policy/`, { id: id });
    return policyLikePromise.data.likes;
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

  /**
   * Posts an address to backend on address search
   * @param {Object} data - { username, password, address } 
   */
  static async postAddress(data) {
    const postAddressPromise = await axios.post(`/address/`, data);
    return postAddressPromise.data;
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
    const putCampaignPromise = await axios.put('/campaign/', data);
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

  static async getUserScore(req) {
    const payload = { 
      user_id: req.user_id, 
      username: req.username, 
      password: req.password 
    };
    const userPromise = await axios.post(`/users/`, payload);
    return userPromise.data.score;
  }
}
