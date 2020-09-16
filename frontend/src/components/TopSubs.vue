<template>
<div class="col-lg-6 col-md- col-12" style="margin-bottom:0.5rem;">
    <div class="row mt-2">
        <div class="col-2 d-flex align-self-center">
            <p><span :class="css_class">{{ rank }}</span></p>
        </div>
        <div class="col-10">
            <div class="row">
                <div class="col top-n-list"><p><a href="https://reddit.com/r/${e[0]}" target="_blank">r/{{ subreddit }}</a></p></div>
            </div>
            <div class="row">
                <div class="col top-n-list"><p class="caption">{{ count }} {{mode == Constants.COMMENT ? "comments" : "submissions"}}</p></div>
            </div>
        </div>
    </div>
</div>
</template>

<script>

import Constants from "@/assets/js/config/Constants.js";
export default {
    name: "TopSubs",
    props: ["rank", "subreddit", "count", "css_class", "mode"],
    data: function() {
        return {
            Constants,
        };
    }
};
</script>

<style>

</style>