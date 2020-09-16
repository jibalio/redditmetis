import * as d3 from "d3";

import d3tip from "d3-tip";

export default {
    generate(a) {
        /*var colorDomain = d3.extent(a, function(d){
            return d.value;
        });*/
        
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
                                  >${d.tooltip_display}</p>
                              </div>
                          </div>
                          <p style="font-size: 0.7em;">${d.original} posts/submissions</p>
                      </div>
                  </div>`; 
        });
        var colorScale = d3.scaleLinear()
            .range(["#f9f9f9","#ffe984", "#ffb923"])
            .domain([0,1,15]);
        var svg = d3.select(".heatmap")
        
            .append("div")
            .classed("svg-container", true)
            .append("svg");
        //responsive SVG needs these 2 attributes and no width and height attr
          
  
        /*var tooltip = d3.select(".heatmap")
          .append("div")
          .style("opacity", 0)
          .attr("class", "tooltip")
          .style("background-color", "white")
          .style("border", "solid")
          .style("border-width", "2px")
          .style("border-radius", "5px")
          .style("padding", "5px")
          .attr("preserveAspectRatio", "xMinYMin meet")
        
  
        // Three function that change the tooltip when user hover / move / leave a cell
        /var mouseover = function() {
          tooltip.style("opacity", 1)
        }

        var svg_width = document.getElementsByClassName("svg-container")[0].style.width;
        var mousemove = function(d) {
          //
          tooltip
            .html(d.tooltip_display)
            .style("left", (d3.mouse(this)[0]*1.85)*(svg_width/1088) + "px")
            .style("top", ((d3.mouse(this)[1]*1.85))*(svg_width/1088)+100 + "px")
  
        }
        var mouseleave = function() {
          tooltip.style("opacity", 0)
        }*/
  
  
        
        
  
        var rectangles = svg
            .selectAll("rect")
            .data(a)
            .enter()
            .append("rect");
          
          
  
        rectangles
            .attr("x", function(d){
                return d.x * 9; 
            })
  
            .attr("value", function(d){
                return d.value;
            })
          
            .attr("y", function(d){
                return d.y * 9; 
            })
            .attr("width", 9)
            .attr("height", 9)
            .style("fill", function(d){
                return colorScale(d.value); 
            }
            )
            .attr("transform", "translate(32,0)")
            .attr("margin","0.5");
        // I commented 7 times on 5pm UTC!
  
        var time_yaxis = [
            "12MN","01A","02A","03A","04A","05A","06A","07A","08A","09A",
            "10A","11A","12NN","01P","02P","03P","04P","05P","06P","07P",
            "08P","09P","10P","11P"
        ];  
        // Add scale band
        var y = d3.scaleBand()
            .range([ 0, 215 ])
            .domain(time_yaxis)
            .padding(0.01);
        svg.append("g")
            .attr("transform","translate(40,0)")
            .attr("class","axis")
            .call(d3.axisLeft(y));
  
          
  
        svg.attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0 600 400")
        
        //class to make it responsive
            .classed("svg-content-responsive", true)
            .call(tip); //habsdygasdbhds
  
        
        
        svg.selectAll("text")
            .style("font-size","7px") //To change the font size of texts
            .style("color","#808080")
            .attr("font-family","sans-serif"); //To change the font size of texts
  
        svg.selectAll("line")
            .style("color","#808080");
  
        svg.selectAll("path.domain")
            .remove();
  
        svg.selectAll("line")
            .remove();

          
          

        
        setTimeout(function(){ 
            svg
                .call(tip);
            svg.selectAll("rect")//2s
                .on("mouseover", tip.show)
                .on("mouseout", tip.hide);
        }, 500);
        
    }
};