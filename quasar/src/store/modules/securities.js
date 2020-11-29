import Vue from "vue";

const state = {
  securities: [],
  loading: false,
  search: "",
  count: 0,
  currentPage: 1,
  paginationLimit: 5,
  sortBy: "",
  descending: "true",
  rowsPerPage: null,
  columns: [
    {
      name: "cusip_number",
      align: "left",
      label: "CUSIP",
      field: "cusip_number",
      sortable: true
    },
    {
      name: "company_name",
      align: "left",
      label: "Company Name",
      field: "company_name",
      sortable: true
    },
    {
      name: "held_by_funds",
      align: "left",
      label: "Held By Funds",
      field: "held_by_funds",
      sortable: true
    },
    {
      name: "holding_count",
      align: "left",
      label: "Holding Count",
      field: "holding_count",
      sortable: true
    }
  ]
};

const getters = {
  getSecurities: s => s.securities,
  getLoading: s => s.loading,
  getColumns: s => s.columns,
  getSecuritiesSearch: s => s.search,
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
      .get("/api/cusip/", { params: getters.getQueryParams })
      .then(resp => {
        commit("setSecurities", resp.data);
        commit("setLoading", false);
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
  setSearch: ({ commit, dispatch }, payload) => {
    commit("setSearch", payload);
    dispatch("fetchData");
  }
};

const mutations = {
  setLoading: (state, payload) => {
    state.loading = payload;
  },
  setSecurities: (state, payload) => {
    state.securities = payload.results;
    state.count = payload.count;
  },
  setCurrentPage: (state, payload) => {
    state.currentPage = payload;
  },
  setPagination: (state, payload) => {
    state.sortBy = payload.sortBy;
    state.descending = payload.descending;
  },
  setSearch: (state, payload) => {
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
