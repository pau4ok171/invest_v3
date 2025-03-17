// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { usePageStore } from '@/store/page'

// Utilities
import { loadLayoutMiddleware } from '@/router/middleware/loadLayout.middleware'
import { RouteNamesEnum } from '@/router/routes.types'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: RouteNamesEnum.home,
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/admin',
      name: RouteNamesEnum.admin,
      component: () => import('@/views/AdminView.vue'),
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (
          !Object.hasOwn(authStore.userInfo, 'is_staff') ||
          !authStore.userInfo.is_staff
        ) {
          next(RouteNamesEnum.page_not_found)
        }
        next()
      },
    },
    {
      path: '/dashboard',
      name: RouteNamesEnum.dashboard,
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/portfolio',
      name: RouteNamesEnum.portfolio,
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/articles',
      name: RouteNamesEnum.article,
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/markets',
      name: RouteNamesEnum.company_list,
      component: () => import('@/views/CompanyListView.vue'),
    },
    {
      path: '/markets/:companySlug',
      name: RouteNamesEnum.company_detail,
      component: () => import('@/views/CompanyDetailView.vue'),
    },
    {
      path: '/watchlist',
      name: RouteNamesEnum.watchlist,
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/screener',
      name: RouteNamesEnum.screener,
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: RouteNamesEnum.page_not_found,
      component: () => import('@/views/PageNotFoundView.vue'),
    },
  ],
})

router.beforeEach(async (route) => {
  const pageStore = usePageStore()

  pageStore.notFound = false
  await loadLayoutMiddleware(route)
})

export default router
