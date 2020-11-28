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
  },

  logout: ({ commit }) => {
    Vue.prototype.$axios.post("/api/logout/").then(resp => {
      commit("logout", resp);
    });
  }
};

const mutations = {
  authSuccess: (state, payload) => {
    localStorage.setItem("authenticated", "success");
    state.authenticated = "success";
  },
  logout: (state, payload) => {
    localStorage.removeItem("authenticated");
    state.authenticated = "";
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
