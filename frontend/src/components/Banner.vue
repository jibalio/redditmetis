<template>
    
    <div>
        <div id="banner" class="row d-flex justify-content-center align-items-center">
            <div class="col-md-5 col-6" style="padding-right:50px">
                <div class="row">
                    <div class="col-md-7 col-12">
                        <h1
                            style="color:white;font-size:5.5vh;font-weight:400"
                            class="small-caps-lower"
                        >See statistics for your Reddit account</h1>
                        <button @click="$emit('debug',0)">test:debug</button>
                    </div>
                    <div class="col-md-12 col-12">
                        <p
                            class="color-white"
                        >Enter your username below to see your Reddit Statistics - recent activity, comment and submissions summaries, word cloud, and more interesting stats. Data is generated from the last 1000 comments and submissions.</p>
                    </div>
                    <div class="col-md-12 col-12 d-flex justify-content-center mt-4">
                        <div class="input-group-prepend">
                            <span class="input-group-text round-edge-left" id="basic-addon3">u/</span>
                        </div>
                        <input
                            v-model.trim="username"
                            type="text"
                            class="form-control round-edge-right"
                            id="input_username_index"
                            aria-describedby="basic-addon3"
                        />
                    </div>
                    <div class="col-md-12 col-12 d-flex justify-content-center mt-2">
                        <button
                            id="search-button_index"
                            type="button"
                            class="btn btn-info"
                            @click="$emit('search_username', username)"
                            style="width:100%">
                                Analyze
                            </button>
                    </div>
                </div>
                <div class="col-12 mt-3">
                    <a href="#" onclick="get_random_user()">
                        <p id="btn-random">See a random Redditor's profile instead</p>
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Banner",
    data: function() {
        return {
            username: "",
        };
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#banner {
    background-image: linear-gradient(160deg, #89c9e8 0%, #77e6a1 100%);
    padding: 5%;
}

#btn-random {
    color: white;
    text-decoration: dotted;
    text-decoration-line: underline;
}
</style>
