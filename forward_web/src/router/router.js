import Vue from "vue";
import VueRouter from "vue-router";
import LoginView from "../views/LoginView";
import HomeView from '../views/HomeView';
import SignUpView from '../views/SignUpView';
import PolicyView from '../views/PolicyView';

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "HomeView",
    component: HomeView,
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView,
  },
  {
    path: "/signup",
    name: "SignUpView",
    component: SignUpView,
  },
  {
    path: "/policy/:id",
    name: "PolicyView",
    component: PolicyView,
    props: true
  },
];

const router = new VueRouter({
  routes,
  mode: "history" // this removes hashtag from url
});

export default router;
