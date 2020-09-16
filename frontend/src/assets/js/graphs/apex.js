// Apex.js
// code for the graphs generated using apexcharts
import ApexCharts from "apexcharts";
import Constants from "@/assets/js/config/Constants.js";

var HOUR_SERIES = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"];
var WEEKDAY_SERIES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
var categories = [];


function number_formatter(val) {
    var v = val.toString();
    var isNegative = v.startsWith("-");
    var ret = "";
    if (isNegative) {
        v = v.substring(1);
        ret = "-";
    }
    if (val>=1000 && val<=999999){
        return ret + parseFloat(val/1000).toFixed(1)+"k";
    } else if (val>=1000000){
        return ret + parseFloat(val/1000000).toFixed(1)+"M";
    }
    return Math.round(val);
}

var chart_gray = {
    color: "#808080",
    fontFamily: "'Nunito'"
};




function generateSubmissionByHourGraph(histogram) {
    var options = {
        legend: {
            position:"top",
            horizontalAlign:"center"
        },
        chart: {
            height: 250,
            type: "bar",
            toolbar:{
                show:false,
            }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "100%",
                endingShape: "rounded"	
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ["transparent"]
        },
        series: [{
            name: "Posts",
            data: histogram.hour.posts
        }, {
            name: "Karma",
            data: histogram.hour.karma
        }],
        xaxis: {
            style:{
                fontSize:"5px",
                color: "#808080",
                fontFamily: "'Nunito'"
            },
            fontFamily: "'Nunito'",
            categories: HOUR_SERIES,
            tickAmount : 8
        },
        fill: {
            opacity: 1
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val;
                }
            }
        },
        colors: [Constants.Color.BLUE, Constants.Color.GREEN],
        yaxis: [
            {
                axisTicks: {
                    show: true
                },
            
                axisBorder: {
                    show: true,
                    color: "#808080"
                },
                labels: {
                    style: chart_gray,
                    formatter: number_formatter
                },
                title: {
                    text: "Posts",
                    style:chart_gray
                }
            },
            {
                opposite: true,
                axisTicks: {
                    show: true
                },
                fontFamily: "'Nunito'",
                axisBorder: {
                    show: true,
                    color: "#808080"
                },
                labels: {
                    style: chart_gray,
                    formatter: number_formatter
                },
                title: {
                    text: "Karma",
                    style: chart_gray
                }
            }
        ],
    };

    var chart = new ApexCharts(
        document.querySelector("#submisison_by_hour"),
        options
    );
    chart.render();
}

function generateSubmissionByWeekdayGraph(histogram) {
    var options = {
        legend: {
            position:"top",
            horizontalAlign:"center"
        },
        chart: {
            height: 225,
            type: "bar",
            toolbar:{
                show:false,
            }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "55%",
                endingShape: "rounded"	
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ["transparent"]
        },
        series: [{
            name: "Posts",
            data: histogram.day.posts
        }, {
            name: "Karma",
            data: histogram.day.karma
        }],
        xaxis: {
            categories: WEEKDAY_SERIES,
            color: "#808080",
            fontFamily: "'Nunito'"
        },
        fill: {
            opacity: 1
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val;
                }
            }
        },
        colors: [Constants.Color.BLUE, Constants.Color.GREEN],
        yaxis: [
            {
                axisTicks: {
                    show: true
                },
                fontFamily: "'Nunito'",
                axisBorder: {
                    show: true,
                    color: "#808080"
                },
                labels: {
                    style: {
                        color: "#808080"
                    },
                    formatter: number_formatter
                },
                title: {
                    text: "Posts",
                    style:{
                        fontFamily: "'Nunito'",
                        color: "#808080"
                    },
            
                }
            },
            {
                opposite: true,
                axisTicks: {
                    show: true
                },
                axisBorder: {
                    show: true,
                    color: "#808080"
                },
                labels: {
                    style: {
                        fontFamily: "'Nunito'",
                        color: "#808080"
                    }
                },
                title: {
                    text: "Karma",
                    style:chart_gray
                }
            }
        ],
    };

    var chart = new ApexCharts(
        document.querySelector("#submission_by_weekday"),
        options
    );

    chart.render();
}
  

async function generateKarmaGraph(PKOverTime) {
    var karma_graph_options = {
        legend: {
            position:"top",
            horizontalAlign:"center"
        },
        chart: {
            height: 225,
            type: "line",
            stacked: false,
            toolbar:{
                show:false,
            }
        },
        dataLabels: {
            enabled: false
        },
        colors: [Constants.Color.BLUE, Constants.Color.GREEN],
        series: [
            {
                name: "Posts"
            },
            {
                name: "Karma"
            }
        ],
        stroke: {
            width: [4, 4]
        },
        plotOptions: {
            bar: {
                columnWidth: "20%"
            }
        },
        xaxis: {
            categories: categories,
            hideOverlappingLabels:true,
            labels:{
                show:false
            },
            style: {
            
                color: "#808080",
                fontFamily: "'Nunito'"
            }
        },
        yaxis: [
            {
                title: {
                    text: "Posts"
                },
                labels: {
                    formatter: number_formatter
                },
            },
            {
                opposite: true,
                title: {
                    text: "Karma"
                },
                labels: {
                    formatter: number_formatter
                }
            }
        ],
        tooltip: {
            intersect: false,
            x: {
                show: false
            }
        },
        
        fontFamily: "'Nunito'",
    };

    var keys = Object.keys(PKOverTime["posts"]).reverse();
    karma_graph_options.xaxis.categories = keys;
    var karma_graph_data = {
        standard:{posts:keys.map(s => PKOverTime["posts"][s]), karma:keys.map(s => PKOverTime["karma"][s])},
        cumulative:{posts:[], karma:[]},
    };
    var tmparray = Object.keys(PKOverTime["posts"]).reverse().map(
        s=>PKOverTime["posts"][s]
    );
    tmparray.reduce(function(a,b,i) { return karma_graph_data.cumulative.posts[i] = a+b; },0);

    tmparray = Object.keys(PKOverTime["karma"]).reverse().map(
        s=>PKOverTime["karma"][s]
    );
    tmparray.reduce(function(a,b,i) { return karma_graph_data.cumulative.karma[i] = a+b; },0);
    karma_graph_options.series[0]["data"] = karma_graph_data.cumulative.posts;
    karma_graph_options.series[1]["data"] = karma_graph_data.cumulative.karma;
    // karma_canvas_notcumu
    var chart_karma = new ApexCharts(document.querySelector("#karma_canvas_cumu"), karma_graph_options);
    await chart_karma.render(); // return promise if done

    karma_graph_options.series[0]["data"] = karma_graph_data.standard.posts;
    karma_graph_options.series[1]["data"] = karma_graph_data.standard.karma;
    var chart_karmac = new ApexCharts(document.querySelector("#karma_canvas_notcumu"), karma_graph_options);
    await chart_karmac.render(); 
}

export default {
    generateSubmissionByHourGraph,
    generateKarmaGraph,
    generateSubmissionByWeekdayGraph
};