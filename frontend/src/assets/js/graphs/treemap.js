import * as d3 from "d3";
import Utils from "@/assets/js/utils.js";
import d3tip from "d3-tip";
var width = 500;
var height = width*0.4;

var format = d3.format(",d");


var name = d => d.ancestors().reverse().map(d => d.data.name).join("/");


var treemap = (data, mode) => d3.treemap()
    .tile(tile)(
        d3.hierarchy(data)
            .sum(d => d[mode])
            .sort((a, b) => b[mode] - a[mode]
            )
    );

function tile(node, x0, y0, x1, y1) {
    d3.treemapBinary(node, 0, 0, width, height);
    for (const child of node.children) {
        child.x0 = x0 + child.x0 / width * (x1 - x0);
        child.x1 = x0 + child.x1 / width * (x1 - x0);
        child.y0 = y0 + child.y0 / height * (y1 - y0);
        child.y1 = y0 + child.y1 / height * (y1 - y0);
    }
}




function chart (data, mode) {
    const removeElements = (elms) => elms.forEach(el => el.remove());

    // Use like:
    removeElements( document.querySelectorAll(".d3-tip") );
    function addRecursive (node) {
        var totalposts = 0;	
        if (node.data[mode]) {
            
            return node.data[mode];
        } else if (node.children) {
            node.children.forEach(function(x) {
                totalposts+=addRecursive(x);
            });
            
            return totalposts;
        } else {
            return totalposts;
        }
        
    }

    document.getElementById("data-posts_by_subreddit").innerHTML = "";
    // mode is "karma" or "posts"
    var colors = [
        {
            color: "#8ddae7",
            subhues: ["#98dee9","#a4e1ec","#afe5ee","#bbe9f1"]
        },
        {
            color: "#86f2be",
            subhues: ["#92f3c5","#9ef5cb","#aaf6d2","#b6f7d8"]
        },
        {
            color: "#e7c28d",
            subhues: ["#e9c898","#eccea4","#eed4af","#f1dabb"]
        },
        {
            color: "#e78d9c",
            subhues: ["#e998a6","#eca4b0","#eeafba","#f1bbc4"]
        },
        {
            color: "#e68e8e",
            subhues: ["#e99999","#eba5a5","#eeb0b0","#f0bbbb"]
        },
        {
            color: "#9ee68e",
            subhues: ["#a8e999","#b1eba5","#b1eba5","#c5f0bb"]
        },
        {
            color: "#e8b7e6",
            subhues: ["#eabee9","#edc5eb","#efcdee","#f1d4f0"]
        },
    ];
    var categoryDict = {};
    var i = 0;
    var catColor = node => {
        if (node.depth===0) {
            return "#eee";
        } else if (node.depth === 1) {
            if (!categoryDict[node.data.name]) {
                categoryDict[node.data.name] = colors[i%colors.length];
                i++;
            }
            return categoryDict[node.data.name]["color"];
        } else {
            var subhues = categoryDict[node.parent.data.name].subhues;
            return subhues[Math.floor(Math.random() * subhues.length)];
        }
    };

    // mode is either 'posts' or 'num'
    
    const x = d3.scaleLinear().rangeRound([0, width]);
    const y = d3.scaleLinear().rangeRound([0, height]);
  
    
    var tip = d3tip().attr("class", "d3-tip").html(function(d) { 
        
        
        
        
        return `<div class="row">
                    <div class="col mpanel round-edge" style="padding-bottom: 0.2rem;">
                        <div class="mpanel-header row" style="padding-right:3rem;">
                            <div class="col d-flex justify-content-start">
                                <p style="color: #000000;
                                    font-size: 0.7em;
                                    font-weight: 400;
                                    font-variant: none  ;
                                    text-transform: none;"
                                >${d.data.name}</p>
                            </div>
                        </div>
                        <p style="font-size: 0.7em;">${Utils.formatNumber(addRecursive(d))} ${mode}</p>
                    </div>
                </div>`; 
    });

    const svg = d3.select("#data-posts_by_subreddit")
        .append("svg")
        .attr("viewBox", [0.5, -30.5, width, height + 30])
        .style("font", "0.4em 'Nunito'")
        .call(tip);
    
    let group = svg.append("g")
        .call(render, treemap(data,mode));
    
    function render(group, root) {

        
        
        const node = group
            .selectAll("g")
            .data(()=>{
                return root.children.concat(root);
            })
            .join("g");
  
        node.filter(d => d === root ? d.parent : d.children)
            .attr("cursor", "pointer")
            .on("click", d => d === root ? zoomout(root) : zoomin(d));
  
        node.append("title")
            .text(d => `${name(d)}\n${format(d.value)}`);
  
        node.append("rect")
        //.attr("id", d => (d.leafUid = DOM.uid("leaf")).id)
            .attr("fill", d => /*d.name == "dataisbeautiful" ? "#fac3df" :"#ddd"*/ {
                return catColor(d);
            })
            .attr("stroke", "#fff");
          
  
        node.append("clipPath")
        //.attr("id", d => (d.clipUid = DOM.uid("clip")).id)
            .append("use");
        //.attr("xlink:href", d => d.leafUid.href);
        //var kx = width / root.dx;
        //var ky = height / 1;

      

        node.append("text")
            .attr("clip-path", d => d.clipUid)
            .attr("font-weight", d => d === root ? "bold" : null)
            .selectAll("tspan")
            .data(d => (d === root ? name(d) : d.data.name).split(/(?=[A-Z][^A-Z])/g).concat(Utils.formatNumber(
                addRecursive(d)
            ))).join("tspan")
        
            .join("tspan")
            .attr("x", 3)
            .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
            .attr("fill-opacity", (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
            .attr("font-weight", (d, i, nodes) => i === nodes.length - 1 ? "normal" : null)
            .attr("fill", "#484848")
            .text(d => d);    
          

        group.call(position, root);

        node.on("mouseover", tip.show)
            .on("mouseout", tip.hide);

    }
  
    function position(group, root) {
        group.selectAll("g")
            .attr("transform", d => d === root ? "translate(0,-30)" : `translate(${x(d.x0)},${y(d.y0)})`)
            .select("rect")
            .attr("width", d => {
                return d === root ? width : x(d.x1) - x(d.x0);
            })
            .attr("height", d => d === root ? 30 : y(d.y1) - y(d.y0));
    }
  
    

    // When zooming in, draw the new nodes on top, and fade them in.
    function zoomin(d) {
        const group0 = group.attr("pointer-events", "none");
        const group1 = group = svg.append("g").call(render, d);
  
        x.domain([d.x0, d.x1]);
        y.domain([d.y0, d.y1]);
  
        svg.transition()
            .duration(750)
            .call(t => group0.transition(t).remove()
                .call(position, d.parent))
            .call(t => group1.transition(t)
                .attrTween("opacity", () => d3.interpolate(0, 1))
                .call(position, d));
    }
    
    // When zooming out, draw the old nodes on top, and fade them out.
    function zoomout(d) {
        const group0 = group.attr("pointer-events", "none");
        const group1 = group = svg.insert("g", "*").call(render, d.parent);
  
        x.domain([d.parent.x0, d.parent.x1]);
        y.domain([d.parent.y0, d.parent.y1]);
  
        svg.transition()
            .duration(750)
            .call(t => group0.transition(t).remove()
                .attrTween("opacity", () => d3.interpolate(1, 0))
                .call(position, d))
            .call(t => group1.transition(t)
                .call(position, d.parent));
    }
  
    return svg.node();
}





export default {
    chart,
};