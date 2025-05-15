// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { usePageStore } from '@/store/page'

// Utilities
import { loadLayoutMiddleware } from '@/router/middleware/loadLayout.middleware'
import { RouteNamesEnum } from '@/router/routes.types'
import { AppLayoutsEnum } from '@/layouts/layouts.types'

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
      meta: {
        layout: AppLayoutsEnum.admin,
      },
      children: [
        {
          path: 'models',
          name: 'adminModels',
          component: () => import('@/components/admin/models/AdminModels.vue'),
          meta: {
            layout: AppLayoutsEnum.admin,
          },
          children: [
            {
              path: 'companies',
              name: 'adminModelsCompanies',
              component: () =>
                import('@/components/admin/models/company/AdminModelsCompanies.vue'),
              meta: {
                layout: AppLayoutsEnum.admin,
              },
            },
            {
              path: 'companies/new',
              name: 'adminCompanyModelNew',
              component: () => import('@/components/admin/models/company/AdminModelCompany.vue'),
              meta: {
                layout: AppLayoutsEnum.admin,
              },
            },
            {
              path: 'companies/:companyUID([A-Za-z0-9-]+)',
              name: 'adminCompanyModel',
              component: () => import('@/components/admin/models/company/AdminModelCompany.vue'),
              meta: {
                layout: AppLayoutsEnum.admin,
              },
              props: true,
            },
          ],
        },
        {
          path: 'dashboard',
          name: 'adminDashboard',
          component: () => import('@/components/admin/dashboard/AdminDashboard.vue'),
          meta: {
            layout: AppLayoutsEnum.admin,
          },
        },
        {
          path: 'staff',
          name: 'adminStaff',
          component: () => import('@/components/admin/staff/AdminStaff.vue'),
          meta: {
            layout: AppLayoutsEnum.admin,
          },
        },
        {
          path: 'settings',
          name: 'adminSettings',
          component: () => import('@/components/admin/settings/AdminSettings.vue'),
          meta: {
            layout: AppLayoutsEnum.admin,
          },
        },
      ],
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
      props: true,
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
  pageStore.loading = true

  await loadLayoutMiddleware(route)
})

router.afterEach(() => {
  const pageStore = usePageStore()

  setTimeout(() => pageStore.loading = false, 15000)
})

export default router
