import Vue from "vue";
import Vuex from "vuex";

// import example from './module-example'
import holdings from "./modules/holdings";
import filings from "./modules/filings";
import core from "./modules/core";
import portfolio from "./modules/portfolio";
import dashboard from "./modules/dashboard";
import investors from "./modules/investors";
import securities from "./modules/securities";
import cusip from "./modules/cusip/";

Vue.use(Vuex);

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default function(/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      // example
      holdings,
      filings,
      core,
      portfolio,
      dashboard,
      investors,
      securities,
      cusip
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  });

  return Store;
}
