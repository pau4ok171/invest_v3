import { createRouter, createWebHistory } from 'vue-router';
import { loadLayoutMiddleware } from "@/router/middleware/loadLayout.middleware";
import { RouteNamesEnum } from "@/router/routes.types";
import { AppLayoutsEnum } from "@/layouts/layouts.types";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
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
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/articles',
      name: RouteNamesEnum.article,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/markets',
      name: RouteNamesEnum.company,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/CompanyView.vue')
    },
    {
      path: '/watchlist',
      name: RouteNamesEnum.watchlist,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/screener',
      name: RouteNamesEnum.screener,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/HomeView.vue')
    }
  ]
})

router.beforeEach(loadLayoutMiddleware);

export default router
