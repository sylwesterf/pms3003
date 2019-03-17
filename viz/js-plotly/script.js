function drawLineChart() {

  var jsonData = $.ajax({
    url: 'https://cors.io/?https://s3.eu-central-1.amazonaws.com/pms3003/data.json',
    dataType: 'json',
  }).done(function (results) {

    // Split timestamp and data into separate arrays
	var eventpm1 = [];
	var eventpm25 = [];
    	var eventpm10 = [];
	var eventdt = [];
    results.forEach(function(item) {
      	eventpm1.push(item.pm1);
	eventpm25.push(item.pm25);
	eventpm10.push(item.pm10);
	eventdt.push(item.dt);
    });

    // Create the chart.js data structure using 'labels' and 'data'
    var pm1 = {
	y: eventpm1,
  	x: eventdt,
  	mode: 'lines'
    };

    var pm25 = {
	y: eventpm25,
  	x: eventdt,
  	mode: 'lines'
    };

    var pm10 = {
	y: eventpm10,
  	x: eventdt,
  	mode: 'lines'
    };

    var data = [pm1,pm25,pm10];

    var layout = {};

    Plotly.newPlot('pms3003', data, layout, {showSendToCloud: true});

  });
}

drawLineChart();