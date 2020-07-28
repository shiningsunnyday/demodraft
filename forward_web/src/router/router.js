import Vue from "vue";
import VueRouter from "vue-router";
import LoginView from "../views/LoginView";
import HomeView from '../views/HomeView';
import SignUpView from '../views/SignUpView';

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
];

const router = new VueRouter({
  routes,
  mode: "history" // this removes hashtag from url
});

export default router;
