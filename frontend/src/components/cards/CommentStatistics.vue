<template>
    <ContentPanel title="comment statistics">
        <div v-if="user.analysis.summary.comments.count<=0" class="row justify-content-center mt-3 mb-3" id="no-comments-container"><p>This user has no comments</p></div>
                        <div v-else class="row mt-2" id="comments-container">
                            <div class="col-md-6 col-sm-12 col-12 mb-3">
                                <!-- COMMENT NUMBERS-->
                                <div class="row d-flex justify-content-center mb-2">
                                    <StatContainer v-for="i in comment_stats" :key="i.key" :m_key="i.key" :value="i.value"/>
                                </div> 
                            </div>
                            <div class="col-md-6 col-sm-12 col-12">
                                <div class="row">
                                    <div class="col d-flex justify-content-center">
                                        <h2>best comment</h2>
                                    </div>
                                </div>
                                <CommentContainer 
                                        :votes="best_comment.votes" 
                                        :subreddit="best_comment.sub" 
                                        :fromnow="Utils.getFromNow(best_comment.created_utc)" 
                                        :permalink="best_comment.permalink"
                                        :gildings="best_comment.gildings"
                                        >
                                        <span v-if="truncated.best_comment" v-html="Utils.removeMd(best_comment.text)"></span>
                                        <span v-if="!truncated.best_comment" v-html="Utils.removeMd(best_comment.full)"></span>
                                        <span v-if="best_comment.more"><a @click="truncated.best_comment=!truncated.best_comment" href="#!" onclick="return false;">{{ truncated.best_comment ? 'Read more' : 'Show less' }}</a></span>
                                </CommentContainer>
                                <!-- worst COMMENT -->
                                <div class="row mt-3">
                                    <div class="col d-flex justify-content-center">
                                        <h2>worst comment</h2>
                                    </div>
                                </div>
                                <CommentContainer
                                        class="mb-3" 
                                        :votes="worst_comment.votes" 
                                        :subreddit="worst_comment.sub" 
                                        :fromnow="Utils.getFromNow(worst_comment.created_utc)" 
                                        :permalink="worst_comment.permalink"
                                        :gildings="worst_comment.gildings"
                                        >
                                        <span v-if="truncated.worst_comment" v-html="Utils.removeMd(worst_comment.text)"></span>
                                        <span v-if="!truncated.worst_comment" v-html="Utils.removeMd(worst_comment.full)"></span>
                                        <span v-if="worst_comment.more"><a v-on:click="truncated.worst_comment = !truncated.worst_comment" href="#!" onclick="return false;">{{ truncated.worst_comment ? 'Read more' : 'Show less'}}</a></span>
                                </CommentContainer>
        
                            </div>

                            <div class="mt-2 col-md-6 col-sm-12 col-12">
                                <!-- COMMENT NUMBERS-->
                                <div class="row d-flex justify-content-center mb-2">
                                    <h2>top subreddits by number of comments</h2>
                                </div> 
                                <div class="row d-flex justify-content-center mb-2 num-list">
                                    <TopSubs v-for="(s, idx) in this.user.analysis.top_subs.comment" 
                                        :key="'tc'+idx" 
                                        :rank="idx+1"
                                        :subreddit="s[0]"
                                        :count="s[1]"
                                        :css_class="'gradient-number-1'"
                                        :mode="Constants.COMMENT"
                                        />
                                </div> 
                            </div>
                            <div class="mt-2 col-md-6 col-sm-12 col-12">
                                <!-- COMMENT NUMBERS-->
                                <div class="row d-flex justify-content-center mb-2">
                                    <h2>top subreddits by comment karma</h2>
                                </div> 
                                <div class="row d-flex justify-content-center mb-2 num-list" id="list-comment-karma">
                                    <TopSubs v-for="(s, idx) in this.user.analysis.top_subs_by_karma.comment" 
                                        :key="'tck'+idx" 
                                        :rank="idx+1"
                                        :subreddit="s[0]"
                                        :count="s[1]"
                                        :css_class="'gradient-number'"
                                        :mode="Constants.COMMENT"
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
    name: "CommentStatistics",
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
                best_comment : true,
                worst_comment : true
            },
            best_comment: Utils.readMoreWrapper(
                this.user.analysis.summary.comments.best,
                this.user.gildings.best.comment
            ),
            worst_comment: Utils.readMoreWrapper(
                this.user.analysis.summary.comments.worst,
                this.user.gildings.worst.comment
            ),
            comment_stats: [
                { key: "comment count", value: Utils.formatNumber(this.user.analysis.summary.comments.count) },
                { key: "gilded comments", value: Utils.formatNumber(this.user.analysis.summary.comments.gilded) },
                { key: "karma", value: Utils.formatNumber(this.user.analysis.summary.comments.all_time_karma) },
                { key: "avg. karma per comment", value: Utils.formatNumber(this.user.analysis.summary.comments.average_karma) },
                { key: "word count", value: Utils.formatNumber(this.user.analysis.summary.comments.total_word_count) },
                { key: "unique word count", value: Utils.formatNumber(this.user.analysis.summary.comments.unique_word_count) },
                { key: "hours typed", value: Utils.formatNumber(this.user.analysis.summary.comments.hours_typed) },
                { key: "karma per word", value: Utils.formatNumber(this.user.analysis.summary.comments.karma_per_word) },
            ],
        };
    },
    watch: {
        worst_comment: {
            handler(){
            },
            deep: true
        }
    }
    /*computed: {
        best_comment_truncated: function() {
            return this.user.best_comment ? this.user.truncated.best_comment : true;
        },
        truncated.worst_comment: function () {
            return this.user.worst_comment ? this.user.truncated.worst_comment : true;
        }
    }*/
};
</script>