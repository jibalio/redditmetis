<template>
    <ContentPanel title="help improve data">
        <div class="row">

                <!-- ACTIVITY HEATMAP HALF-->
                <div class="col-md-12 col-lg-12 col-12 mb-3 mt-2">
                    <div class="mt-2 row d-flex justify-content-center">
                        <div class="col-12">
                            <div id="help-cat" class="row">
                                <div class="col-12 d-flex justify-content-center">
                                    <h2>categorize subreddits</h2>
                                </div>
                                <div class="col-12 d-flex justify-content-center">
                                    <p style="text-align:center" class="caption ml-3 mr-3">Help RedditMetis by categorizing the subreddits below. Subreddit categories will be updated once they get suggested enough.</p>
                                </div>
                                <div class="col-12 d-flex justify-content-center">
                                    <p style="text-align:center" class="caption ml-3 mr-3">You don't have to fill them all in, if you aren't familiar with some of them.</p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-3 col-12 d-flex justify-content-center">
                            <div v-if="isCategorizationLoading" class="mb-4 spinner-border text-info" role="status" style="width:50px;height:50px">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                        <div class="col-12 d-flex justify-content-center" v-if="this.isCategorizationLoading">
                            <p>{{categorizationLoadText}}</p>
                        </div>

                        <div class="col-md-8 col-12 mt-3 d-flex justify-content-center">
                            
                            <table v-if="!isCategorizationLoading && !isCategorizationUnavailable" class="table table-sm">
                                <thead>
                                    <tr>
                                        <th style="width:25%"><p>Subreddit</p></th>
                                        <th style="width:75%"><p>Category</p></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- TODO: MAKE IT SUBMITTABLE -->
                                    <tr v-for="subreddit in uncategorized_subs" :key="'hid_uncategorized'+subreddit">
                                        <td style="width:25%"><p>{{ subreddit }}</p></td>
                                        <td style="width:75%">
                                            <v-select :disabled="isSubmittedCategorization" v-model="form_data[subreddit]" :options="topics" label="name" placeholder="-- Choose Category --">
                                                <template>
                                                    <input
                                                    class="vs__search"
                                                    :required="true"
                                                    />
                                                </template>
                                            </v-select>
                                        </td>
                                        
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-if="this.isSubmittingCategorizationError" class="alert alert-warning col-8" role="alert">
                            {{isSubmittingCategorizationText}}
                        </div>
                        <div v-if="this.isSubmittedCategorization" class="alert alert-success col-8" role="alert">
                            <p class="caption">Your suggestions have been submitted. Thank you!</p>
                        </div>
                        <div v-if="this.isCategorizationUnavailable" class="alert alert-warning col-8" role="alert">
                            <p class="caption">Service is unavailable right now. Please try again later.</p>
                        </div>
                        <div class="col-12 d-flex justify-content-center" v-if="!this.isSubmittedCategorization && !isCategorizationUnavailable">
                            <button class="btn btn-info " @click="submitSubredditCategorization()" :disabled="isSubmittingCategorization || isCategorizationLoading">
                                <p style="color:white">Submit</p>
                            </button>
                        </div>
                    </div>
                </div>

        </div>
    </ContentPanel>
</template>
<style scoped>
th p, td p {
    text-align: left!important;
}
table {
    table-layout: auto!important;
}
</style>
<script>
import ContentPanel from "../ContentPanel.vue";
// import CommentContainer from "../CommentContainer.vue";
// import {BFormCheckbox} from "bootstrap-vue";
export default {
    mounted: async function() {
            
        var topics = await this.MetisClient.getTopics();
        if (topics.error) {
            this.isCategorizationLoading = false;
            this.isCategorizationUnavailable = true;
        }
        else 
            this.topics = topics.data;
            // Get all the subs that are in the "Other category"

        var uncategorized_subs = [];

        this.user.analysis.metrics.subreddit.children.forEach((topic)=>{
            if (topic.name=="Other") {
                topic.children.forEach((subreddit)=>{
                    uncategorized_subs.push(subreddit.name);
                });
                return;
            }
        });

        if (uncategorized_subs.length == 0) {
            // if the subs of the user are already categorized,
            // just get random subreddits from the database

            var topic_random = await this.MetisClient.getRandomSubredditSuggestions();
            uncategorized_subs = topic_random.data;
        }

        this.isCategorizationLoading = false;
        this.uncategorized_subs = uncategorized_subs;
    },
    name: "HelpImproveData",
    components: {
        ContentPanel,
        // "b-form-checkbox":BFormCheckbox,
        // CommentContainer
    },
    props: ["user"],
    data: function() {
        return {
            topics:null,
            uncategorized_subs:null,
            form_data:{},
            isSubmittingCategorization: false,
            isSubmittingCategorizationError: false,
            isSubmittingCategorizationText: "",
            isSubmittedCategorization: false,
            isCategorizationLoading: true,
            isCategorizationUnavailable: false,
            submissioncounter: 0,
            categorizationLoadText: "Retrieving subreddits. Please wait."
        };
    },
    methods: {
        async submitSubredditCategorization(){
            switch(this.submissioncounter) {
            case 2:
                this.categorizationLoadText = "You're really enjoying this, aren't you?";
                break;
            case 4:
                this.categorizationLoadText = "Thanks! But uh you know you can stop now, right? No? Oh well, fetching more subreddits.";
                break;
            default:
                this.categorizationLoadText = "Awesome! Fetching more subreddits.";
            }
            this.isCategorizationLoading = true;
            this.isSubmittingCategorizationError = false;
            this.isSubmittingCategorization = true;
            var data = [];
            let keys = Object.keys(this.form_data);

            // if there was nothing submitted, do not send data.
            if (keys.length==0) {
                this.isSubmittingCategorizationText = "Please select your suggestions.";
                this.isSubmittingCategorizationError = true;
            } else {
                keys.forEach(key => {
                    data.push({
                        "subreddit":key,
                        "topic_id":this.form_data[key].value
                    });
                });
                
                
                var message = await this.MetisClient.submitSubredditCategorization(data);
                if (message.error){
                    this.isSubmittingCategorizationText = message.error;
                    this.isSubmittingCategorizationError = true;
                } else {
                    

                    // format: ["subreddit1", "subreddit2", "subreddit3"]
                    var topics = await this.MetisClient.getRandomSubredditSuggestions();
                    this.uncategorized_subs = topics.data;
                    
                    this.submissioncounter++;

                    

                        
                }

            }
            this.isSubmittingCategorization = false;
            
            this.isCategorizationLoading = false;
        }
        
            

    },
    computed: {
        
    }


};
</script>