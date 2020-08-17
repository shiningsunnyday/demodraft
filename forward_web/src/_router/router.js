import Vue from 'vue';
import VueRouter from 'vue-router';
import { store } from '@/_stores/store';

import LoginPage from '@/views/LoginPage';
import HomePage from '@/views/HomePage';
import SignUp from '@/views/SignUp';
import SelectedPolicy from '@/components/policy/SelectedPolicy';
import AboutPage from '@/views/AboutPage';
import PoliticianPage from '@/views/PoliticianPage';
import SelectedPolitician from '@/components/politicians/SelectedPolitician';
import CampaignPage from '@/views/CampaignPage';
import NotFound from '@/views/404';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home-page',
    component: HomePage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/login',
    name: 'login-page',
    component: LoginPage,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
  },
  {
    path: '/policy/:id',
    name: 'selected-policy',
    component: SelectedPolicy,
    props: true,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/about',
    name: 'about-page',
    component: AboutPage,
  },
  {
    path: '/politicians',
    name: 'politician-page',
    component: PoliticianPage,
  },
  {
    path: '/politicians/:id',
    name: 'selected-politician',
    component: SelectedPolitician,
    props: true,
  },
  {
    path: '/campaign',
    name: 'campaign-page',
    component: CampaignPage,
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

// handling unauthorized access cases
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router;
