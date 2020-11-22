<template>
  <div class="contents">
    <q-table
      :loading="$store.getters['holdings/getLoading']"
      :hide-bottom="false"
      dense
      title="All Holdings"
      row-key="id"
      :data="$store.getters['holdings/getHoldings']"
      :pagination.sync="pagination"
      :requestServerInteraction="refreshData"
      @request="refreshData"
      hide-pagination
      :columns="$store.getters['holdings/getColumns']"
    >
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
          <q-td key="id" :props="props">
            {{ props.row.id }}
          </q-td>
          <q-td key="investor" :props="props">
            <q-btn
              color="blue"
              type="a"
              :href="`/cik/${props.row.filing.cik.cik_number}`"
            >
              View {{ props.row.filing.cik.cik_number }}
            </q-btn>
          </q-td>
          <q-td key="historical" :props="props">
            <q-btn
              color="black"
              type="a"
              :href="
                `/holdings/${props.row.filing.cik.cik_number}/historical/${props.row.cusip.cusip_number}/`
              "
            >
              View
            </q-btn>
          </q-td>
          <q-td key="nameOfIssuer" :props="props">
            {{ props.row.nameOfIssuer }}
          </q-td>
          <q-td key="value" :props="props">
            {{ props.row.value }}
          </q-td>
          <q-td key="titleOfClass" :props="props">
            {{ props.row.titleOfClass }}
          </q-td>
          <q-td key="cusip" :props="props">
            <q-btn
              color="blue"
              type="a"
              :href="`/cusip/${props.row.cusip.cusip_number}`"
            >
              {{ props.row.cusip.cusip_number }}
            </q-btn>
          </q-td>
          <q-td key="sshPrnamt" :props="props">
            {{ props.row.sshPrnamt }}
          </q-td>
          <q-td key="sshPrnamtType" :props="props">
            {{ props.row.sshPrnamtType }}
          </q-td>
          <q-td key="investmentDiscretion" :props="props">
            {{ props.row.investmentDiscretion }}
          </q-td>
          <q-td key="putCall" :props="props">
            {{ props.row.putCall }}
          </q-td>
          <q-td key="otherManager" :props="props">
            {{ props.row.otherManager }}
          </q-td>
          <q-td key="sole" :props="props">
            {{ props.row.sole }}
          </q-td>
          <q-td key="shared" :props="props">
            {{ props.row.shared }}
          </q-td>
          <q-td key="nonee" :props="props">
            {{ props.row.nonee }}
          </q-td>
          <q-td key="filing" :props="props">
            <q-btn
              color="black"
              type="a"
              :href="`/admin/filing/filing/${props.row.filing.id}/change/`"
            >
              {{ props.row.filing.id }}
            </q-btn>
          </q-td>
        </q-tr>
      </template></q-table
    >
    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="current"
        :max="
          Math.ceil(
            $store.getters['holdings/getCount'] /
              $store.getters['holdings/getPagination'].rowsPerPage
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
export default {
  name: "HoldingsTable",
  data() {
    return {};
  },
  methods: {
    refreshData(props) {
      this.$store.dispatch("holdings/fetchData");
    }
  },
  computed: {
    holdingSearch: {
      get() {
        return this.$store.getters["holdings/getHoldingSearch"];
      },
      set(v) {
        this.$store.dispatch("holdings/setHoldingSearch", v);
      }
    },
    pagination: {
      get() {
        return this.$store.getters["holdings/getPagination"];
      },
      set(v) {
        this.$store.dispatch("holdings/setPagination", v);
      }
    },
    current: {
      get() {
        const currentPage = this.$store.getters["holdings/getCurrentPage"];
        return currentPage;
      },
      set(v) {
        this.$store.dispatch("holdings/setCurrentPage", v);
      }
    }
  },
  created() {
    this.$store.dispatch("holdings/fetchData");
  }
};
</script>
<style></style>
