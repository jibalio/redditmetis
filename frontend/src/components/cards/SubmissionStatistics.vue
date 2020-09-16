<template>
    <ContentPanel title="submission statistics">
        <div v-if="user.analysis.summary.comments.count<=0" class="row justify-content-center mt-3 mb-3" id="no-comments-container"><p>This user has no comments</p></div>
                        <div v-else class="row mt-2" id="comments-container">
                            <div class="col-md-6 col-sm-12 col-12 mb-3">
                                <!-- COMMENT NUMBERS-->
                                <div class="row d-flex justify-content-center mb-2">
                                    <StatContainer v-for="i in submission_stats" :key="i.key" :m_key="i.key" :value="i.value"/>
                                </div> 
                            </div>
                            <div class="col-md-6 col-sm-12 col-12">
                                <div class="row">
                                    <div class="col d-flex justify-content-center">
                                        <h2>best comment</h2>
                                    </div>
                                </div>
                                <CommentContainer 
                                        :votes="best_submission.votes" 
                                        :subreddit="best_submission.sub" 
                                        :fromnow="Utils.getFromNow(best_submission.created_utc)" 
                                        :permalink="best_submission.permalink"
                                        :gildings="best_submission.gildings"
                                        >
                                        <p>
                                            <span v-if="truncated.best_submission" v-html="best_submission.title"></span>
                                            <span v-if="!truncated.best_submission" v-html="best_submission.title"></span>
                                        </p>
                                </CommentContainer>
                                <!-- worst COMMENT -->
                                <div class="row mt-3">
                                    <div class="col d-flex justify-content-center">
                                        <h2>worst comment</h2>
                                    </div>
                                </div>
                                <CommentContainer
                                        class="mb-3" 
                                        :votes="worst_submission.votes" 
                                        :subreddit="worst_submission.sub" 
                                        :fromnow="Utils.getFromNow(worst_submission.created_utc)" 
                                        :permalink="worst_submission.permalink"
                                        :gildings="worst_submission.gildings"
                                        >
                                        <p>
                                            <span v-if="truncated.worst_submission" v-html="worst_submission.title"></span>
                                            <span v-if="!truncated.worst_submission" v-html="worst_submission.title"></span>
                                            <span v-if="worst_submission.more"><a v-on:click="truncated.worst_submission = !truncated.worst_submission" href="#!">{{ truncated.worst_submission ? 'Read more' : 'Show less'}}</a></span>
                                        </p>
                                </CommentContainer>
        
                            </div>

                            <div class="mt-2 col-md-6 col-sm-12 col-12">
                                <!-- COMMENT NUMBERS-->
                                <div class="row d-flex justify-content-center mb-2">
                                    <h2>top subreddits by number of submissions</h2>
                                </div> 
                                <div class="row d-flex justify-content-center mb-2 num-list">
                                    <TopSubs v-for="(s, idx) in this.user.analysis.top_subs.post" 
                                            :key="'ts'+idx" 
                                            :rank="idx+1"
                                            :subreddit="s[0]"
                                            :count="s[1]"
                                            :css_class="'gradient-number-1'"
                                            :mode="Constants.SUBMISSION"
                                        />
                                </div> 
                            </div>
                            <div class="mt-2 col-md-6 col-sm-12 col-12">
                                <!-- COMMENT NUMBERS-->
                                <div class="row d-flex justify-content-center mb-2">
                                    <h2>top subreddits by submission karma</h2>
                                </div> 
                                <div class="row d-flex justify-content-center mb-2 num-list" id="list-comment-karma">
                                    <TopSubs v-for="(s, idx) in this.user.analysis.top_subs_by_karma.submission" 
                                        :key="'tsk'+idx" 
                                        :rank="idx+1"
                                        :subreddit="s[0]"
                                        :count="s[1]"
                                        :css_class="'gradient-number'"
                                        :mode="Constants.SUBMISSION"
                                        />
                                </div> 
                            </div>
                        </div>
    </ContentPanel>
</template>
<script>

import Utils from "@/assets/js/utils.js";

import ContentPanel from "../ContentPanel.vue";
import CommentContainer from "../CommentContainer.vue";
import TopSubs from "../TopSubs.vue";
import Constants from "@/assets/js/config/Constants.js";
import StatContainer from "../StatContainer.vue";
export default {
    name: "SubmissionStatistics",
    components: {
        ContentPanel,
        CommentContainer,
        StatContainer,
        TopSubs,
    },
    props: ["user"],
    data: function() {
        return {
            Constants,
            Utils,
            truncated: {
                best_submission : true,
                worst_submission : true
            },
            best_submission: (function() {
                var a = this.user.analysis.summary.submissions.best;
                if (this.user.gildings.best.submission) {
                    a["gildings"] = {
                        "platinum": this.user.gildings.best.submission.gid_3,
                        "gold": this.user.gildings.best.submission.gid_2,
                        "silver": this.user.gildings.best.submission.gid_1,
                    };
                }
                return a;
            }.bind(this))(),
            worst_submission: (function() {
                var a = this.user.analysis.summary.submissions.worst;
                if (this.user.gildings.worst.submission) {
                    a["gildings"] = {
                        "platinum": this.user.gildings.worst.submission.gid_3,
                        "gold": this.user.gildings.worst.submission.gid_2,
                        "silver": this.user.gildings.worst.submission.gid_1,
                    };
                }
                return a;
            }.bind(this))(),
            submission_stats: [
                { key: "comment count", value: Utils.formatNumber(this.user.analysis.summary.submissions.count) },
                { key: "gilded comments", value: Utils.formatNumber(this.user.analysis.summary.submissions.gilded) },
                { key: "karma", value: Utils.formatNumber(this.user.analysis.summary.submissions.all_time_karma) },
            ]
        };
    }
};
</script>