function drawLineChart() {

  var selectorOptions = {
    buttons: [{
        step: 'hour',
        stepmode: 'backward',
        count: 6,
        label: '6h'
    }, {
        step: 'day',
        stepmode: 'backward',
        count: 1,
        label: '1d'
    }, {
        step: 'day',
        stepmode: 'backward',
        count: 7,
        label: '7d'
    }, {
        step: 'day',
        stepmode: 'backward',
        count: 14,
        label: '2w'
    }, {
        step: 'all',
    }],
  };

  var jsonData = $.ajax({
    url: 'https://cors.io/?https://s3.eu-central-1.amazonaws.com/pms3003/data2.json',
    dataType: 'json',
  }).done(function (results) {

    // Split timestamp and data into separate arrays
	var eventpm1 = [];
	var eventpm25 = [];
    var eventpm10 = [];
	var temp = [];
	var hum = [];
	var eventdt = [];
	var tooltip = [];
    results.forEach(function(item) {
      	eventpm1.push(item.pm1);
		eventpm25.push(item.pm25);
		eventpm10.push(item.pm10);
		temp.push(item.temp);
		hum.push(item.hum);
		eventdt.push(item.dt);
    });

	//tooltip.forEach(function(element) {
	//	tooltip += (" c");
	//	console.log(element + "c");
	//});
	
	var tooltip = temp.map(function(v, i) {
		if (v == null) {
			v = "";
			return v;
		};
		return "temp: " + v + "°C | hum: " + hum[i] + "%";
	});
	//console.log( "tooltip:", tooltip );

    // Create the chart.js data structure using 'labels' and 'data'
    var pm1 = {
	y: eventpm1,
  	x: eventdt,
	name:'pm1',
	visible:'legendonly',
  	mode: 'lines'
    };

    var pm25 = {
	y: eventpm25,
  	x: eventdt,
	name:'pm2.5',
  	mode: 'lines'
    };

    var pm10 = {
	y: eventpm10,
  	x: eventdt,
	name:'pm10',
	text: tooltip,
  	mode: 'lines'
    };

    var data = [pm1,pm25,pm10];

    var layout = {
        xaxis: {
            rangeselector: selectorOptions,
            rangeslider: {}
        },
        yaxis: {
			title: "µg/m3",
            fixedrange: true
        }};

    Plotly.newPlot('pms3003', data, layout);

  });
}

drawLineChart();