import {createRouter, createWebHistory} from 'vue-router';
import {loadLayoutMiddleware} from "@/router/middleware/loadLayout.middleware";
import {RouteNamesEnum} from "@/router/routes.types";

// VIEWS
import HomeView from "@/views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: RouteNamesEnum.home,
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
      name: RouteNamesEnum.company_list,
      component: () => import('@/views/CompanyListView.vue')
    },
    {
      path: '/markets/:company_slug',
      name: RouteNamesEnum.company_detail,
      component: () => import('@/views/CompanyDetailView.vue')
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
