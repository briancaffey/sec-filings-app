<template>
  <div>
    <q-table
      :loading="$store.getters['investors/getLoading']"
      :hide-bottom="false"
      dense
      row-key="id"
      :data="$store.getters['investors/getInvestors']"
      :pagination.sync="pagination"
      :requestServerInteraction="refreshData"
      @request="refreshData"
      hide-pagination
      :columns="$store.getters['investors/getColumns']"
    >
      <template #top-left>
        <q-btn
          type="a"
          :href="`/api/cik/${$store.getters['core/getPeriod'].value}/`"
          >Investors ({{ $store.getters["investors/getCount"] }})
        </q-btn>
      </template>
      <template v-slot:top-right>
        <q-input
          outlined
          dense
          placeholder="CIK or Investor Name"
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
          <q-td key="cik_number" :props="props">
            <q-btn color="blue" type="a" :href="`/cik/${props.row.cik_number}`">
              View {{ props.row.cik_number }}
            </q-btn>
          </q-td>
          <q-td key="filer_name" :props="props">
            {{ props.row.filer_name }}
          </q-td>
          <q-td key="total_periods_filed" :props="props">
            {{ props.row.total_periods_filed }}
          </q-td>
          <q-td key="current_period_holding_count" :props="props">
            {{ props.row.current_period_holding_count | currency }}
          </q-td>
          <q-td key="current_period_fund_size" :props="props">
            $ {{ props.row.current_period_fund_size | currency }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="current"
        :max="
          Math.ceil(
            $store.getters['investors/getCount'] /
              $store.getters['investors/getPagination'].rowsPerPage
          )
        "
        :max-pages="10"
        :direction-links="true"
        :boundary-links="true"
        size="sm"
      />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {};
  },
  methods: {
    refreshData(props) {
      this.$store.dispatch("investors/fetchData");
    }
  },
  watch: {
    period(newValue, oldValue) {
      if (newValue !== "-") {
        this.refreshData();
      }
    }
  },
  computed: {
    ...mapState("core", ["period"]),
    search: {
      get() {
        return this.$store.getters["investors/getSearch"];
      },
      set(v) {
        this.$store.dispatch("investors/setSearch", v);
      }
    },
    pagination: {
      get() {
        return this.$store.getters["investors/getPagination"];
      },
      set(v) {
        this.$store.dispatch("investors/setPagination", v);
      }
    },
    current: {
      get() {
        const currentPage = this.$store.getters["investors/getCurrentPage"];
        return currentPage;
      },
      set(v) {
        this.$store.dispatch("investors/setCurrentPage", v);
      }
    }
  }
};
</script>

<style scoped></style>
