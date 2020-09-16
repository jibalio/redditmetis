<template>
    <ContentPanel title="basic information" class="mt-4">
        <div class="row">
            <div class="col-lg-6 col-md-6 col-12">
                <div class="row">
                    <div class="col-12 mt-3">
                        <h2>about</h2>
                    </div>
                    <div class="col-md-5 col-6">
                        <p class="sublabel">username:</p>
                        <p class="sublabel">cake day</p>
                        <p class="sublabel">link karma</p>
                        <p class="sublabel">comment karma</p>
                        <p class="sublabel">total karma</p>
                    </div>
                    <div class="col-md-7 col-6">
                        <p id="text-username">{{user.analysis.username}}</p>
                        <p
                            id="text-joined"
                            >{{ moment.unix(user.about.created_utc).tz(this.Constants.Timezone).format("MMMM DD, YYYY HH:mm") }}</p>
                        <p id="text-link_karma">{{user.about.link_karma}}</p>
                        <p id="text-comment_karma">{{user.about.comment_karma}}</p>
                        <p id="text-total_karma">{{user.about.link_karma + user.about.comment_karma}}</p>
                    </div>
                    <div class="col-12 mt-3">
                        <h2>text readability</h2>
                    </div>
                    <div class="col-12">
                        <p class="caption">
                            Calculated using the Gunning fog index.
                            <a
                                href="https://en.wikipedia.org/wiki/Gunning_fog_index"
                                target="_blank"
                                >What's a fog index?</a>
                        </p>
                        <p
                            class="caption"
                            >Note: This measures what reading level is needed to understand your texts. A higher fog index does not necessarily mean good writing.</p>
                    </div>
                    <div class="col-md-5 col-6">
                        <p class="sublabel">fog index</p>
                        <p class="sublabel">text complexity</p>
                    </div>
                    <div class="col-md-7 col-6 mb-3">
                        <p id="fog-number" :style="{ color:  gfIndex.color }">{{ gfIndex.index }}</p>
                        <p id="fog-measure" :style="{ color:  gfIndex.color }">{{ gfIndex.measure }}</p>
                    </div>
                    <div class="col-12 mt-3">
                        <h2>wholesomeness meter</h2>
                    </div>
                    <div class="col-12">
                        <p
                            class="caption"
                            >Results were gathered through machine learning methods and natural language processing.</p>
                        <p class="caption">Take this with a grain of salt.</p>
                    </div>
                    <!-- SENTIMENT ANALYSIS -->
                    <div class="col-12 ml-1 mr-4 mt-3">
                        <div class="row" style="margin-right: 25%;">
                            <div class="col-6" style="padding-right:0px;">
                                <div class="d-flex justify-content-start">
                                    <p class="caption">Unwholesome</p>
                                </div>
                            </div>
                            <div class="col-6" style="padding-left:0px;">
                                <div class="d-flex justify-content-end">
                                    <p class="caption">Wholesome</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 ml-1 mr-4">
                        <div class="row" style="margin-right: 25%;">
                            <div class="col-6" style="padding-right:0px;">
                                <div class="progress d-flex justify-content-end round-edge-left">
                                    <div
                                        :style="{width: wholesomenessMeter.offset_n+'%'}"
                                        id="sentiment-left"
                                        class="progress-bar bg-blue"
                                        role="progressbar"
                                        style="color:#808080;"
                                        >-{{ wholesomenessMeter.offset_n ? wholesomenessMeter.offset_n+'%' : '' }}</div>
                                </div>
                            </div>
                            <div class="col-6" style="padding-left:0px;">
                                <div class="progress round-edge-right">
                                    <div
                                        :style="{width: wholesomenessMeter.offset_p+'%'}"
                                        id="sentiment-right"
                                        class="progress-bar bg-green"
                                        role="progressbar"
                                        style="color:#808080;"
                                        >{{ wholesomenessMeter.offset_p ? wholesomenessMeter.offset_p+'%' : '' }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 mt-4">
                        <p class="sublabel">most wholesome comment</p>
                    </div>
                    <div class="col-12">
                        <CommentContainer
                            :votes="mpc.votes"
                            :subreddit="mpc.sub"
                            :fromnow="getFromNow(mpc.created_utc)"
                            :permalink="mpc.permalink"
                            :gildings="mpc.gildings"
                            >
                            <span v-if="truncated.mpc" v-html="marked(mpc.text)"></span>
                            <span v-if="!truncated.mpc" v-html="marked(mpc.full)"></span>
                            <span v-if="mpc.more">
                            <a
                                @click="truncated.mpc=!truncated.mpc"
                                href="#!"
                                onclick="return false;"
                                >{{ truncated.mpc ? 'Read more' : 'Show less' }}</a>
                            </span>
                        </CommentContainer>
                    </div>
                    <div class="col-12 mt-2">
                        <p class="sublabel">least wholesome comment</p>
                    </div>
                    <div class="col-12">
                        <CommentContainer
                            :votes="mnc.votes"
                            :subreddit="mnc.sub"
                            :fromnow="getFromNow(mnc.created_utc)"
                            :permalink="mnc.permalink"
                            :gildings="mnc.gildings"
                            >
                            <span v-if="truncated.mnc" v-html="marked(mnc.text)"></span>
                            <span v-if="!truncated.mnc" v-html="marked(mnc.full)"></span>
                            <span v-if="mnc.more">
                            <a
                                @click="truncated.mnc=!truncated.mnc"
                                href="#!"
                                >{{ truncated.mnc ? 'Read more' : 'Show less' }}</a>
                            </span>
                        </CommentContainer>
                    </div>
                    <div class="col-12 mt-3">
                        <h2>help improve data</h2>
                        <p
                            class="caption"
                            >To train the machine, we need data! Help gather data by answering the question below. This will help the machine generate cooler statistics in the future.</p>
                        <p
                            class="caption"
                            >Below is a random comment pulled from Reddit. What is the emotion shown in this comment?</p>
                    </div>
                    <div id="improve_sentiment_container" class="col-12 mt-2">
                        <div class="row">
                            <div class="col-12">
                                <transition name="transition-class" enter-active-class="animated fadeIn">
                                    <CommentContainer v-if="!submittingImproveData && !skipSentiment" :hidedetails="true">
                                        <span
                                            v-if="truncated.randomCommentSentimentRm"
                                            v-html="marked(randomCommentSentimentRm.text)"
                                            ></span>
                                        <span
                                            v-if="!truncated.randomCommentSentimentRm"
                                            v-html="marked(randomCommentSentimentRm.full)"
                                            ></span>
                                        <span v-if="randomCommentSentimentRm.more">
                                        <a
                                            @click="truncated.randomCommentSentimentRm=!truncated.randomCommentSentimentRm"
                                            href="#!" onclick="return false;"
                                            >{{ truncated.randomCommentSentimentRm ? 'Read more' : 'Show less' }}</a>
                                        </span>
                                    </CommentContainer>
                                </transition>
                                <transition name="transition-class2" enter-active-class="animated fadeIn">
                                    <div v-if="submittingImproveData || skipSentiment" class="d-flex justify-content-center mt-2 row">
                                        <div class="col-12 d-flex justify-content-center">
                                            <div
                                                role="status"
                                                class="spinner-border text-info"
                                                style="width:30px;height:30px"
                                                >
                                                <span class="sr-only"></span>
                                            </div>
                                        </div>
                                        <div class="col-12 d-flex justify-content-center mt-1 mb-1">
                                            <p v-if="!skipSentiment">Thanks! You're Awesome!</p>
                                        </div>
                                    </div>
                                </transition>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12 mt-2">
                                <button
                                    type="button"
                                    class="btn btn-outline-success btn-sm space-left mt-1"
                                    @click="submitImproveData('happy')"
                                    :disabled="submittingImproveData"
                                    >Happy</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-warning btn-sm space-left mt-1"
                                    @click="submitImproveData('sad')"
                                    :disabled="submittingImproveData"
                                    >Sad</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-info btn-sm space-left mt-1"
                                    @click="submitImproveData('surprised')"
                                    :disabled="submittingImproveData"
                                    >Suprised</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-danger btn-sm space-left mt-1"
                                    @click="submitImproveData('angry')"
                                    :disabled="submittingImproveData"
                                    >Angry</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-purple btn-sm space-left mt-1"
                                    @click="submitImproveData('bored')"
                                    :disabled="submittingImproveData"
                                    >Bored</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-secondary btn-sm space-left mt-1"
                                    @click="submitImproveData('neutral')"
                                    :disabled="submittingImproveData"
                                    >Neutral</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-secondary btn-sm space-left mt-1"
                                    @click="submitImproveData('trash')"
                                    :disabled="submittingImproveData"
                                    >Spam/Gibberish/Bot</button>
                                <button
                                    type="button"
                                    class="btn btn-outline-secondary btn-sm space-left mt-1"
                                    @click="skipComment()"
                                    :disabled="submittingImproveData"
                                    >Skip</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Synopsis -->
            <div class="col-lg-6 col-md-6 col-12">
                <div class="row">
                    <div class="col-12 mt-3">
                        <h2>synopsis</h2>
                    </div>
                    <div class="col-12">
                        <p class="caption">Click on the # to view sources.</p>
                    </div>
                    <div v-for="(s,property) in user.analysis.synopsis" class="col-12 mt-3" :key="property">
                        <div v-if="s.data">
                            <div class="row">
                                <div class="col-lg-4 col-md-4 col-12">
                                    <p class="sublabel">{{Enum.SYNOPSIS_KEYS[property]}}</p>
                                </div>
                                <div class="col-lg-8 col-md-8 col-12">
                                    <p v-for="(data, didx) in s.data" class="mb-3 ml-2 sublabel" :key="'syndata'+didx">
                                        <!-- LAZY POPPOVER -->
                                        <!-- <span class="guess mr-2  shadow-sm">{{ data.value }}</span>
                                        <span :id="'src'+idx+'-'+property" v-for="(source,idx) in data.sources" class="mr-1 sublabel guess-dots" :key="source">
                                            <a :href="source" target="_blank">&#8226;</a>
                                        
                                        <b-popover :id="'srcpopover'+idx+'-'+property" :target="'src'+idx+'-'+property" triggers="hover" placement="top" style="max-width:300px">
                                            <CommentContainerLazy
                                                :permalink="source"
                                                :synopsis_word="data.value"
                                            />
                                        </b-popover>
                                        
                                        </span>-->
                                        <span class="guess mr-2  shadow-sm">{{ data.value }}</span>
                                        <span :id="'src'+idx+'-'+property" v-for="(source,idx) in data.sources" class="mr-1 sublabel" :key="source">
                                            <a :href="source" target="_blank">#</a>
                                        </span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </ContentPanel>
</template>
<style scoped>
.guess-dots a {
    color: #a6afad;
}
.guess-dots a:hover {
        color: #00B894;
        text-decoration: none;
}
</style>
<script>
// import Heatmapper from "@/assets/js/activitymapper";
import ContentPanel from "../ContentPanel.vue";
import CommentContainer from "../CommentContainer.vue";
// import CommentContainerLazy from "../CommentContainerLazy.vue";
import moment from "moment-timezone";
// import DomPurify from "dompurify";
import marked from "marked";
// import {BPopover} from "bootstrap-vue"

export default {
    name: "BasicInformation",
    components: {
        ContentPanel,
        CommentContainer,
        // CommentContainerLazy,
        // "b-popover": BPopover,
    },
    props: ["user"],
    data: function() {
        return {
            moment,
            marked,
            // DomPurify,
            truncated: {
                mnc: true,
                mpc: true,
                randomCommentSentimentRm: true
            },
            randomCommentSentiment: null,
            submittingImproveData: false,
            skipSentiment: false
        };
    },
    methods: {
        submitImproveData: function(emotion) {
            this.submittingImproveData = true;
            this.MetisClient.submitImproveData(
                this.randomCommentSentimentRm.full,
                emotion
            );
            this.getRandomComment();
        },
        getRandomComment() {
            this.submittingImproveData = true;
            this.MetisClient.getRandomComment().then(data => {
                this.submittingImproveData = false;
                this.skipSentiment = false;
                this.randomCommentSentiment = {
                    full: data,
                    text: data
                };
            });
        },
        tanh: q => 2 / (1 + Math.pow(Math.E, -4 * q)) - 1,
        getFromNow: function(q) {
            return moment(new Date(q * 1000)).fromNow();
        },
        skipComment: function() {
            this.skipSentiment = true;
            this.getRandomComment();
        },
        readMoreWrapper: function(msg) {
            msg["full"] = msg.full || msg.text;
            if (!msg) {
                return;
            }

            if (msg.text.split(/\r\n|\r|\n/).length > 4 || msg.text.length > 300) {
                if (msg.text.split(/\r\n|\r|\n/).length > 4) {
                    msg["more"] = true;
                    msg["text"] =
                        msg.text
                            .split(/\r\n|\r|\n/)
                            .slice(0, 4)
                            .join("\r\n") + " ...";
                }
                if (msg.text.length > 250) {
                    msg["more"] = true;
                    msg["text"] = msg.text.substring(0, 300) + " ...";
                }
            } else {
                msg["more"] = false;
            }
            return msg;
        }
    },
    computed: {
        icon_img: function() {
            return this.user.about.icon_img.split("?")[0];
        },
        gfIndex: function() {
            var index = Math.min(Math.round(this.user.analysis.readability["gf-index"]), 17);
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
            return {
                index,
                color,
                measure
            };
        },
        wholesomenessMeter: function() {
            var sentiments = this.user.analysis.sentiments;
            // var mpc = sentiments.most_positive_comment;
            // var mnc = sentiments.most_negative_comment;
            var total_sentiments = sentiments.negative + sentiments.positive;
            var offset =
                (sentiments.positive - sentiments.negative) / total_sentiments;

            var offset_n = 0;
            var offset_p = 0;
            if (offset < 0) {
                offset_n = Math.round(this.tanh(offset * -1) * 100);
            } else {
                offset_p = Math.round(this.tanh(offset) * 100);
            }
            return {
                offset_n,
                offset_p
            };
        },
        mpc: function() {
            var a = this.readMoreWrapper(this.user.analysis.sentiments.most_positive_comment);
            if (this.user.gildings.mpc) {
                a["gildings"] = {
                    platinum: this.user.gildings.mpc.gid_3,
                    gold: this.user.gildings.mpc.gid_2,
                    silver: this.user.gildings.mpc.gid_1
                };
            }
            return a;
        },
        mnc: function() {
            var a = this.readMoreWrapper(this.user.analysis.sentiments.most_negative_comment);
            if (this.user.gildings.mnc) {
                a["gildings"] = {
                    platinum: this.user.gildings.mnc.gid_3,
                    gold: this.user.gildings.mnc.gid_2,
                    silver: this.user.gildings.mnc.gid_1
                };
            }
            return a;
        },

        randomCommentSentimentRm: function() {
            if (!this.randomCommentSentiment) {
                return {
                    text: ""
                };
            } else {
                return this.readMoreWrapper(this.randomCommentSentiment);
            }
        },
        best_comment: function() {
            var a = this.readMoreWrapper(this.user.analysis.summary.comments.best);
            if (this.user.gildings.best.comment) {
                a["gildings"] = {
                    platinum: this.user.gildings.best.comment.gid_3,
                    gold: this.user.gildings.best.comment.gid_2,
                    silver: this.user.gildings.best.comment.gid_1
                };
            }
            return a;
        },
        worst_comment: function() {
            var a = this.readMoreWrapper(this.user.analysis.summary.comments.worst);
            if (this.user.gildings.worst.comment) {
                a["gildings"] = {
                    platinum: this.user.gildings.worst.comment.gid_3,
                    gold: this.user.gildings.worst.comment.gid_2,
                    silver: this.user.gildings.worst.comment.gid_1
                };
            }
            return a;
        },
        best_submission: function() {
            var a = this.user.analysis.summary.submissions.best;
            if (this.user.gildings.best.submission) {
                a["gildings"] = {
                    platinum: this.user.gildings.best.submission.gid_3,
                    gold: this.user.gildings.best.submission.gid_2,
                    silver: this.user.gildings.best.submission.gid_1
                };
            }
            return a;
        },
        worst_submission: function() {
            var a = this.user.analysis.summary.submissions.worst;
            if (this.user.gildings.worst.submission) {
                a["gildings"] = {
                    platinum: this.user.gildings.worst.submission.gid_3,
                    gold: this.user.gildings.worst.submission.gid_2,
                    silver: this.user.gildings.worst.submission.gid_1
                };
            }
            return a;
        }
    },
    created: function() {
        this.skipSentiment = true;
        this.getRandomComment();
    }
};
</script>