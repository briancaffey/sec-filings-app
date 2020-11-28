<template>
  <q-page padding>
    <h4>Account</h4>
    <q-card>
      <q-card-section>
        <div class="text-h6">API Keys</div>
        <div>You can request API Keys to use in your own application.</div>
        <div>
          API Documentation can be found
          <a style="text-decoration:none;" href="/api/swagger-ui/">here</a>
        </div>
      </q-card-section>
      <q-card-section>
        <q-btn @click="requestToken" coloir="primary">Request API Key</q-btn>
      </q-card-section>
      <q-card-section v-if="token">
        <div>
          Save this token somewhere secure. You will have to request another
          token if you lose this token.
        </div>
        <q-input style="max-width: 350px" readonly boardered v-model="token">
          <template v-slot:after>
            <q-btn
              @click="copyTokenToClipboard"
              round
              dense
              :color="copied ? 'green' : ''"
              flat
              icon="content_copy"
            />
          </template>
        </q-input>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { copyToClipboard } from "quasar";
export default {
  data() {
    return {
      token: null,
      copied: false
    };
  },
  methods: {
    copyTokenToClipboard() {
      copyToClipboard(this.token).then(() => {
        this.copied = true;
      });
    },
    requestToken() {
      this.copied = false;
      this.$axios.post("/api/request-api-token/").then(resp => {
        this.token = resp.data.token;
      });
    }
  }
};
</script>

<style scoped></style>
