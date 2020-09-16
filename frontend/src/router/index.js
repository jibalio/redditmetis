/* eslint-disable */

import Vue from 'vue';
import VueMeta from "vue-meta";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";

import Userpage from '../views/Userpage.vue'

Vue.use(VueRouter);
Vue.use(VueMeta);
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {
            title: "hello!!!",
        }
    },
    {
        path: "/user/:uname",
        name: "userpage",
        component: Userpage,
        props: true,
        meta: { title: ($route=>"u/"+$route+" on RedditMetis - A Reddit User Analyzer")() }
    }
]

const router = new VueRouter({
    mode: 'history',
    routes,
})

router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    next()
});

export default router
