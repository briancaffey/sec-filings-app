<template>
  <q-page padding> Logging in with {{ provider }}... </q-page>
</template>

<script>
export default {
  methods: {
    handleOauthCallback() {
      const vm = this;
      const provider = this.$route.params.provider;
      this.$axios
        .post(`/api/social/${provider}/`, { code: this.$route.query.code })
        .then(resp => {
          vm.$store.commit("auth/authSuccess");
          vm.$router.push("/");
        });
    }
  },
  mounted() {
    this.handleOauthCallback();
  },
  computed: {
    provider() {
      return this.$route.params.provider;
    }
  }
};
</script>
