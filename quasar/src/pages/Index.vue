<template>
  <q-page padding>
    <q-card v-if="dev">
      <q-card-section class="q-px-md"
        >Welcome! It looks like you are running this project in
        <code>{{ env }}</code> mode, awesome! Thank you contributing to this
        project. To make sure your local development environment is set up
        correctly, have a look at the checklist.
      </q-card-section>
      <q-card-section>
        <q-btn color="primary">Development Checklist (coming soon)</q-btn>
      </q-card-section>
    </q-card>
    <q-card>
      <q-card-section>
        Welcome to Open SEC Data, a site for accessing and analyzing public SEC
        Data.
      </q-card-section>
      <q-card-section>
        <q-btn type="a" href="/about" color="primary">About</q-btn>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      dev: process.env.NODE_ENV === "development",
      env: process.env.NODE_ENV
    };
  }
};
</script>
