var AWS = require("aws-sdk");

AWS.config.update({
    region: "us-west-2",
    endpoint: "http://localhost:8000"
});

var docClient = new AWS.DynamoDB.DocumentClient();

var params = {
    TableName: "Movies",
    ProjectionExpression: "#yr, title, info.rating",
    FilterExpression: "#yr between :start_yr and :end_yr",
    ExpressionAttributeNames:{
        "#yr": "year"
    },
    ExpressionAttributeValues:{
        ":start_yr": 1950,
        ":end_yr": 1959
    }
};

console.log("Scanning Movies table.");
docClient.scan(params, onScan);

function onScan(err, data){
    if(err){
        console.error("Unable to scan the table. Error JSON:", JSON.stringify(err, null, 2));
    }else{
        console.log("Scan succeeded.");
        data.Items.forEach(function(movie){
            console.log(movie.year + ": ", movie.title, "- rating:", movie.info.rating);
        });

        if(typeof data.LastEvaluatedKey != "undefined"){
            console.log("Scanning for more ...");
            params.ExclusivesStartKey = data.LastEvaluatedKey;
            docClient.scan(params, onScan);
        }
    }
}
