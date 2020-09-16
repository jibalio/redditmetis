<template>
    <ContentPanel title="subreddit breakdown">
        <div class="row mt-3">
            <div class="col-lg-12 col-md-12 col-12">
                <div class="row">
                    <div class="col-12 d-flex justify-content-center">
                        <h2>Subreddit Breakdown</h2>
                    </div>
                    <div class="col-12 d-flex justify-content-center">
                        <p class="caption"> 
                            Click on the squares to zoom in. Click on the header tile (top) to go back. <a href="#" v-scroll-to="'#help-cat'" style="border-bottom: 1px dotted;">Help Categorize Subreddits</a>
                        </p>
                    </div>
                    
                    <div class="col-12 d-flex justify-content-center">
                        <b-form-radio-group id="radio-group-2" v-model="mode" name="radio-sub-component">
                            <b-form-radio value="posts"><p class="caption">by Number of Comments/Submissions</p></b-form-radio>
                            <b-form-radio value=karma><p class="caption">by Karma</p></b-form-radio>
                        </b-form-radio-group>
                    </div>
                    
                    <div class="col-12" style="padding:0 30px 30px 30px;">
                        <div  id="data-posts_by_subreddit"></div>
                    </div>
                </div>
            </div>
        </div>
    
    
    </ContentPanel>
</template>
<script>
import Treemap from "@/assets/js/graphs/treemap.js";
import ContentPanel from "../ContentPanel.vue";
import {BFormRadioGroup, BFormRadio} from "bootstrap-vue";
export default {
    name: "SubredditBreakdown",
    components: {
        ContentPanel,
        "b-form-radio-group": BFormRadioGroup,
        "b-form-radio": BFormRadio
    },
    props: ["user"],
    data: function() {
        return {
            mode: "posts",
        };
        
    },
    watch: {
        mode: function (val) {
            
            Treemap.chart(this.user.analysis.metrics.subreddit, val);
        }
    },
    mounted: function() {
        Treemap.chart(this.user.analysis.metrics.subreddit, "posts");
    },
    computed: {
    },
    methods: {
    }
};
</script>