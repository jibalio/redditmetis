<template>
        
        <div class="container">
                

                <transition appear name="animated slideInUp">
                        <div>
                                <div class="row" v-if="user.about">
                                        <div class="col-12 d-flex justify-content-center">
                                                <img :src="user.about.icon_img.split('?')[0]" class="snoovatar round-edge" height="75px" width="75px"/>
                                        </div>
                                        <div class="col-12 d-flex justify-content-center mt-3">
                                                                <p class="metis-brand"><a :href="'https://reddit.com/user/'+(user.about.name)" class="user.analysis-link" target="_blank">u/{{ user.about.name }}</a></p>
                                        </div>
                                        <div class="col-12 d-flex justify-content-center mt-1" v-if="user.analysis">
                                                <p class="sublabel">redditor for {{user.analysis.age_string}}</p>
                                        </div>
                                        <div class="col-12 d-flex justify-content-center mt-1" v-if="user.analysis">
                                                <p class="sublabel" style="font-size:1.3rem;"><span v-if="user.analysis.is_gold" class="badge badge-warning">gold</span></p>
                                        </div>
                                </div>
                                <div v-if="user.analysis && user.about">
                                        <BasicInformation :user="user">
                                        </BasicInformation>

                                        <ActivityPatterns :user="user">
                                        </ActivityPatterns>

                                        <SubredditBreakdown :user="user">
                                        </SubredditBreakdown>

                                        <CommentStatistics :user="user" v-if="this.user.analysis.summary">
                                        </CommentStatistics>

                                        <SubmissionStatistics :user="user" v-if="this.user.analysis.summary">
                                        </SubmissionStatistics>

                                        <CorpusStatistics :user="user">
                                        </CorpusStatistics>

                                        <HelpImproveData :user="user">
                                        </HelpImproveData>


                                </div>
                        </div>
                </transition>
                
        </div>
        
</template>

<script>
import BasicInformation from "@/components/cards/BasicInformation.vue";
import ActivityPatterns from "@/components/cards/ActivityPatterns.vue";
import CommentStatistics from "@/components/cards/CommentStatistics.vue";
import SubmissionStatistics from "@/components/cards/SubmissionStatistics.vue";
import CorpusStatistics from "@/components/cards/CorpusStatistics.vue";
import SubredditBreakdown from "@/components/cards/SubredditBreakdown.vue";
import HelpImproveData from "@/components/cards/HelpImproveData.vue";

import Constants from "@/assets/js/config/Constants.js";
import moment from "moment-timezone";
export default {
    name: "Result",
    components: {
        BasicInformation,
        ActivityPatterns,
        CommentStatistics,
        SubmissionStatistics,
        CorpusStatistics,
        SubredditBreakdown,
        HelpImproveData
    },
    props: [
        "user"
    ],
    data: function() {
        return {
            Constants,
            moment
        };
    },
    computed: {
        gfIndex: function() {
            var index = Math.min(Math.round(this.user.analysis.readability["gf-index"]),17);
            var measure;
            var color;
            if (index >= 17) {
                measure = "Very High";
                color = "#8f0000";
            } else if (index >= 14) {
                measure = "High";
                color = "#fd5555";
            } else if (index >= 9) {
                measure = "Medium";
                color = "#f1bd26";
            } else if (index >= 6) {
                measure = "Low";
                color = "#65c12d";
            } else {
                measure = "Very Low";
                color = "#bbe62e";
            }
            return { index, color, measure };
        },
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


</style>
