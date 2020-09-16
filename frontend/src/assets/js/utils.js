// import marked from "marked";
import moment from "moment-timezone";
import removeMd from "remove-markdown";

export default {
    validateUsername(u) {
        return /^[A-Za-z0-9_-]+$/.test(u);
    },

    sigmoid(val) {
        //var result = val;
        var result = 1/(1+Math.pow(Math.E,-1*val));
        // var result = Math.pow(val+20, 0.005); // this is a bad normalization function
        
        return result;
    },
    formatNumber (val, fixed) {
        var decimals = fixed || 2;
        var v = val.toString();
        var isNegative = v.startsWith("-");
        var ret = "";
        if (isNegative) {
            v = v.substring(1);
            ret = "-";
        }
        if (val >= 1000 && val <= 999999) {
            return ret + parseFloat(val / 1000).toFixed(decimals) + "k";
        } else if (val >= 1000000) {
            return ret + parseFloat(val / 1000000).toFixed(decimals) + "M";
        }
        return Math.round(val);
    },

    /*parseMarkdown: function(text) {
        return DomPurify.sanitize(marked(text));
    },*/
    
    regexSearch: function(text, word) {
        var regexp = new RegExp("(I'm|my|as a|my|I am|Im).+"+word);
        return text.match(regexp) ? text.match[0] : text;
    },

    removeMd: function(text) {
        return removeMd(text);
    },

    getFromNow: function(q) {
        return moment(new Date(q * 1000)).fromNow();
    },

    readMoreWrapper: function(msg, gildings) {
        if (!msg || msg == undefined){
            return {truncated: "true"};
        }
        var o = msg;
        o["truncated"]= true;
        o["more"]= false;
        o["full"] = msg.text || msg.selftext || msg.body;
        o["gildings"]= null;
        if (o["full"].split(/\r\n|\r|\n/).length > 4 || o["full"].length > 300) {
            if (o["full"].split(/\r\n|\r|\n/).length > 4) {

                o["more"] = true;
                o["text"] = o["full"].split(/\r\n|\r|\n/).slice(0, 4).join("\r\n") + " ...";
            }
            if (o["full"].length > 250) {
                o["more"] = true;
                o["text"] = o["full"].substring(0, 300) + " ...";
            }
        } else {
            o["more"] = false;
        }
        if (gildings) {
            o["gildings"] = {
                platinum: gildings.gid_3,
                gold: gildings.gid_2,
                silver: gildings.gid_1
            };
        }
        /*o["toggle"] = function() {
            debugger;
            this.truncated = !this.truncated;
            alert("sdfsf");
        }*/
        return o;
    }

};