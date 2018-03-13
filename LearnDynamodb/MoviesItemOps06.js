var AWS = require("aws-sdk");
AWS.config.update({
    region: "us-west-2",
    endpoint: "http://localhost:8000"
});

var docClient = new AWS.DynamoDB.DocumentClient();

var table = "Movies";

var year = 2015;
var title = "The Big New Movie";

var params = {
    TableName: table,
    Key:{
        "year": year,
        "title": title
    },
    ConditionExpression: "info.rating <= :val",
    ExpressionAttributeValues:{
        ":val": 50.0
    }
};

console.log("Attemptin a conditional delete...");
docClient.delete(params, function(err, data){
    if(err){
        console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
    }else{
        console.log("DeleteItem succeeded:", JSON.stringify(data, null, 2));
    }
});
