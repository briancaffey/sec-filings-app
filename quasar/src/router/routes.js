const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/Index.vue")
      },
      {
        path: "login",
        component: () => import("pages/Login/index.vue")
      },
      {
        path: "account",
        component: () => import("pages/Account/index.vue"),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "filings",
        component: () => import("pages/Filings.vue"),
        name: "filings"
      },
      {
        path: "holdings",
        component: () => import("pages/Holdings.vue"),
        name: "stats"
      },
      {
        path: "/holdings/:cik/historical/:cusip/",
        component: () => import("pages/HistoricalHoldings.vue")
      },
      {
        path: "cik",
        component: () => import("pages/Cik/index.vue")
      },
      {
        path: "cik/:cik",
        component: () => import("pages/Cik/Portfolio.vue")
      },
      {
        path: "funds",
        component: () => import("pages/Funds/index.vue")
      },
      {
        path: "investors",
        component: () => import("pages/Investors/index.vue")
      },
      {
        path: "securities",
        component: () => import("pages/Securities/index.vue")
      },
      {
        path: "cusip/:cusip",
        component: () => import("pages/Cusip/index.vue")
      },
      {
        path: "dashboard",
        component: () => import("pages/Dashboard.vue")
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "*",
    component: () => import("pages/Error404.vue")
  }
];

export default routes;
