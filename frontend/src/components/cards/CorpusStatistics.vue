<template>
    <ContentPanel title="corpus statistics">
        <div class="row mt-3">
            <div class="col-lg-6 col-md-6 col-12">
                <div class="row mb-2 d-flex justify-content-center" id="top-words">
                    <div class="col-12 d-flex justify-content-center">
                        <h2>Word Cloud</h2>
                    </div>
                    <div class="col-12 d-flex justify-content-center">
                        <p class="caption">Word size is proportional to word frequency.</p>
                    </div>
                    <div class="col-12 d-flex justify-content-center">
                        <p class="caption">{{ wordCloudCaption }}</p>
                    </div>
                    <div class="col-8 mt-1 d-flex justify-content-center">
                        <input v-model="wordcloudExcludeWords" type="range" class="custom-range" min="0" max="10" @change="excludeTopWords">
                    </div>
                    <div class="col-12 d-flex justify-content-center mt-1" id="word-cloud-container">
                        <div id="word-cloud"></div>
                    </div>
                </div> 
            </div>
            <div class="col-lg-6 col-md-6 col-12">
                <div class="row">
                    <div class="col-12 d-flex justify-content-center">
                        <h2>Word Frequency Table</h2>
                    </div>
                    <div class="col-12 d-flex justify-content-center">
                        <p class="caption">Scroll down the table to see more words.</p>
                    </div>
                    <div class="col-12 mt-3">
                        <div id="freq-table" class="ml-2 mr-2" :style="{'overflow':'scroll','height':wordcloudSize+'px'}">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th><p>Word</p></th>
                                        <th><p>Frequency</p></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(word,idx) in user.analysis.metrics.common_words" :key="'wc'+idx">
                                        <td><p>{{ word.text }}</p></td>
                                        <td><p>{{ word.size }}</p></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    
    
    </ContentPanel>
</template>
<script>
import Utils from "@/assets/js/utils.js";
import Wordcloud from "@/assets/js/graphs/wordcloud.js";

import ContentPanel from "../ContentPanel.vue";
import Constants from "@/assets/js/config/Constants.js";

export default {
    name: "CorpusStatistics",
    components: {
        ContentPanel
    },
    props: ["user"],
    data: function() {
        return {
            Constants,
            Utils,
            wordcloudExcludeWords: 0,
            wordcloudSize: 0,
            document,
        };
        
    },
    mounted: function() {
        this.wordcloudSize = Math.min(430,document.getElementById("word-cloud-container").offsetWidth*0.9);
        Wordcloud.generate(this.user.analysis.metrics.common_words, 0);
    },
    computed: {
        wordCloudCaption: function() {
            if (this.wordcloudExcludeWords == 0) {
                return "Showing all words. Drag slider to exclude top words.";
            } else {
                return "Excluded top " + this.wordcloudExcludeWords + " words.";
            }
        }
    },
    methods: {
        excludeTopWords: function() {
            Wordcloud.generate(this.user.analysis.metrics.common_words, this.wordcloudExcludeWords);
        }
    }
};
</script>