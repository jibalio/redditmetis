<template>
    <div>
        <Navbar></Navbar>
        <Banner v-on:search_username="analyze" v-on:debug="debug"></Banner>
    </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';
import Banner from "@/components/Banner.vue";
import Navbar from "@/components/Navbar.vue";
import Hmap from "@/assets/js/graphs/hmap.js";
export default {
    name: "Home",
    components: {
        Banner,
        Navbar
    },
    methods: {
        analyze(userName) {
            this.$router.push({name:"userpage",params:{
                uname: userName 
            }});
        },
        async debug (post,comments) {
            Hmap.getHeatmapString(post,comments);
        }
    }
};
</script>
