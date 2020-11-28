<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <q-toolbar-title> Form Thirteen <span em="1">♚</span> </q-toolbar-title>
        <q-btn
          v-if="!$store.getters['auth/getAuthenticated']"
          outlined
          color="white"
          text-color="blue"
          @click="$router.push('/login')"
          >Login</q-btn
        >&nbsp;
        <q-btn
          v-if="$store.getters['auth/getAuthenticated']"
          outlined
          color="white"
          text-color="blue"
          @click="$store.dispatch('auth/logout')"
          >Logout</q-btn
        >&nbsp;
        <period-select />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label header class="text-grey-8">
          Essential Links
        </q-item-label>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
        <EssentialLink
          v-if="$store.getters['auth/getAuthenticated']"
          title="Account"
          caption="User account"
          link="/account"
          icon="person"
        ></EssentialLink>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from "components/EssentialLink.vue";

const linksData = [
  {
    title: "Home",
    caption: "",
    icon: "home",
    link: "/"
  },
  {
    title: "Filer Profiling",
    caption: "Side-by-side fund comparisons",
    icon: "table_chart",
    link: "/funds"
  },
  {
    title: "Holdings List",
    caption: "All Filed Holdings",
    icon: "table_chart",
    link: "/holdings"
  },
  {
    title: "Filings List",
    caption: "All 13F Filings",
    icon: "file_copy",
    link: "/filings"
  },
  {
    title: "Dashboard",
    caption: "High-level View",
    icon: "file_copy",
    link: "/dashboard"
  },
  {
    title: "Investors",
    caption: "All 13F Filers",
    icon: "money",
    link: "/investors"
  },
  {
    title: "Securities",
    caption: "All Securities",
    icon: "money",
    link: "/securities"
  },
  {
    title: "API Documentation",
    caption: "OpenAPI Swagger Documentation",
    icon: "code",
    link: "/api/swagger-ui/"
  },
  {
    title: "Admin",
    caption: "Django Admin",
    icon: "settings",
    link: "/admin/"
  },
  {
    title: "SEC",
    caption: "SEC Link",
    icon: "link",
    link: "https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm"
  },
  {
    title: "About",
    caption: "About this project",
    icon: "info",
    link: "about"
  }
];

export default {
  name: "MainLayout",
  components: { EssentialLink },
  data() {
    return {
      leftDrawerOpen: false,
      essentialLinks: linksData
    };
  }
};
</script>
