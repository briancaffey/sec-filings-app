import Vue from "vue";
import VueRouter from "vue-router";

import routes from "./routes";

Vue.use(VueRouter);

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default function({ store }) {
  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,

    // Leave these as they are and change in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    // mode: process.env.VUE_ROUTER_MODE,
    mode: "history",
    base: process.env.VUE_ROUTER_BASE
  });
  // https://forum.quasar-framework.org/topic/2680/access-the-store-in-routes-js-to-use-navigation-guards/7
  Router.beforeEach((to, from, next) => {
    let allowedToEnter = true;
    const isAuthenticated = store.getters["auth/getAuthenticated"];
    to.matched.some(record => {
      // check for `meta` property in route
      if ("meta" in record) {
        //check to see if the user needs to be logged in to visit the page
        if ("requiresAuth" in record.meta) {
          if (!isAuthenticated) {
            allowedToEnter = false;
            next({
              path: "/login",
              replace: true,
              // redirect back to original path when done signing in
              query: { redirect: to.fullPath }
            });
          }
        }
      }
    });
    if (allowedToEnter) {
      // go to the requested page
      next();
    }
  });

  return Router;
}
