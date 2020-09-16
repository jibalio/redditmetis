<template>
    <div class="row gray-container ml-1 mr-1 round-edge shadow-sm">
            <div class="col-12" ref="wrapper"><slot v-html="rawHtml" ></slot></div>
            <div class="col-12" v-if="gildings && (gildings.platinum || gildings.gold || gildings.silver)">
                <p class="caption">
                    <span v-if="gildings.platinum" class="mr-1"><img src="https://www.redditstatic.com/gold/awards/icon/platinum_16.png" /> x{{gildings.platinum}}</span>
                    <span v-if="gildings.gold" class="mr-1"><img src="https://www.redditstatic.com/gold/awards/icon/gold_16.png" /> x{{gildings.gold}}</span>
                    <span v-if="gildings.silver" class="mr-1"><img src="https://www.redditstatic.com/gold/awards/icon/silver_16.png" /> x{{gildings.silver}}</span>
                </p>
            </div>
            <div class="col-12 mt-2"  v-if="!hidedetails" >
                <p class="float-left caption"><a :href="'https://reddit.com/r/'+subreddit">r/{{subreddit}}</a></p>
                <p class="float-right caption">
                    <span :class="votes>0?'upvoted':'downvoted'" >{{votes | cleanNumber(1)}}</span> • 
                    <span>{{ fromnow }}</span> •
                    <span><a :href="permalink" target="_blank">permalink</a></span>
                </p>
            </div>
        </div>
</template>

<script>
export default {
    name: "CommentContainer",
    props: ["votes", "subreddit", "fromnow", "permalink", "hidedetails", "gildings"],
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

    
</style>
