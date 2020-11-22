import Vue from "vue";
import { Notify } from "quasar";

const state = {
  loading: false,
  filings: [],
  search: "",
  count: 100,
  currentPage: 1,
  paginationLimit: 5,
  sortBy: "",
  descending: "true",
  rowsPerPage: null,
  columns: [
    {
      name: "cik",
      align: "left",
      label: "CIK",
      field: "cik",
      sortable: true
    },
    {
      name: "filer_name",
      align: "left",
      label: "Filer Name",
      field: "filer_name",
      sortable: true
    },
    {
      name: "total_value",
      align: "left",
      label: "Total Value",
      field: "total_value",
      sortable: true
    },
    {
      name: "filename",
      align: "left",
      label: "File",
      field: "filename",
      sortable: true
    },
    {
      name: "date_filed",
      align: "left",
      label: "Date Filed",
      field: "date_filed",
      sortable: true
    }
  ]
};

const getters = {
  getSearch: s => s.search,
  getLoading: s => s.loading,
  getFilings: s => s.filings,
  getColumns: s => s.columns,
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
      .get("/api/filings/", { params: getters.getQueryParams })
      .then(resp => {
        commit("setFilings", resp.data);
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
  setSearch: ({ commit, dispatch }, payload) => {
    commit("setSearch", payload);
    dispatch("fetchData");
  }
};

const mutations = {
  setSearch: (state, payload) => {
    state.search = payload;
  },
  setLoading: (state, payload) => {
    state.loading = payload;
  },
  setFilings: (state, payload) => {
    state.filings = payload.results;
    state.count = payload.count;
  },
  setCurrentPage: (state, payload) => {
    state.currentPage = payload;
  },
  setPagination: (state, payload) => {
    state.sortBy = payload.sortBy;
    state.descending = payload.descending;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
