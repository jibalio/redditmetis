
<template>
    <div>
        <div v-if="!post" role="status" class="spinner-border text-info" :style="{width:'15px',height:'15px'}"><span class="sr-only"></span></div>
        <CommentContainer v-if="post"
            :votes="post.votes"
            :subreddit="post.subreddit"
            :fromnow="Utils.getFromNow(post.created_utc)"
            :permalink="post.permalink"
            >
            <span v-if="truncated" v-html="Utils.removeMd(post.text)"></span>
            <span v-if="!truncated" v-html="Utils.removeMd(post.full)"></span>
            <span v-if="post.more">
            <a
                @click="truncated=!truncated"
                href="#!"
                >{{ truncated ? 'Read more' : 'Show less'}}</a>
            </span>
        </CommentContainer>
    </div>
</template>

<script>
import Utils from "@/assets/js/utils.js";
import CommentContainer from "./CommentContainer.vue";
export default {
    name: "CommentContainerLazy",
    props: ["permalink", "synopsis_word"],
    components: {CommentContainer,},
    data: function() {
        return {
            Utils,
            truncated: true,
            loaded: false,
            votes: 0,
            subreddit: "",
            created_utc: 0,
            post: null
        }
    },
    methods: {
        async getPostFromLink() {
            var permalink = this.permalink;
            
            var res = await this.MetisClient.getPostFromLink(permalink);
            
            this.loaded = true;

            var a = Utils.readMoreWrapper(
                res[0].data.children[0].data
            );
            this.post = a;
        }
    },
    mounted: function() {
        
        this.getPostFromLink();
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

    
</style>
