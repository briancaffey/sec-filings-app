<template>
  <div class="contents">
    <q-table
      :loading="$store.getters['filings/getLoading']"
      :hide-bottom="false"
      dense
      title="Filings"
      row-key="id"
      :data="$store.getters['filings/getFilings']"
      :pagination.sync="pagination"
      :requestServerInteraction="refreshData"
      @request="refreshData"
      hide-pagination
      :columns="$store.getters['filings/getColumns']"
    >
      <template v-slot:top-right>
        <q-input
          outlined
          small
          dense
          placeholder="Filter filings by CIK or Name"
          debounce="1000"
          v-model="search"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="cik" :props="props">
            <q-btn
              color="black"
              type="a"
              :href="`/cik/${props.row.cik_number}`"
            >
              {{ props.row.cik_number }}
            </q-btn>
          </q-td>
          <q-td key="filer_name" :props="props">
            {{ props.row.filer_name }}
          </q-td>
          <q-td key="total_value" :props="props">
            {{ props.row.total_value }}
          </q-td>
          <q-td key="filename" :props="props">
            <q-btn
              color="black"
              type="a"
              :href="`https://www.sec.gov/Archives/${props.row.filename}`"
            >
              View
            </q-btn>
          </q-td>
          <q-td key="date_filed" :props="props">
            {{ props.row.date_filed }}
          </q-td>
        </q-tr>
      </template></q-table
    >
    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="current"
        :max="
          Math.ceil(
            $store.getters['filings/getCount'] /
              $store.getters['filings/getPagination'].rowsPerPage
          )
        "
        :max-pages="10"
        :direction-links="true"
        :boundary-links="true"
        size="sm"
      />
      <q-btn type="a" :href="`/api/filings/`"
        ><pre>{{ `/api/filings/` }}</pre></q-btn
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "FilingsTable",
  methods: {
    refreshData(props) {
      this.$store.dispatch("filings/fetchData");
    }
  },
  computed: {
    search: {
      get() {
        return this.$store.getters["filings/getSearch"];
      },
      set(v) {
        this.$store.dispatch("filings/setSearch", v);
      }
    },
    pagination: {
      get() {
        return this.$store.getters["filings/getPagination"];
      },
      set(v) {
        this.$store.dispatch("filings/setPagination", v);
      }
    },
    current: {
      get() {
        const currentPage = this.$store.getters["filings/getCurrentPage"];
        return currentPage;
      },
      set(v) {
        this.$store.dispatch("filings/setCurrentPage", v);
      }
    }
  },
  created() {
    this.$store.dispatch("filings/fetchData");
  }
};
</script>
<style></style>
