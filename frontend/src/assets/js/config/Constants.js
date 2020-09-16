
import moment from "moment-timezone";

const Constants = {

    //API_URL: "http://localhost:5000",   // local
    API_URL: "",                     // production

    USE_LOCAL_METIS: false,
    USE_RESULT_CACHE: true,

    COMMENT: 0,
    SUBMISSION: 1,
    Routes: {
        "CACHE_RESULTS_URL": "/save",
    },
    Timezone: moment.tz.guess(),
    AwsLambda: {
        REGION: "",
        IDENTITYPOOLID: "",
        FUNCTIONNAME: "",
    },
    HEATMAP_DATE_FORMAT: "YYYY-MM-DD HH:00",
    DAY_KEYS: {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
    },
    Color: {
        GRAY: "#808080",
        BLUE: "#76cad9",
        GREEN: "#7ee7b4",
    },
    Error : {
        "InvalidUserError": { error: true, name: "InvalidUserError", message: "The username you entered is invalid." },
        "UserNotFoundError": { error: true, name: "UserNotFoundError", message: "That user does not exist." },
        "ContentBlocked":{error:true, name:"ContentBlocked", message:"Uh oh. Your browser prevents RedditMetis from reaching Reddit.<br /><br /> If you're on Firefox, whitelist RedditMetis by clicking the shield icon left of the URL bar, and reload the page. <br /><br /> Otherwise, whitelist RedditMetis on any content blocking plugins you installed. <br /><br /><a target='_blank' href='https://www.reddit.com/r/RedditMetis/comments/cwnod2/getting_user_not_found_or_no_response_errors/'>Why is this happening?</a>"},
        "BannedUserError": { error: true, name: "BannedUserError", message: "That user has been banned." },
        "NoDataError": { esrror: true, name: "NoDataError", message: "This user has no data to show." },
        "UnexpectedError": { error: true, name: "UnexpectedError", message: "An unexpected error occured. Please PM u/consulnappy on Reddit."},
        "LambdaInvokeError": { error: true, name: "LambdaInvokeError", message: "Connection refused. Please check your system time if it is configured correctly (must not be more than 5 mins. ahead/behind).<br /><br />This is an anti-spam measure.<br /><br />Code: LambdaInvokeError"},
        "NoResponseError": { error: true, name: "NoResponseError", message: "The server did not return a response. It might be the user has no comment/submission history. If you think this is incorrect, it might be a server problem. Please PM u/consulnappy on Reddit.\nCode:NoResponseError" },
        "UnexpectedErrorRetrieve": { error: true, name: "UnexpectedErrorRetrieve", message: "An unexpected error occured while retrieving user info from Reddit." },
        "SaveCacheError": { error: true, name: "SaveCacheError", message: "An error occured while caching the results (SaveCacheError)" }
    }

};

export default Constants;