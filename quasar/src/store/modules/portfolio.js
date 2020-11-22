import Vue from "vue";
import { Notify } from "quasar";
import router from "../../router";

const state = {
  cik: null,
  loading: false,
  holdings: [],
  search: "",
  count: 100,
  currentPage: 1,
  paginationLimit: 5,
  sortBy: "",
  descending: "true",
  rowsPerPage: null,
  columns: [
    {
      name: "cusip",
      align: "left",
      label: "CUSIP",
      field: "cusip",
      sortable: true
    },
    {
      name: "company_name",
      align: "left",
      label: "Security",
      field: "company_name",
      sortable: false
    },
    // {
    //   name: "historical",
    //   align: "left",
    //   label: "Historical",
    //   field: "historical",
    //   sortable: false
    // },
    // {
    //   name: "change",
    //   align: "left",
    //   label: "Change",
    //   field: "change",
    //   sortable: true
    // },
    {
      name: "total",
      align: "left",
      label: "Total",
      field: "total",
      sortable: true
    },
    // {
    //   name: "value_delta",
    //   align: "left",
    //   label: "Value Delta",
    //   field: "value_delta",
    //   sortable: true
    // },
    {
      name: "sshPrnamt",
      align: "left",
      label: "Shares",
      field: "sshPrnamt",
      sortable: true
    },
    // {
    //   name: "shares_delta",
    //   align: "left",
    //   label: "Shares Delta",
    //   field: "shares_delta",
    //   sortable: true
    // },
    {
      name: "percentage",
      align: "left",
      label: "Weight",
      field: "percentage",
      sortable: true
    }
    // {
    //   name: "weight_delta",
    //   align: "left",
    //   label: "Weight Delta",
    //   field: "weight_delta",
    //   sortable: true
    // }
  ]
};

const getters = {
  getCik: s => s.cik,
  getLoading: s => s.loading,
  getHoldings: s => s.holdings,
  getColumns: s => s.columns,
  getHoldingSearch: s => s.search,
  getPaginationLimit: s => s.paginationLimit,
  getCount: s => s.count,
  getCurrentPage: s => s.currentPage,
  getRowsPerPage: s => s.rowsPerPage,
  getPagination: s => {
    return {
      sortBy: s.sortBy,
      descending: s.descending,
      rowsPerPage: s.paginationLimit,
      pagination: {
        rowsPerPage: s.paginationLimit,
        pagesNumber: s.count
      }
    };
  },
  getQueryParams: s => {
    let desc = s.descending === false ? "" : "-";
    const sort = s.sortBy || "";
    if (sort === "") {
      desc = "";
    }
    return {
      offset: (s.currentPage - 1) * s.paginationLimit,
      limit: s.paginationLimit,
      sorting: `${desc}${sort}`,
      search: s.search
    };
  }
};

const actions = {
  fetchData: ({ commit, getters, rootGetters }, payload) => {
    if (rootGetters["core/getPeriod"].value === "-") return;
    const cik = getters.getCik;
    const period = rootGetters["core/getPeriod"].value;
    Vue.prototype.$axios
      .get(`/api/cik/${cik}/portfolio/period/`, {
        params: { period, ...getters.getQueryParams }
      })
      .then(resp => {
        commit("setHoldings", resp.data);
        commit("setLoading", false);
      })
      .catch(err => {
        commit("setLoading", false);
        Notify.create({
          message: err.response.data.detail
        });
      });
  },
  setCurrentPage: ({ commit, dispatch }, payload) => {
    commit("setCurrentPage", payload);
    dispatch("fetchData");
  },
  setPagination: ({ commit, dispatch }, payload) => {
    commit("setPagination", payload);
    dispatch("fetchData");
  },
  setHoldingSearch: ({ commit, dispatch }, payload) => {
    commit("setHoldingSearch", payload);
    dispatch("fetchData");
  }
};

const mutations = {
  setCik: (state, payload) => {
    state.cik = payload;
  },
  setLoading: (state, payload) => {
    state.loading = payload;
  },
  setHoldings: (state, payload) => {
    state.holdings = payload.results;
    state.count = payload.count;
  },
  setCurrentPage: (state, payload) => {
    state.currentPage = payload;
  },
  setPagination: (state, payload) => {
    state.sortBy = payload.sortBy;
    state.descending = payload.descending;
  },
  setHoldingSearch: (state, payload) => {
    state.search = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
