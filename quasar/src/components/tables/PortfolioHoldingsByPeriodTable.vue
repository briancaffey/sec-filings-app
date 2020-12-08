<template>
  <div class="wrapper">
    <q-table
      :loading="$store.getters['portfolio/getLoading']"
      :hide-bottom="false"
      dense
      :title="`Holdings (${$store.getters['core/getPeriod'].label})`"
      row-key="id"
      :data="$store.getters['portfolio/getHoldings']"
      :pagination.sync="pagination"
      :requestServerInteraction="refreshData"
      @request="refreshData"
      hide-pagination
      :columns="$store.getters['portfolio/getColumns']"
    >
      <template #top-left>
        <q-btn
          type="a"
          :href="
            `/api/cik/${$route.params.cik}/portfolio/${$store.getters['core/getPeriod'].value}/`
          "
        >
          {{ `Holdings (${$store.getters["core/getPeriod"].label})` }}
        </q-btn>
      </template>
      <template v-slot:top-right>
        <q-input
          outlined
          dense
          placeholder="Filter Holdings"
          debounce="1000"
          v-model="holdingSearch"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="cusip" :props="props">
            <q-btn
              color="blue"
              type="a"
              :href="`/cusip/${props.row.cusip_number}`"
            >
              View {{ props.row.cusip_number }}
            </q-btn>
          </q-td>
          <q-td key="company_name" :props="props">
            {{ props.row.company_name }}
          </q-td>
          <!-- <q-td key="change" :props="props">
            <template v-if="props.row.delta_values.shares > 0">
              <span style="color:green">
                <b>Add</b>
              </span>
            </template>
            <template v-else-if="props.row.delta_values.shares < 0">
              <span style="color:red">
                <b>Reduce</b>
              </span>
            </template>
            <template v-else>
              <span style="color:blue ">
                <b>New</b>
              </span>
            </template>
          </q-td> -->
          <q-td key="total" :props="props">
            <b>{{ props.row.total | currency }}</b>
          </q-td>
          <!-- <q-td key="value_delta" :props="props">
            <template v-if="props.row.delta_values.total > 0">
              <span style="color:green">
                <b>{{ (props.row.delta_values.total * 100) | currency }}%</b>
              </span>
            </template>
            <template v-else-if="props.row.delta_values.total < 0">
              <span style="color:red">
                <b>{{ (props.row.delta_values.total * 100) | currency }}%</b>
              </span>
            </template>
            <template v-else>
              <span>
                <b>{{ (props.row.delta_values.total * 100) | currency }}</b>
              </span>
            </template>
          </q-td> -->
          <q-td key="sshPrnamt" :props="props">
            <b>{{ props.row.sshPrnamt | currency }}</b>
          </q-td>
          <!-- <q-td key="shares_delta" :props="props">
            <template v-if="props.row.delta_values.shares > 0">
              <span style="color:green">
                <b>{{ (props.row.delta_values.shares * 100) | currency }}%</b>
              </span>
            </template>
            <template v-else-if="props.row.delta_values.shares < 0">
              <span style="color:red">
                <b>{{ (props.row.delta_values.shares * 100) | currency }}%</b>
              </span>
            </template>
            <template v-else>
              <span>
                <b>{{ (props.row.delta_values.shares * 100) | currency }}</b>
              </span>
            </template>
          </q-td> -->
          <q-td key="percentage" :props="props">
            <b>{{ props.row.percentage | currency }}</b>
          </q-td>
          <!-- <q-td key="weight_delta" :props="props">
            <template v-if="props.row.delta_values.weight > 0">
              <span style="color:green">
                <b>{{ (props.row.delta_values.weight * 100) | currency }}%</b>
              </span>
            </template>
            <template v-else-if="props.row.delta_values.weight < 0">
              <span style="color:red">
                <b>{{ (props.row.delta_values.weight * 100) | currency }}%</b>
              </span>
            </template>
            <template v-else>
              <span>
                <b>{{ (props.row.delta_values.weight * 100) | currency }}</b>
              </span>
            </template>
          </q-td> -->
        </q-tr>
      </template></q-table
    >
    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="current"
        :max="
          Math.ceil(
            $store.getters['portfolio/getCount'] /
              $store.getters['portfolio/getPagination'].rowsPerPage
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
  name: "HoldingsTable",
  data() {
    return {};
  },
  methods: {
    refreshData(props) {
      this.$store.dispatch("portfolio/fetchData");
    }
  },
  watch: {
    period(newValue, oldValue) {
      if (newValue.value !== "-") {
        this.refreshData();
      }
    }
  },
  computed: {
    ...mapState("core", ["period"]),
    holdingSearch: {
      get() {
        return this.$store.getters["portfolio/getHoldingSearch"];
      },
      set(v) {
        this.$store.dispatch("portfolio/setHoldingSearch", v);
      }
    },
    pagination: {
      get() {
        return this.$store.getters["portfolio/getPagination"];
      },
      set(v) {
        this.$store.dispatch("portfolio/setPagination", v);
      }
    },
    current: {
      get() {
        const currentPage = this.$store.getters["portfolio/getCurrentPage"];
        return currentPage;
      },
      set(v) {
        this.$store.dispatch("portfolio/setCurrentPage", v);
      }
    }
  },
  created() {
    this.$store.commit("portfolio/setCik", this.$route.params.cik);
    this.$store.dispatch("portfolio/fetchData");
  }
};
</script>
<style>
.wrapper {
  margin-bottom: 10px;
}
</style>
