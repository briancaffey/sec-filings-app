<template>
  <div class="select">
    <q-select
      outlined
      dense
      bg-color="white"
      v-model="period"
      :options="$store.getters['core/getPeriods']"
    >
      <template v-slot:prepend> <q-icon name="today" /> </template
    ></q-select>
  </div>
</template>

<script>
export default {
  computed: {
    period: {
      get() {
        return this.$store.getters["core/getPeriod"];
      },
      set(v) {
        this.$store.dispatch("core/setPeriod", v);
      }
    }
  }
};
</script>

<style scoped></style>
