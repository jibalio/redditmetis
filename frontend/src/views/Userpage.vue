<template>
    <div>
        <Navbar class="fixed-top shadow-sm" ref="ref_navbar" ></Navbar>

        <div :style="containerStyle">


            <!-- LOADING -->
            <div class="row d-flex justify-content-center align-items-center" v-if="!error && status<2" 
                style="min-height: 80vh;height: 80%;">
                <div class="col-md-4 col-lg-4 col-12">
                    <div class="row" >
                        <div v-if="status==0" class="col-12 d-flex justify-content-center">
                            <div id="progress-circle" style="width:80px;"></div>
                        </div>
                        <div v-if="status==1" class="col-12 d-flex justify-content-center">
                            <div role="status" class="spinner-border text-info" style="width:75px;height:75px;"><span class="sr-only"></span></div>
                        </div>
                        <div v-if="status!=-1" class="col-12 d-flex justify-content-center">
                            <p class="mt-3">{{loadText}}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ERROR -->

            <div :key="$route.fullPath" class="row d-flex justify-content-center" v-if="status==-1 || error">
                <div class="col-md-4 col-lg-4 col-xs-5 col-10" style="padding:30px">
                    <div class="row d-flex justify-content-center">
                        <div class="col-12 d-flex justify-content-center" v-if="error.name == 'UserNotFoundError' || error.name=='InvalidUserError' || error.name=='BannedUserError'">
                                <img :src="require('@/assets/img/snoo_gray.png')" class="snoovatar round-edge" height="75px" width="75px"/>
                        </div>
                        <div class="col-12 d-flex justify-content-center mt-2">
                            <h1 v-if="error.name == 'UserNotFoundError'">That user does not exist</h1>
                            <h1 v-if="error.name == 'InvalidUserError'">That username is invalid</h1>
                            <h1 v-if="error.name == 'BannedUserError'">That user is banned</h1>
                            <h1 v-if="error.name == 'UnexpectedError'">An unexpected error has occured</h1>
                        </div>

                        <div v-if="error.name == 'UserNotFoundError'">
                            <div class="col-12 d-flex justify-content-center mt-2">
                                <p><strong>U/{{$route.params.uname}}</strong> does not exist. Check the spelling of the username.</p>
                            </div>
                            <div class="col-12 d-flex justify-content-center">
                                <p class="caption">Usernames are NOT case sensitive, and a 'u/' in front is not required.</p>
                            </div>
                            <div class="col-12 d-flex justify-content-center mt-4">
                                <p>Or try searching for another user.</p>
                            </div>
                        </div>

                        <div v-if="error.name == 'InvalidUserError'">
                            <div class="col-12 d-flex justify-content-center mt-2">
                                <p><strong>U/{{$route.params.uname}}</strong> is not a valid username.</p>
                            </div>
                            <div class="col-12 d-flex justify-content-center">
                                <p class="caption">Usernames are NOT case sensitive, and a 'u/' in front is not required.</p>
                            </div>
                            <div class="col-12 d-flex justify-content-center mt-4">
                                <p>Or try searching for another user.</p>
                            </div>
                        </div>

                        <div v-if="error.name == 'BannedUserError'">
                            <div class="col-12 d-flex justify-content-center mt-2">
                                <p><strong>U/{{$route.params.uname}}</strong> is a banned user.</p>
                            </div>
                            <div class="col-12 d-flex justify-content-center mt-4">
                                <p>Try searching for another user.</p>
                            </div>
                        </div>

                        <div v-if="error.name == 'UnexpectedError'">
                            <div class="col-12 d-flex justify-content-center mt-2">
                                <p>An unexpected error has occured. <br />Some browser plugins/content blockers prevent RedditMetis from reaching Reddit. Try disabling those or use a different browser.</p>
                            </div>
                            <div class="col-12 d-flex justify-content-center mt-4">
                                <p>Or try searching for another user.</p>
                            </div>
                        </div>

                        <div class="col-md-9 col-lg-9 col-12 d-flex justify-content-center mt-2">
                            
                            <div class="d-flex justify-content-center shadow-sm mt-1" style="width:70%" tabindex="0">
                                <div class="input-group-prepend">
                                    <span id="basic-addon3" class="input-group-text round-edge-left bg-gradient" style="color:#22655a;">u/</span>
                                </div>
                                <input v-on:keyup.enter="search(searchBarText)" v-model="searchBarText" type="text" aria-describedby="basic-addon3" placeholder="Username" class="err-input form-control flex-fill no-border round-edge-right" >
                            </div>

                              <b-button @click="search(searchBarText);" class="ml-2 shadow-sm bg-gradient no-border errsearchbutton" style="width:30%">Search</b-button>  
                        </div>
                        
                    </div>
                </div>
            </div>

            <Result :key="$route.fullPath" :user="user" v-if="status==2"></Result>
        </div>
        

    </div>
