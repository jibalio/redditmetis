import axios from "axios";
import moment from "moment-timezone";
import pako from "pako";

import Constants from "./config/Constants.js";
import Enum from "./config/Enum.js";
import LambdaClient from "./AwsWrapper.js";

export default class MetisClient {
    
    
    constructor () {
        this.timezone = moment.tz.guess();
        axios.interceptors.response.use((response) => response, (error) => {
            
            return Promise.reject(error);
        });
    }

    // Returns boolean if gg.
    test() {
        axios.get("https://www.reddit.com/r/redditmetis.json?limit=1");
        
    }

    async getAbout(username, onTick){
        var data;
        onTick();
        try {
            data = (await axios.get(`https://www.reddit.com/user/${username}/about.json`)).data.data;
            onTick();
            
        } catch (err) {
            
            if (err.response) {
                
                data = Constants.Error.UserNotFoundError;
            } else {
                data = Constants.Error.UnexpectedError;
            }
        }
        return new Promise (resolve => {
            resolve(data);
        });
    }


    async getDataRecursive(username, mode, onTick) {

        var base_url;
        if (mode === 0) {
            base_url = `https://www.reddit.com/user/${username}/comments/.json?limit=100`;
        } else {
            base_url = `https://www.reddit.com/user/${username}/submitted/.json?limit=100`;
        }

        var after = "";
        var data = [];

        while(after!=null){
            var url = base_url;
            url = base_url+(after===""? "" : "&after="+after);
            var response = (await axios.get(url))["data"];
            var children = response["data"]["children"];
            after = response["data"]["after"];
            
            if (mode !== 0) { 
                children.forEach(function(child) {
                    data.push([
                        child["data"]["id"],
                        child["data"]["subreddit"],
                        child["data"]["selftext"],
                        child["data"]["created_utc"],
                        child["data"]["score"],
                        child["data"]["permalink"].toLowerCase(),
                        child["data"]["url"].toLowerCase(),
                        child["data"]["title"],
                        child["data"]["is_self"],
                        child["data"]["gilded"],
                        child["data"]["domain"],
                    ]);
                });
            } else {
                children.forEach(child => {
                    data.push([
                        child["data"]["id"],
                        child["data"]["subreddit"],
                        child["data"]["body"],
                        child["data"]["created_utc"],
                        child["data"]["score"],
                        child["data"]["link_id"].toLowerCase().substring(3),
                        child["data"]["edited"],
                        child["data"]["parent_id"].startsWith("t3"),
                        child["data"]["gilded"],
                    ]);

                });
            }
            
            onTick();

        }

        return new Promise(resolve=>{
            resolve(data);
        });

    }

    getComments(username, onTick) {
        return this.getDataRecursive(username, 0, onTick);
    }

    getSubmissions(username, onTick) {
        return this.getDataRecursive(username, 1, onTick);
    }
        
    async getGildings(list_ids){
        var url = `https://api.reddit.com/api/info/?id=${list_ids.join(",")}`;
        var response = await axios.get(url);
        return new Promise(resolve => {
            resolve(response.data.data.children);
        });
    }
    
    async getAnalysis(about, comments, submissions) {
        

        var response;
        var useLocal = Constants.USE_LOCAL_METIS;
        var payload = {
            about: about,
            comments: comments,
            submissions: submissions,
            tz: this.timezone
        };
        
        if (useLocal) {
            var url = Constants.API_URL + "/api/metis_local";
            response = await axios.post(url, {"data":JSON.stringify(payload)});
            response = JSON.parse(JSON.parse(response.data.Payload).body);
        } else {
            var pullParams = {
                FunctionName: Constants.AwsLambda.FUNCTIONNAME,
                InvocationType: Enum.Aws.InvocationType.REQUESTRESPONSE,
                Payload: JSON.stringify({ "body": JSON.stringify(payload) })
            };
            response = (await LambdaClient.invoke(pullParams).promise()).Payload;
            response = JSON.parse(JSON.parse(response).body);
        }
        
        var decoded = JSON.parse(this.decode(response["b"]));
        return new Promise(resolve=>resolve({decoded, response}));
    }

    async getRandomComment(){
        var url = Constants.API_URL+"/api/randomcomment";
        var response = await axios.get(url,{
            crossDomain: true
        });
        return new Promise(resolve=>resolve(response.data.data.children[0].data.body));
    }

    async getTopics(){
        var url = Constants.API_URL+"/api/subdata/topics";
        var response;
        try {
            response = await axios.get(url,{
                crossDomain: true
            });
        } catch (e) {
            response = {success:false, error:"An error has occured while submitting the data. Please try again later."};
        }
        return new Promise(resolve=>{
            resolve(response);
        });
    }

    async getRandomSubredditSuggestions() {
        var url = Constants.API_URL+"/api/subdata/getrandom";
        var response;
        try {
            response = await axios.get(url,{
                crossDomain: true
            });
        } catch (e) {
            response = {success:false, error:"An error has occured while submitting the data. Please try again later."};
        }
        return new Promise(resolve=>{
            resolve(response);
        });
    }
  
    /**
     * submitSubredditCategorization
     * @param data 
     * @param data.subreddit : string - subreddit name without 'r/' prefix
     * @param data.topic_id : integer - topic_id in the database
     */
    async submitSubredditCategorization(data) {
        var url = Constants.API_URL+"/api/subdata/submitcategorization";
        var res;
        try {
            res = await axios.post(url, data);
        } catch (e) {
            res = {success:false, error:"An error has occured while submitting the data. Please try again later."};
        }
        return new Promise(resolve=>{
            resolve(res);
        });
    }

    
    /**
     * check
     * Check if a user's analysis results exists in cache.
     * @param username string:
     */
    async check(username) {
        var url = Constants.API_URL+`/api/check/${username}`;
        var isExists = await axios.get(url);
        return new Promise(resolve=>{
            resolve(isExists.data);
        });    
    }

    // Load the cached results
    async load(username) {
        var url = `/api/load/${username}`;
        var data = await axios.get(url);
        return new Promise(resolve=>{
            resolve(data.data);
        });
    }

    // save the results to cache
    save(savePayload) {
        var url = Constants.API_URL+"/api/save";
        return axios.post(url, savePayload);
    }

    
    encode(data) {
        return btoa(
            pako.deflate(JSON.stringify(data), {
                to: "string",
                gzip: !0
            })
        );
    }
    
    decode (s) {

        // If s is an object (from AWS lambda), set s to the string content
        
    
        // Construct a uInt8Array from the string
        var i_uint8array = Uint8Array.from( 
            atob(s),
            c => c.charCodeAt(0)
        );
    
        // Decompress the string
        var jsonstr = pako.inflate(i_uint8array, { 
            to: "string" 
        });
    
        
        return jsonstr;
    
    }


    submitImproveData(text, emotion) {
        var url = Constants.API_URL+"/improve_data/sentiment";
        return axios.post(url,{
            text,
            emotion
        });
    }


    async getPostFromLink(permalink) {
        var url = `${permalink}.json`;
        var data = await axios.get(url);
        return new Promise(resolve=>{
            resolve(data.data);
        });
    }

}

