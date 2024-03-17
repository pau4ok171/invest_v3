import { createRouter, createWebHistory } from 'vue-router';
import { loadLayoutMiddleware } from "@/router/middleware/loadLayout.middleware";
import { RouteNamesEnum } from "@/router/routes.types";
import { AppLayoutsEnum } from "@/layouts/layouts.types";

// VIEWS
import HomeView from "@/views/HomeView.vue";
import CompanyListView from "@/views/CompanyListView.vue";
import CompanyDetailView from "@/views/CompanyDetailView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/dashboard',
      name: RouteNamesEnum.dashboard,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/portfolio',
      name: RouteNamesEnum.portfolio,
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/articles',
      name: RouteNamesEnum.article,
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/markets',
      name: RouteNamesEnum.company,
      component: CompanyListView
    },
    {
      path: '/markets/:company_slug',
      name: CompanyDetailView.name,
      component: CompanyDetailView
    },
    {
      path: '/watchlist',
      name: RouteNamesEnum.watchlist,
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/screener',
      name: RouteNamesEnum.screener,
      component: () => import('@/views/HomeView.vue')
    }
  ]
})

router.beforeEach(loadLayoutMiddleware);

export default router
