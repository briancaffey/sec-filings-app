import Vue from "vue";

const state = {
  investors: [],
  loading: false,
  holdings: [],
  search: "",
  count: 1000,
  currentPage: 1,
  paginationLimit: 5,
  sortBy: "",
  descending: "true",
  rowsPerPage: null,
  columns: [
    {
      name: "cik_number",
      align: "left",
      label: "CIK",
      field: "filer_name",
      sortable: true
    },
    {
      name: "filer_name",
      align: "left",
      label: "Investor",
      field: "investor",
      sortable: true
    },
    {
      name: "total_periods_filed",
      align: "left",
      label: "Periods Filed",
      field: "total_periods_filed",
      sortable: true
    },
    {
      name: "current_period_holding_count",
      align: "left",
      label: "Current Period Holdings Count",
      field: "current_period_holding_count",
      sortable: true
    },
    {
      name: "current_period_fund_size",
      align: "left",
      label: "Current Period Fund Size",
      field: "current_period_fund_size",
      sortable: true
    }
  ]
};

const getters = {
  getInvestors: s => s.investors,
  getLoading: s => s.loading,
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
  fetchData: ({ commit, getters, rootGetters }) => {
    commit("setLoading", true);
    const period = rootGetters["core/getPeriod"].value;
    if (period === "-") return;
    Vue.prototype.$axios
      .get(`/api/cik/${period}/`, { params: getters.getQueryParams })
      .then(resp => {
        commit("setInvestors", resp.data);
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
  setInvestors: (state, payload) => {
    state.investors = payload.results;
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
