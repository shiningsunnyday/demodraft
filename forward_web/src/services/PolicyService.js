import axios from 'axios';
import * as Config from '../config.json';

axios.defaults.baseURL = Config.API_URL;
axios.defaults.auth = Config.API_AUTH;
axios.defaults.headers.post['Content-Type'] = 'application/json';

export class PolicyService {
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

  static async likePolicy(req) {
    const { id, username} = req;
    if (!id || !username) {
      return;
    }
    
    const policyLikePromise = axios.put(`/policy/`, { 
      id: id,
      username: username
    });

    const policyLike = await policyLikePromise;
    return policyLike.data.likes;
  }
}