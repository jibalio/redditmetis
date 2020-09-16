<template>
    <ContentPanel title="activity pattern">
        <div class="row">
            <div class="row">
                <!-- ACTIVITY HEATMAP HALF-->
                <div class="col-md-6 col-lg-6 col-12 mb-3">
                    <div id="heatmap_container">
                        <div class="mt-2 row d-flex justify-content-center">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-12 d-flex justify-content-center">
                                        <h2>activity heatmap</h2>
                                    </div>
                                    <div class="col-12 d-flex justify-content-center">
                                        <p style="text-align:center" class="caption ml-3 mr-3">Times are in {{ Constants.Timezone }}. Darker squares means more activity. Hover or click on the squares to see the date.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="heatmap">
                        </div>
                    </div>
                </div>


                <!-- SUBMISSIONS BY WEEKDAY -->
                <div class="col-sm-12 col-md-6 col-12 mt-2 mb-3">
                    <div class="row">
                        <div class="col-12 d-flex justify-content-center">
                            <h2>submissions by weekday</h2>
                        </div>
                        <div class="col-12 d-flex justify-content-center">
                            <p class="caption">Click on the labels to remove/filter by post/karma</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <div id="submission_by_weekday"></div>
                        </div>
                    </div>
                </div>


                <!-- SUBMISSIONS BY HOUR1-->
                <div class="col-md-6 col-lg-6 col-12 mb-3">
                    <div class="row">
                        <div class="col-12 d-flex justify-content-center">
                            <h2>submissions by hour of day</h2>
                        </div>
                        <div class="col-12 d-flex justify-content-center">
                            <p class="caption">Click on the labels to remove/filter by post/karma</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <div id="submisison_by_hour"></div>
                        </div>
                    </div>
                    
                </div>



                <!-- POSTS OVER TIME -->
                <div class="col-sm-12 col-md-6 col-lg-6 col-12 mb-3">
                    <div class="row">
                        <div class="col-12 d-flex justify-content-center">
                            <h2>post/karma over time</h2>
                        </div>
                        <div class="col-12 d-flex justify-content-center">
                            <p class="caption">Click on the labels to remove/filter by post/karma</p>
                        </div>
                        <div class="col-12 d-flex justify-content-center mb-2">
                            <b-form-checkbox v-model="cumulative" name="check-button"  switch>
                                <p class="caption">Cumulative</p>
                            </b-form-checkbox>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <div v-show="cumulative || graph_loading" id='karma_canvas_cumu'></div>
                            <div v-show="!cumulative || graph_loading" id='karma_canvas_notcumu'></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </ContentPanel>
</template>
<style scoped>

</style>
<script>
import ContentPanel from "../ContentPanel.vue";
import Heatmap from "@/assets/js/graphs/hmap.js";
import ActivityCharts from "@/assets/js/graphs/apex.js";
import {BFormCheckbox} from "bootstrap-vue";
export default {
    mounted: async function() {
        await ActivityCharts.generateKarmaGraph(this.user.PKOverTime);
        ActivityCharts.generateSubmissionByHourGraph(this.user.histogram);
        ActivityCharts.generateSubmissionByWeekdayGraph(this.user.histogram);
        Heatmap.generate(this.user.heatmapData);
        this.graph_loading = false;
    },
    name: "ActivityPatterns",
    components: {
        ContentPanel,
        "b-form-checkbox":BFormCheckbox,
        // CommentContainer
    },
    props: ["user"],
    data: function() {
        return {
            graph_loading: true,
            cumulative: true,

        };
    },
};
</script>