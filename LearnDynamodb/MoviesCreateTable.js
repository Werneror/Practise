var AWS = require('aws-sdk');
AWS.config.update({
    region: "us-west-2",
    endpoint: "http://127.0.0.1:8000"
});

var dynamodb = new AWS.DynamoDB();
var params = {
    TableName: "Movies",
    KeySchema: [
        {AttributeName: "year", KeyType: "HASH"},
        {AttributeName: "title", KeyType: "RANGE"}
    ],
    AttributeDefinitions: [
        {AttributeName: "year", AttributeType: "N"},
        {AttributeName: "title", AttributeType: "S"}
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 10,
        WriteCapacityUnits: 10
    }
};

dynamodb.createTable(params, function(err, data){
    if(err){
        console.error("Unable to create table. Error JSON:", JSON.stringify(err, null, 2));
    }else{
        console.log("Create table. Table description JSON:", JSON.stringify(data, null, 2));
    }
});
