import Vue from "vue";

const state = {
  accountStatus: {
    id: null,
    email: null,
    is_staff: null,
    is_superuser: null,
    stripe_customer_id: null,
    subscription_valid_through: null,
    is_premium: null
  }
};

const getters = {
  getAccountStatus: s => s.accountStatus
};

const actions = {
  fetchData: ({ commit, dispatch }, payload) => {
    Vue.prototype.$axios.post("/api/account/", payload).then(resp => {
      commit("setAccount", resp);
    });
  }
};

const mutations = {
  setAccount: (state, payload) => {
    state.accountStatus = payload.data;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
