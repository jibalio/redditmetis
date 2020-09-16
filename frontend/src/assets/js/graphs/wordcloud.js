import * as d3 from "d3";
import d3cloud from "d3-cloud";

async function generate(data, excludeNumWords) {
    return new Promise((resolve) => {
        var containerWidth = Math.min(430,document.getElementById("word-cloud-container").offsetWidth*0.825);
        renderWordCloud({
            container: "word-cloud",
            width: containerWidth,
            height: containerWidth,
            data: data.slice(excludeNumWords),
            margin: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            }
        });
        resolve(true);
    });
}

// borrowed from u/orionmelt's snoopsnoo code
function renderWordCloud (options) {
    options = options || {};
    //var container = "#"+options.container;
    var data = JSON.parse(JSON.stringify(options.data));
    var width = options.width;
    var height = options.height;
    var margin = options.margin;
    var color = options.color || d3.scaleOrdinal(["#008FFB","#00E396","#FEB019","#FF4560","#775DD0"]);
    
    var docFrag = document.createDocumentFragment();
    
    if (!data.length) {
      
        return;
    }
    var min_count = data[data.length-1].size-1;
    var max_count = data[0].size;

    document.getElementById("word-cloud").innerHTML = "";
    d3cloud().size([width, height])
        .words(data)
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function(d) {
            var size = (60*(d.size-min_count))/(max_count-min_count);
            return size>12 ? size : 12;
        })
        .on("end", draw)
        .start();

    function draw(words) {
        d3.select(docFrag).append("svg")
            .attr("width", width+margin.left+margin.right)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + (width+margin.left+margin.right)/2 +"," + height/2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("fill", function(d, i) { return color(i); })
            .attr("font-family","'Nunito',sans-serif")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });

    }
    document.getElementById(options.container).appendChild(docFrag);
}


export default {
    generate
};