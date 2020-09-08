import axios from 'axios';
import * as Config from '../config.json';

axios.defaults.baseURL = Config.API_URL;
axios.defaults.auth = Config.API_AUTH;
axios.defaults.headers.post['Content-Type'] = 'application/json';

export class AuthUtil {
  static async login(user) {
    if (!user) {
      return;
    }

    const payload = { 
      username: user.username, 
      password: user.password 
    };

    const loginPromise = axios.post('/login/', payload);
    const login = await loginPromise;
    const {
      id,
      username,
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
      first_name: first_name,
      last_name: last_name,
      approved: approved ? approved : undefined,
      isMod: login.status === 204 ? false : is_mod,
      politician_id: politician_id ? politician_id : undefined,
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
}