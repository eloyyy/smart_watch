var chart1;
var chart2;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {

            var series1 = chart1.series[0],
                shift1 = series1.data.length > 20;

            var series2 = chart2.series[0],
                shift2 = series2.data.length > 20; 

            var series3 = chart3.series[0],
                shift3 = series3.data.length > 20; 

            // add the point
            chart1.series[0].addPoint(point[0], true, shift1);
            chart2.series[0].addPoint(point[1], true, shift2);
            chart3.series[0].addPoint(point[2], true, shift3);

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart1 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container1',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live data X axis accelerometer'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'X acceleration',
            data: []
        }]
    });

    chart2 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container2',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live data Y axis accelerometer'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Y acceleration',
            data: [],
            color: 'red'
        }]
    });

    chart3 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container3',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live data Z axis accelerometer'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Z acceleration',
            data: [],
            color: 'green'
        }]
    });

});