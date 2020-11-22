import Vue from "vue";
import { Notify } from "quasar";

const state = {
  loading: false,
  holdings: [],
  search: "",
  count: null,
  currentPage: 1,
  paginationLimit: 5,
  sortBy: "",
  descending: "true",
  rowsPerPage: null,
  columns: [
    {
      name: "id",
      align: "left",
      label: "ID",
      field: "id",
      sortable: true
    },
    {
      name: "investor",
      align: "left",
      label: "Investor",
      field: "investor",
      sortable: false
    },
    {
      name: "historical",
      align: "left",
      label: "Historical",
      field: "historical",
      sortable: false
    },
    {
      name: "nameOfIssuer",
      align: "left",
      label: "Name of Issuer",
      field: "nameOfIssuer",
      sortable: true
    },
    {
      name: "value",
      align: "left",
      label: "Value",
      field: "value",
      sortable: true
    },
    {
      name: "titleOfClass",
      align: "left",
      label: "Title of Class",
      field: "titleOfClass",
      sortable: true
    },
    {
      name: "cusip",
      align: "left",
      label: "CUSIP",
      field: "cusip",
      sortable: true
    },
    {
      name: "sshPrnamt",
      align: "left",
      label: "sshPrnamt",
      field: "sshPrnamt",
      sortable: true
    },
    {
      name: "sshPrnamtType",
      align: "left",
      label: "sshPrnamtType",
      field: "sshPrnamtType"
    },
    {
      name: "investmentDiscretion",
      align: "left",
      label: "Investment Discretion",
      field: "investmentDiscretion"
    },
    {
      name: "putCall",
      align: "left",
      label: "Put Call",
      field: "putCall"
    },
    {
      name: "otherManager",
      align: "left",
      label: "Other Manager",
      field: "otherManager"
    },
    {
      name: "sole",
      align: "left",
      label: "SOLE",
      field: "sole",
      sortable: true
    },
    {
      name: "shared",
      align: "left",
      label: "SHARED",
      field: "shared",
      sortable: true
    },
    {
      name: "nonee",
      align: "left",
      label: "NONE",
      field: "nonee",
      sortable: true
    },
    {
      name: "filing",
      align: "left",
      label: "FILING",
      field: "filing"
    }
  ]
};

const getters = {
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
  fetchData: ({ commit, getters }) => {
    commit("setLoading", true);
    Vue.prototype.$axios
      .get("/api/holdings/", { params: getters.getQueryParams })
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
