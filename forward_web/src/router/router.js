import Vue from 'vue';
import VueRouter from 'vue-router';
import { store } from '../stores/store';

import LoginView from '../views/LoginView';
import HomeView from '../views/HomeView';
import SignUpView from '../views/SignUpView';
import PolicyView from '../views/PolicyView';
import AboutPage from '../views/AboutPage';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView, // change to HomePage
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView, // change to LoginPage
  },
  {
    path: '/signup',
    name: 'SignUpView',
    component: SignUpView, // change to SignUp
  },
  {
    path: '/policy/:id',
    name: 'PolicyView',
    component: PolicyView, // change to PolicyPage
    props: true,
  },
  {
    path: '/about',
    name: 'about-page', // should probably start standardizing this name format
    component: AboutPage
  }
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
