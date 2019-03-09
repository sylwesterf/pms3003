var credentials = new AWS.Credentials({
  accessKeyId: 'xyz', secretAccessKey: 'xyz'
});
AWS.config.credentials = credentials;

var dynamodb = new AWS.DynamoDB.DocumentClient({region: 'eu-central-1'});

var params = {
 TableName: 'pms3003js',
 Limit: 100,
};
/*
dynamodb.scan(params, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else{
    document.write("<table style=\"width:30%\">\n");
    document.write("<tr><th>Date</th><th>pm1</th><th>pm2.5</th><th>pm10</th></tr>");
    data.Items.forEach(function(item) {
        document.write("<tr><td>", item.dt, '</td><td>', item.pm1,'</td><td>', item.pm25,'</td><td>',item.pm10, '</td></tr>');                    
    });
    document.write("</table>");                    
    }
});
*/
dynamodb.scan(params, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else{
	var eventDateTime = [];
	var eventpm10 = [];
	var eventpm25 = [];
	var eventpm1 = [];
	data.Items.forEach(function(item) {
		eventDateTime.push(item.dt);
		eventpm10.push(item.pm10);
		eventpm25.push(item.pm25);
		eventpm1.push(item.pm1);
});

//Chart.js code
var lineChartData = {
    labels : eventDateTime,
    datasets : [
    {
        label: "pm10",
        fillColor : "rgba(220,220,220,0.2)",
        strokeColor : "rgba(220,220,220,1)",
        pointColor : "rgbargba(220,220,220,1)",
        pointStrokeColor : "#fff",
        pointHighlightFill : "#fff",
        pointHighlightStroke : "rgba(220,220,220,1)",
        data : eventpm10
     },
	{
        label: "pm2.5",
        fillColor : "rgba(151,187,205,0.2)",
        strokeColor : "rgba(151,187,205,1)",
        pointColor : "rgba(151,187,205,1)",
        pointStrokeColor : "#fff",
        pointHighlightFill : "#fff",
        pointHighlightStroke : "rgba(151,187,205,1)",
        data : eventpm25
     },
	 {
        label: "pm1",
        fillColor : "rgba(200,200,200,0.2)",
        strokeColor : "rgba(200,200,200,1)",
        pointColor : "rgba(200,200,200,1)",
        pointStrokeColor : "#fff",
        pointHighlightFill : "#fff",
        pointHighlightStroke : "rgba(200,200,200,1)",
        data : eventpm1
     },
    ]}

var ctx = document.getElementById("pms3003").getContext("2d");

var myNewChart = new Chart(ctx , {
    type: "line",
    data: lineChartData, 
});
}});
