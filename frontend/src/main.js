console.log("RedditMetis v1.00");

import Vue from "vue";
import App from "./App.vue";
import router from "./router";

// Vendor
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "vue-select/dist/vue-select.css";
import "animate.css";

import Constants from  "./assets/js/config/Constants.js";
Vue.prototype.Constants = Constants;

import VueScrollTo from "vue-scrollto";
Vue.use(VueScrollTo);

import Enum from "./assets/js/config/Enum.js";
Vue.prototype.Enum = Enum;

import { VBToggle } from "bootstrap-vue";
// Note: Vue automatically prefixes the directive name with 'v-'
Vue.directive("b-toggle", VBToggle);

import { BCollapse } from "bootstrap-vue";
Vue.component("b-collapse", BCollapse);

import vSelect from "vue-select";
Vue.component("v-select", vSelect);

import axios from "axios";


Vue.prototype.CLIENT = axios.create({
    baseURL: "http://localhost:5000"
});

Vue.component("spinner", {
    props: ["size"],
    template: "<div role=\"status\" class=\"spinner-border text-info\" :style=\"{width:size,height:size}\"><span class=\"sr-only\"></span></div>"
});

Vue.filter("cleanNumber", function(val, fixed) {
    var decimals = fixed || 0;
    var v = val.toString();
    var isNegative = v.startsWith("-");
    var ret = "";
    if (isNegative) {
        v = v.substring(1);
        ret = "-";
    }
    if (val >= 1000 && val <= 999999) {
        return ret + parseFloat(val / 1000).toFixed(decimals) + "k";
    } else if (val >= 1000000) {
        return ret + parseFloat(val / 1000000).toFixed(decimals) + "M";
    }
    return Math.round(val);
});


// Custom Styles
import MetisClient from "./assets/js/metisclient.js";
import "./assets/css/style.css";
import "./assets/css/googlefonts.css";
Vue.prototype.MetisClient = new MetisClient();
Vue.config.productionTip = false;

new Vue({
    router,
    render: h => h(App)
}).$mount("#app");
