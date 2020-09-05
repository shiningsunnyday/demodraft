import axios from 'axios';
import * as Config from '../config.json';
axios.defaults.baseURL = Config.API_URL;
axios.defaults.auth = Config.API_AUTH;
axios.defaults.headers.post['Content-Type'] = 'application/json';

export class ApiUtil {
  static async login(user) {
    if (!user) {
      return;
    }

    const payload = { username: user.username, password: user.password };
    const loginPromise = axios.post('/login/', payload);
    const login = await loginPromise;
    const {
      id,
      username,
      email,
      password,
      approved,
      first_name,
      last_name,
      politician_id,
      is_mod,
    } = login.data;

    return {
      id: id,
      username: username,
      password: password,
      email: email,
      first_name: first_name,
      last_name: last_name,
      approved: approved,
      isMod: login.status === 204 ? false : is_mod,
      politician_id: politician_id,
      campaignPending: user.campaignPending,
    };
  }

  static async signUp(user) {
    if (!user) {
      return;
    }

    const payload = { 
      username: user.username, 
      email: user.email,
      password: user.password,
      first_name: user.first_name,
      last_name: user.last_name,
    };

    const signUpPromise = axios.post('/login/', payload);
    const signUp = await signUpPromise;

    const {
      id,
      username,
      email,
      password,
      first_name,
      last_name,
    } = signUp.data;

    return {
      id: id,
      username: username,
      password: password,
      email: email,
      first_name: first_name,
      last_name: last_name,
      campaignPending: user.campaignPending,
    };
  }

  static async getPolicies() {
    const policiesPromise = axios.get('/policies/');
    const policies = await policiesPromise;
    return policies.data;
  }

  static async getPolicy(id) {
    const policyPromise = axios.get(`/policy/?id=${id}`);
    const policy = await policyPromise;
    return policy.data;
  }
  static async getComments(id, section) {
    try {
      const commentsPromise = axios.get(`/thread/?${section}_id=${id}`);
      const comments = await commentsPromise;
      return comments.data;
    } catch (error) {
      alert(`Error ${error.response.status}: Something when wrong updating this ${section}'s comments`);
      console.log(error);
    }
    
  }

  static async getThreadFromComment(id) {
    const threadPromise = axios.get(`/thread/?thread_id=${id}`);
    const thread = await threadPromise;
    return {
      data: thread.data,
      replies: thread.data.slice(1),
      leadComment: thread.data[0],
      lastComment: thread.data[thread.data.length - 1]
    };
  }

  static async deleteThread(thread_id, username) {
    const payload = { thread_id: thread_id, username: username };
    const deleteThreadPromise = axios.post(`/thread/`, payload );
    const deleteThread = await deleteThreadPromise;
    return deleteThread.data;
  }

  static async deleteComment(comment_id, username) {
    const payload = { prev_comment_id: comment_id, username: username };
    const deleteCommentPromise = axios.post(`/comment/`, payload );
    const deleteComments = await deleteCommentPromise;
    return deleteComments.data;
  }

  static async putPolicyLike(id) {
    const policyLikePromise = axios.put(`/policy/`, { id: id });
    const policyLike = await policyLikePromise;
    return policyLike.data.likes;
  }

  static async commentLike(id) {
    const payload = { comment_id: id };
    const commentLikePromise = axios.patch(`/comment/`, payload);
    const commentLike = await commentLikePromise;
    return commentLike.data.likes;
  }

  static async addNewThread(data) {
    try {
      await axios.post(`/thread/`, data);
    } catch (error) {
      alert('error on addNewThread');
      console.log(error);
    }
  }

  static async addNewReply(data) {
    try {
      await axios.post(`/comment/`, data);
    } catch (error) {
      alert('error on addNewReply');
      console.log(error);
    }
  }

  static async getAllPoliticians() {
    const allPoliticiansPromise = axios.get(`/politician/`);
    const allPoliticians = await allPoliticiansPromise;
    return allPoliticians.data;
  }

  static async getSelectedPolitician(id) {
    const selectedPoliticianPromise = axios.get(`/politician/?politician_id=${id}`);
    const selectedPolitician = await selectedPoliticianPromise;
    return selectedPolitician.data;
  }

  static async postAddress(data) {
    const postAddressPromise = axios.post(`/address/`, data);
    const postAddress = await postAddressPromise;
    return postAddress.data;
  }

  static async submitCampaign(data) {
    return await axios.post(`/politician/`, data);
  }

  static async putCampaign(data) {
    const putCampaignPromise = axios.put('/campaign/', data);
    const campaign = await putCampaignPromise;
    return campaign.data;
  }

  static async getCampaign(politician_id) {
    const getCampaignPromise = axios.get(`/campaign/?politician_id=${politician_id}`);
    const campaign = await getCampaignPromise;
    return campaign.data;
  }

  static async postStance(data) {
    return await axios.post(`/stance/`, data);
  }

  static async getStance(data) {
    return await axios.get(`/stance/?politician_id=${data}`);
  }

  static async getModifiedPolitician(req) {
    const { user } = req;

    if (!user) {
      alert('Missing req for getModifiedPolitician');
      return;
    }

    try {
      const politician = await ApiUtil.getSelectedPolitician(user.politician_id);
      const stance = await ApiUtil.getStance(user.politician_id);
      const campaign = await ApiUtil.getCampaign(user.politician_id);
      const allPoliticianStances = stance.data;
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
    const userScorePromise = axios.post(`/users/`, payload);
    const userScore = await userScorePromise;
    return userScore.data.score;
  }
}