</template>
<style scoped>
#navbar_upage {
    background-image: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
}

.errsearchbutton {
    margin-top: 4px;
    height: 92%;
    width:100%;
}

.err-input {
    height: calc(1.4em + 0.75rem + 2px);font-family: 'Nunito', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 0.9rem;
    color: #353535;
    margin: 0 0 0 0;
}

p,h1,h2 {
    text-align: center;
}
 
</style>
<script>

// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';
import Utils from "@/assets/js/utils.js";
import Navbar from "@/components/Navbar.vue";
import Result from "@/components/Result.vue";
import PostProcessor from "@/assets/js/postprocessor.js";
import Constants from "@/assets/js/config/Constants.js";
import ProgressBar from "progressbar.js";
import {BButton} from "bootstrap-vue";
export default {
    name: "Home",
    components: {
        Navbar,
        Result,
        "b-button":BButton,
    },
    data: function() {
        return this.initialState();
    },
    metaInfo() {
        return {
            title: this.pagetitle,
        };
    },
    mounted: function() { 
        this.$nextTick(this.initializeLoadBar);
        if (!Utils.validateUsername(this.$route.params.uname)){
            this.error = Constants.Error.InvalidUserError;
        } else {
            this.analyze(this.$route.params.uname);
        }
    },
    computed : {
        pagetitle: function() {
            if (!this.error) {
                return "u/"+this.$route.params.uname + " on RedditMetis - A Reddit User Analyzer";
            } else {
                return "RedditMetis - Error";
            }
        },
        containerStyle: function() {
            if ((!this.error && this.status<2) || (this.status==-1 || this.error)){
                return {
                    "margin-top":this.navHeight+"px",
                    "overflow":"hidden",
                };
            } else {
                return {
                    "margin-top":this.navHeight+"px",
                };
            }
            
            
        }
    },
    methods: {
        initializeLoadBar() {
            
            
            this.navHeight = this.$refs.ref_navbar.$el.clientHeight+50;
            this.bar = new ProgressBar.Circle("#progress-circle", {
                color: "#353535",
                // This has to be the same size as the maximum width to
                // prevent clipping
                strokeWidth: 4,
                trailWidth: 1,
                easing: "easeInOut",
                duration: 1400,
                text: {
                    autoStyleContainer: false
                },
                from: { color: "#00b894", width: 1 },
                to: { color: "#00b894", width: 1 },
                step: function(state, circle) {
                    circle.path.setAttribute("stroke", state.color);
                    circle.path.setAttribute("stroke-width", state.width);
                    var value = Math.round(circle.value() * 100);
                    if (value === 0) {
                        circle.setText("");
                    } else {
                        circle.setText(value + "%");
                    }
                }
            });
        },
        initialState() {
            return {
                searchBarText: "",
                user:{
                    analysis: null,
                    about: null,
                    postCache: null,
                    gildings: {
                        best: {
                            comment: null,
                            submission: null,
                        },
                        worst: {
                            comment: null,
                            submission: null,
                        },
                        mpc: null,
                        mnc: null,
                    },
                },
                submittingImproveData: false,
                navHeight: 0,
                loadText: "",
                status: 0,
                error: null,
                bar: null,
                progress: 0,
            };
        },

        search(userName) {
            this.$router.push({name:"userpage",params:{
                uname: userName.trim()
            }});
        },
        
        handleError (error) {
            this.error = error;
            this.status = -1;
        },

        async analyze(userName) {

            try {
                this.loadText = "Retrieving User Info";
                var about, comments, submissions, result, decoded, processResults;

                

                about = await this.MetisClient.getAbout(userName, ()=>{
                    this.$nextTick(function() {
                        this.incrementProgress(0.10);
                    });
                });
                
                
                if (about.is_suspended){
                    this.handleError(Constants.Error.BannedUserError);
                    return;
                }

                if (about.error) {
                    var error = about;
                    this.handleError(error);
                    this.metaInfo.title = this.pagetitle;
                    return;
                }

                var path = this.$route.path;
                var fixedPath = "/user/"+about.name;
                if (path !== fixedPath)
                    this.$router.replace({path: fixedPath});

                
                this.user.about = about;
                // Check if this user exists in the cache.
                var useCache = Constants.USE_RESULT_CACHE;
                var cachedCopy = useCache ? await this.MetisClient.check(userName) : {"exists":false};
                if (cachedCopy.exists) {
                    decoded = JSON.parse(this.MetisClient.decode(cachedCopy.result));
                    var postCache = JSON.parse(this.MetisClient.decode(cachedCopy.postTimestamps));
                    this.user.postCache = JSON.parse(postCache);
                    processResults = PostProcessor.process(false, false, JSON.parse(postCache));
                } else {

                    this.loadText = "Retrieving Comments";
                    comments = await this.MetisClient.getComments(userName, ()=>{
                        this.$nextTick(function() {
                            this.incrementProgress(0.03);
                        });
                    }); // onTick function
                    
                    this.loadText = "Retrieving Submissions";
                    submissions = await this.MetisClient.getSubmissions(userName, ()=>{
                        this.$nextTick(function() {
                            this.incrementProgress(0.03);
                        });
                    }); //onTick

                    this.loadText = "Analyzing User";
                    processResults = PostProcessor.process(submissions, comments);

                    this.status = 1;
                    
                    result = await this.MetisClient.getAnalysis(about,comments,submissions);
                    var response = result["response"];
                    decoded = result["decoded"];

                }
                //this.incrementProgress(1-this.progress);
                this.user.postCache = processResults.postCache;
                this.user.heatmapData = processResults.graphs.heatmapData;
                this.user.histogram = processResults.graphs.histogram;
                this.user.PKOverTime = processResults.graphs.PKOverTime;
                
                var best_comment_id = "t1_" + decoded.summary.comments.best.permalink.split("/")[8];
                var worst_comment_id = "t1_" + decoded.summary.comments.worst.permalink.split("/")[8];
                var best_submission_id = "t3_" + decoded.summary.submissions.best.permalink.split("/")[6];
                var worst_submission_id = "t3_" + decoded.summary.submissions.worst.permalink.split("/")[6];
                var mpc_id = "t1_" + decoded.sentiments.most_positive_comment.permalink.split("/")[8];
                var mnc_id = "t1_" + decoded.sentiments.most_negative_comment.permalink.split("/")[8];
                var ids = [best_comment_id,worst_comment_id,best_submission_id,worst_submission_id,mpc_id,mnc_id];

                var results = await this.MetisClient.getGildings(ids);

                this.user.gildings.best.comment = results[0].data.gildings;
                this.user.gildings.worst.comment = results[1].data.gildings;
                this.user.gildings.best.submission = results[2].data.gildings;
                this.user.gildings.worst.submission = results[3].data.gildings;
                this.user.gildings.mpc = results[4].data.gildings;
                this.user.gildings.mnc = results[5].data.gildings;

                
                this.user.analysis = decoded;
                

                if (!cachedCopy.exists) {
                    // Save the results to the cache
                    var savePayload = {};
                    savePayload["ts"] = this.MetisClient.encode(JSON.stringify(this.user.postCache));
                    savePayload["u"] = userName;
                    savePayload["b"] = response["b"];
                    this.MetisClient.save(savePayload);
                }
                this.status = 2;
            } catch(err) {
                this.handleError(Constants.Error.UnexpectedError);
                
            }
        },

        incrementProgress(f) {
            this.progress += f;
            this.bar.animate(this.progress);
        },
    }
};
</script>
