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

export class PoliticianService {
  static async getAllPoliticians() {
    const allPoliticiansPromise = axios.get(`/politician/`);
    const allPoliticians = await allPoliticiansPromise;
    return allPoliticians.data;
  }

  static async getPolitician(id) {
    const selectedPoliticianPromise = axios.get(`/politician/?politician_id=${id}`);
    const selectedPolitician = await selectedPoliticianPromise;
    return selectedPolitician.data;
  }

  static async postStance(data) {
    return await axios.post(`/stance/`, data);
  }

  static async getAllStances(id) {
    const getAllStancesPromise = axios.get(`/stance/?politician_id=${id}`);
    const allStances = await getAllStancesPromise;
    return allStances.data;
  }

  static async postPlan(req, user) {
   if (!user.id || user.politician_id !== req.politician_id) {
     return;
   }
   return await axios.post(`/plan/`, req);
  }

  static async getPlan(req) {
    return await axios.get(`/plan/`, {
      params: {
        politician_id: req.politician_id,
        policy_id: req.policy_id
      }
    });
   }

   static async getPoliticianArea(isRandom) {
    return await axios.get(`/area/`, {
      params: {
        random: isRandom,
      }
    });
   }
}