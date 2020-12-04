<template>
  <div>
    <q-table
      :title="`Funds holding ${$store.getters['cusip/getCompanyName']}`"
      :columns="$store.getters['cusip/holdingCiks/getColumns']"
      :data="$store.getters['cusip/holdingCiks/getData']"
      :filter="filter"
      :loading="loading"
    >
      <template #top-left>
        <q-btn
          type="a"
          style="text-decoration:none; color:black"
          :href="
            `/api/cusip/${$route.params.cusip}/cik/${$store.getters['core/getPeriod'].value}/`
          "
        >
          {{
            `Funds holding ${$store.getters["cusip/getCompanyName"]} (${$store.getters["cusip/holdingCiks/getData"].length})`
          }}
        </q-btn>
      </template>
      <template v-slot:top-right>
        <q-input
          outlined
          dense
          placeholder="Search by CIK or Filer Name"
          debounce="1000"
          v-model="filter"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="cik_number" :props="props">
            <router-link
              style="text-decoration:none;"
              :to="`/cik/${props.row.cik_number}`"
            >
              <q-btn color="blue">
                {{ props.row.cik_number }}
              </q-btn>
            </router-link>
          </q-td>
          <q-td key="filer_name" :props="props">
            {{ props.row.filer_name }}
          </q-td>
          <q-td key="total_value" :props="props">
            $ {{ props.row.total_value | currency }}
          </q-td>
          <q-td key="total_shares" :props="props">
            {{ props.row.total_shares | currency }}
          </q-td>
          <q-td key="first_filed" :props="props">
            {{ props.row.first_filed }}
          </q-td>
          <q-td key="percent_of_portfolio" :props="props">
            {{ props.row.percent_of_portfolio | percentage(3) }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      filter: ""
    };
  },
  computed: {
    ...mapState("core", ["period"]),
    loading: {
      get() {
        return this.$store.getters["cusip/holdingCiks/getLoading"];
      }
    }
  },
  methods: {
    fetchData() {
      const { cusip } = this.$route.params;
      this.$store.dispatch("cusip/holdingCiks/fetchData", { cusip });
    }
  },
  watch: {
    period(newValue, oldValue) {
      if (newValue.value !== "-") {
        this.fetchData();
      }
    }
  }
};
</script>

<style scoped></style>
