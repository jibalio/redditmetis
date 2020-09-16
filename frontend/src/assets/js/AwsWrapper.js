import AWS from "aws-sdk/global";
import Constants from "./config/Constants.js";
import AWSLambda from "aws-sdk/clients/lambda";

AWS.config.region = Constants.AwsLambda.REGION; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: Constants.AwsLambda.IDENTITYPOOLID,
});

var LambdaClient = new AWSLambda({ region: AWS.config.region });

export default LambdaClient;


