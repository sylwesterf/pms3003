function sortTable() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("myTable");
  switching = true;
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      // Check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        // If so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

var credentials = new AWS.Credentials({
  accessKeyId: 'xyz', secretAccessKey: 'xyz'
});
AWS.config.credentials = credentials;

var dynamodb = new AWS.DynamoDB.DocumentClient({region: 'eu-central-1'});

var params = {
 TableName: 'pms3003',
 Limit: 100,
};

dynamodb.scan(params, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else{
    document.write("<table id=\"myTable\" style=\"width:100%\" class=\"pure-table\">\n");
    document.write("<tr><th onclick=\"sortTable(0)\">Date</th><th>pm2.5</th><th>pm10</th></tr>");
    data.Items.forEach(function(item) {
        document.write("<tr><td>", item.dt, '</td><td>', item.pm25,'</td><td>',item.pm10, '</td></tr>');                    
    });
    document.write("</table>");                    
    }
});
