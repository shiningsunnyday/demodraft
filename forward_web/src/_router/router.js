import Vue from 'vue';
import VueRouter from 'vue-router';
import { store } from '@/_stores/store';
import NProgress from 'nprogress';

import NotFound from '@/views/404';
import PoliticianPlan from '@/components/politicians/PoliticianPlan';

Vue.use(VueRouter);

const loadView = (view) => {
  return () => import(/* webpackChunkName: "view-[request]" */ `../views/${view}.vue`);
};

const routes = [
  {
    path: '/',
    name: 'about-page',
    component: loadView('AboutPage'),
    meta: {
      requiresAuth: true,
      keepAlive: true,
    },
  },
  {
    path: '/policies',
    name: 'policies-page',
    component: loadView('PoliciesPage'),
    meta: {
      requiresAuth: true,
      keepAlive: true,
    },
  },
  {
    path: '/login',
    name: 'login-page',
    component: loadView('LoginPage'),
  },
  {
    path: '/signup',
    name: 'signup',
    component: loadView('SignUp'),
  },
  {
    path: '/policy/:id',
    name: 'selected-policy',
    component: () => import(/* webpackChunkName: "selected-policy" */ `../components/policy/SelectedPolicy.vue`),
    props: true,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/politicians',
    name: 'politician-page',
    component: loadView('PoliticianPage'),
    meta: {
      requiresAuth: true,
      keepAlive: true,
    },
  },
  {
    path: '/politicians-plan/:id',
    name: 'politician-plan',
    component: PoliticianPlan,
    props: true,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/politicians/:id',
    name: 'selected-politician',
    component: () => import(/* webpackChunkName: "selected-politician" */ `../components/politicians/SelectedPolitician.vue`),
    props: true,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/campaign',
    name: 'campaign-page',
    component: loadView('CampaignPage'),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    name: 'profile-page',
    component: () => import(/* webpackChunkName: "profile" */ '../views/ProfilePage.vue'),
    meta: {
      requiresAuth: true,
    },
  },
  { path: '*', component: NotFound },
];

const router = new VueRouter({
  routes,
  mode: 'history', // this removes hashtag from url
});

router.beforeEach((to, from, next) => {
  NProgress.start();
  // handling unauthorized access cases
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      return next();
    }
    next('/login');
  } else {
    next();
  }
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
