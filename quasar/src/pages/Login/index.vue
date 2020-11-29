<template>
  <q-page padding>
    <div class="login">
      <q-card class="card">
        <q-card-section>
          <div class="text-center q-pa-md q-gutter-md">
            <!-- <q-btn round color="black">
              <q-icon name="fab fa-google-plus-g" size="1.2rem" />
            </q-btn>
            <q-btn round color="black">
              <q-icon name="fab fa-github" size="1.2rem" />
            </q-btn>
            <q-btn round color="black">
              <q-icon name="fab fa-microsoft" size="1.2rem" />
            </q-btn> -->
            <q-btn type="a" :href="buildUrl" class="full-width" color="black">
              <q-icon name="fab fa-linkedin" left size="1.2rem" />
              Sign in with LinkedIn
            </q-btn>
          </div>
        </q-card-section>

        <q-card-section>
          <q-form @submit.prevent="login">
            <q-input
              outlined
              style="padding-bottom:5px;"
              id="email"
              v-model="email"
              type="text"
              label="Email"
              autofocus
            />
            <q-input
              outlined
              style="padding-bottom:5px;margin:auto"
              id="password"
              type="password"
              v-model="password"
              label="Password"
            />
            <q-btn
              unelevated
              color="primary"
              type="submit"
              class="full-width text-white"
              label="Login with Email"
            />
          </q-form>
        </q-card-section>
        <q-card-section class="text-center q-pa-sm">
          <p class="text-grey-6">
            If you don't have an account, <u>Sign Up</u>
          </p>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import buildURL from "axios/lib/helpers/buildURL";
export default {
  data() {
    return {
      email: process.env.NODE_ENV === "production" ? "" : "admin@company.com",
      password: process.env.NODE_ENV === "production" ? "" : "password",
      redirect: null,
      linkedinUrl: {
        url: "https://www.linkedin.com/oauth/v2/authorization",
        params: {
          response_type: "code",
          client_id: process.env.LINKEDIN_CLIENT_ID,
          scope: "r_liteprofile r_emailaddress",
          state: "erferf",
          redirect_uri: "/auth/callback/linkedin-oauth2"
        }
      }
    };
  },
  computed: {
    buildUrl() {
      const base_url = window.location.origin;
      const redirect_uri = `${base_url}${this.linkedinUrl.params.redirect_uri}`;
      const params = { ...this.linkedinUrl.params, redirect_uri };

      return buildURL(this.linkedinUrl.url, params);
    }
  },
  created() {
    this.setRedirect();
    this.$axios.get("/api/login-set-cookie/");
  },
  methods: {
    setRedirect() {
      if ("redirect" in this.$route.query) {
        this.redirect = this.$route.query.redirect;
      }
    },
    login() {
      const vm = this;
      const { email, password, redirect } = this;
      this.$store
        .dispatch("auth/login", {
          email,
          password
        })
        .then(() => {
          if (redirect) {
            // TODO: redirect not working
            vm.$router.push("/");
          } else {
            vm.$router.push("/");
          }
        });
      this.email = "";
      this.password = "";
    }
  }
};
</script>

<style scoped>
.login {
  text-align: center;
  display: grid;
  justify-content: center;
}

.card {
  max-width: 95%;
  min-width: 320px;
  padding: 20px;
}
</style>
