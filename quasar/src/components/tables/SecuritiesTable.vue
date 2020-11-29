<template>
  <div>
    <q-table
      :loading="$store.getters['securities/getLoading']"
      :hide-bottom="false"
      dense
      :title="`Securities (${$store.getters['securities/getCount']})`"
      row-key="id"
      :data="$store.getters['securities/getSecurities']"
      :pagination.sync="pagination"
      :requestServerInteraction="refreshData"
      @request="refreshData"
      hide-pagination
      :columns="$store.getters['securities/getColumns']"
    >
      <template #top-left>
        <q-btn type="a" :href="`/api/cusip/`"
          >Securities ({{ $store.getters["securities/getCount"] }})
        </q-btn>
      </template>
      <template v-slot:top-right>
        <q-input
          outlined
          dense
          placeholder="CUSIP or Company Name"
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
          <q-td key="cusip_number" :props="props">
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
          <q-td key="held_by_funds" :props="props">
            {{ props.row.held_by_funds }}
          </q-td>
          <q-td key="holding_count" :props="props">
            {{ props.row.holding_count }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <div class="row justify-center q-mt-md">
      <q-pagination
        v-model="current"
        :max="
          Math.ceil(
            $store.getters['securities/getCount'] /
              $store.getters['securities/getPagination'].rowsPerPage
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
  data() {
    return {};
  },
  methods: {
    refreshData(props) {
      this.$store.dispatch("securities/fetchData");
    }
  },
  created() {
    this.$store.dispatch("securities/fetchData");
  },
  computed: {
    search: {
      get() {
        return this.$store.getters["securities/getSearch"];
      },
      set(v) {
        this.$store.dispatch("securities/setSearch", v);
      }
    },
    pagination: {
      get() {
        return this.$store.getters["securities/getPagination"];
      },
      set(v) {
        this.$store.dispatch("securities/setPagination", v);
      }
    },
    current: {
      get() {
        const currentPage = this.$store.getters["securities/getCurrentPage"];
        return currentPage;
      },
      set(v) {
        this.$store.dispatch("securities/setCurrentPage", v);
      }
    }
  }
};
</script>

<style scoped></style>
