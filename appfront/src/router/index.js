import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/managerHome.vue'
import workerApplyHistory from '../components/worker/workerApplyHistory.vue'
import workerApply from '../components/worker/workerApply.vue'
import workerApplyStatistics from '../components/worker/workerApplyStatistics.vue'
import workerAccount from '../components/worker/workerAccount.vue'
import allWorkerStatisticsData from '../components/manager/allWorkerStatisticsData.vue'
import managerApprove from '../components/manager/managerApprove.vue'
import workerAccountManager from '../components/manager/workerAccountManager.vue'
import overtimeStatistics from '../components/manager/overtimeStatistics.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('../views/login.vue'),
    meta: {
      isLogin: false
    }
  },
  {
    path: '/manager',
    name: 'managerView',
    component: HomeView,
    meta: {
      isLogin: true,
      pathType: 2
    },
    children: [
      { path: 'allWorkerStatisticsData', component: allWorkerStatisticsData },
      { path: 'managerApprove', component: managerApprove },
      { path: 'workerAccountManager', component: workerAccountManager },
      {path: 'overtimeStatistics', component: overtimeStatistics}
    ]
  },

  {
    path: '/worker',
    name: 'workerView',
    component: () => import(/* webpackChunkName: "about" */ '../views/workerHome.vue'),
    meta: {
      isLogin: true,
      pathType: 1
    },
    children: [
      { path: 'account', component: workerAccount },
      { path: 'applyHistory', component: workerApplyHistory },
      { path: 'apply', component: workerApply },
      { path: 'timePool', component: workerApplyStatistics },

    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
