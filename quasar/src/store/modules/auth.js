import Vue from "vue";

const state = {
  authenticated: localStorage.getItem("authenticated") || ""
};

const getters = {
  getAuthenticated: s => s.authenticated
};

const actions = {
  login: ({ commit, dispatch }, payload) => {
    Vue.prototype.$axios.post("/api/login/", payload).then(resp => {
      commit("authSuccess", resp);
    });
  }
};

const mutations = {
  authSuccess: (state, payload) => {
    localStorage.setItem("authenticated", "success");
    state.authenticated = "success";
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
