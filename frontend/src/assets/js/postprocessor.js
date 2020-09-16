// postprocessor.js
// This is not what you think it means
// This is literally a Reddit Post Processor

import Constants from "@/assets/js/config/Constants.js";
import moment from "moment-timezone";




// Set the starting date of the heatmap 59 days before today.
// To be used for the heatmap when iterating through the 
// comments and finding if any posts match this date.
var currentDate = (()=>{
    var cd = new Date();
    cd.setHours(0);
    cd.setMinutes(0);
    cd.setSeconds(0);
    cd.setMilliseconds(0);
    cd.setDate(cd.getDate() - 59);
    return cd;
})();

// Last 60 days in string format
var LAST_60_DAYS_STRING = (() => {
    var dates = {};
    for (var i = 0; i < 60 * 24; i++) {
        dates[moment(currentDate).format(Constants.HEATMAP_DATE_FORMAT)] = 0;
        currentDate.setHours(currentDate.getHours() + 1);
    }
    return dates;
})();

export default {
    process(submissions, comments, postCache) {
        
        var isCached = true;
        // Create a cache of timestamps
        if (!postCache || postCache.length==0) {
            postCache = [];   
            isCached = false;
        }

        var PKOverTime = {
            posts: {},
            karma: {},
            posts_cumu: {},
            karma_cumu: {},
            posts_tracker: 0,
            karma_tracker: 0,
        };

        var histogram = {
            day: {
                posts: [0, 0, 0, 0, 0, 0, 0],
                karma: [0, 0, 0, 0, 0, 0, 0],
            },
            hour: {
                posts: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                karma: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            }
        };


        function addActivityToPKOverTime (postDateTime, postKarma) {

            // Add to dictionary of recent activity (last 60 days) if doesn't exist.
            if (!(postDateTime.format("MMMM YYYY") in PKOverTime["posts"])) {
                PKOverTime["posts"][postDateTime.format("MMMM YYYY")] = 0;
                PKOverTime["karma"][postDateTime.format("MMMM YYYY")] = 0;
            }
            PKOverTime["posts"][postDateTime.format("MMMM YYYY")] += 1;
            PKOverTime["karma"][postDateTime.format("MMMM YYYY")] += postKarma;
            if (postDateTime.format(Constants.HEATMAP_DATE_FORMAT) in LAST_60_DAYS_STRING) {
                LAST_60_DAYS_STRING[postDateTime.format(Constants.HEATMAP_DATE_FORMAT)] += 1;
            }
        
        }

        function addActivityToHistogram (time, karma) {

            histogram.day.posts[Constants.DAY_KEYS[time.format("dddd")]] += 1;
            histogram.hour.posts[time.hour()] += 1;
        
            histogram.day.karma[Constants.DAY_KEYS[time.format("dddd")]] += karma;
            histogram.hour.karma[time.hour()] += karma;
        
        }

        function getPostTimeData(item) {
            // comment[3] is the unix timestamp of post date
            const postTimestamp = item[3];
            const postKarma = item[4];
            const postDateTime = moment.unix(postTimestamp).tz(Constants.Timezone);
            addActivityToHistogram(postDateTime, postKarma);
            addActivityToPKOverTime(postDateTime, postKarma);
            return postTimestamp;
        }

        var _x = 0;
        var _y = 0;
        var _xticker = 0;

        function g_x() {
            var ret = _x;
            _xticker += 1;
            _xticker %= 24;
            if (_xticker == 0)
                _x += 1;
            return ret;
        }

        function g_y() {
            var r = _y;
            _y += 1;
            _y %= 24;
            return r;
        }

        function IHeatMap(s) {
            var utc = moment(s, Constants.HEATMAP_DATE_FORMAT, Constants.Timezone).unix();
            var utc_today = moment().unix();
            if (utc < utc_today) {
                return {
                    x: g_x(),
                    y: g_y(),
                    value: LAST_60_DAYS_STRING[s],
                    tooltip_display: s
                };
            } else {
                return null;
            }

        }
        // var MODE_COMMENT = 0;
        // var MODE_SUBMISSION = 1;
        // var ss = MODE_COMMENT;

        if (postCache.length === 0) {
            comments.map(x => getPostTimeData(x));
            //ss = MODE_SUBMISSION;
            submissions.map(x => getPostTimeData(x));
            var getPostAndScore = x => [
                0,
                0,
                0,
                x[3],
                x[4],
                0,
                0,
                0,
                0,
            ];
            postCache.push(...comments.map(getPostAndScore));
            postCache.push(...submissions.map(getPostAndScore));
        } else {
            postCache.map(x => getPostTimeData(x));
        }
        
        var s = Object.keys(LAST_60_DAYS_STRING).map(s => IHeatMap(s));
        s = s.filter(e => e);
        var ratio = Math.max(...s.map(e => e.value / 15));
        s = s.map(v => (function(s) {
            s.original = s.value;
            s.value = s.value == 1 ? 1 : (Math.round(s.value / (ratio == 0 ? 1 : ratio)));
            return s;
        })(v));


        return {
            graphs: {
                heatmapData: s,
                histogram: histogram,
                PKOverTime: PKOverTime,
            },
            postCache: isCached ?  false : postCache
        };
    }
};