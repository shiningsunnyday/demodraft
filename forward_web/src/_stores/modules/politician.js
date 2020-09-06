import * as types from '@/_stores/mutation-types';
import { ApiUtil } from '@/_utils/api-utils.js';

const politician = JSON.parse(sessionStorage.getItem('politicianState'));
export const politicianStore = {
  state: politician ? { politician } : { politician: {} },
  mutations: {
    [types.SET_POLITICIAN]: (state, payload) => {
      state.politician = payload;
    },
    [types.UPDATE_CAMPAIGN]: (state, payload) => {
      state.politician.actblue = payload.actblue;
      state.politician.fundraiseGoal = payload.fundraiseGoal;
    },
    [types.UPDATE_ENDORSED]: (state, payload) => {
      state.politician.endorsed = payload;
    }
  },
  actions: {
    setPolitician: async ({ commit }, user) => {
      const politician = await ApiUtil.getModifiedPolitician({ user });
      sessionStorage.setItem('politicianState', JSON.stringify(politician));
      commit(types.SET_POLITICIAN, politician);
    },
    updateCampaign: async ({ commit, getters }, req) => {
      commit(types.UPDATE_CAMPAIGN, req);
      sessionStorage.setItem('politicianState', JSON.stringify(getters.getPolitician));
    },
    updateEndorsed: async ({ commit, getters }, req) => {
      commit(types.UPDATE_ENDORSED, req);
      sessionStorage.setItem('politicianState', JSON.stringify(getters.getPolitician));
    }
  },
  getters: {
    getPolitician: (state) => {
      return state.politician;
    },
  },
};
