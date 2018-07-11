<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<meta charset="utf-8"/>
    <script type="text/javascript" src="js/plugins/d3/d3.js"></script>
    <script type="text/javascript" src="js/plugins/jquery/jquery-1.9.1.js"></script>
    <link rel="stylesheet" href="css/demo.css"/>
    <style>
    	.style{color: gray;font-size: 12px;margin-left: 15px;}
    	.msg{color: black;font-size: 12px;}
    </style>
</head>
<div style="border: 1px solid darkgray ;display:none;box-shadow: darkgrey 10px 10px 30px 2px; width: 220px; height: 390px; position: fixed; top: 120px;left: 5px;" class="box" >
	<div style="float: right;" class="remove"><img src="images/delete.jpg" /></div>
	<div style="margin-top: 20px;margin-bottom: 10px;"><span style="color: blue; margin-left: 15px;">|&nbsp;</span><span style="font-size: 12px;color: gray;">公 司 信 息</span>
	</div>
	<div id="company_name" style="color: blue; margin-left: 15px;font-size: 13px;border: 0px;"></div><br />
	<span class="style">法定代表人：</span>&nbsp;<span id="legal_man" style="font-size:12px ;color: blue;"></span><br /><br />
	<span class="style">成立日期：</span><span id="date" class="msg"></span><br /><br />
	<span class="style">注册资金：</span><span id="money" class="msg"></span><br /><br />
	<span class="style">地  &nbsp; 址：</span><br/><div id="address"  class="msg" style="margin-left: 12px;border: 0px"></div>
	
</div>
<body>
<script type="text/javascript">

    //D3.js force力导向图用指定的字段确定link的source和target，默认是索引(node索引)，也可以手动指定
	var nodes = ${zifuchuan1};
		 
	var edges = ${zifuchuan2};
	_this = this;
	highlighted=null;
	var width = 1280;
	var height = 1800;
	var color = d3.scale.category20();
	
	//构造数据
	var force = d3.layout.force()
	     .nodes(nodes)
	     .links(edges)
	     .size([width,height])
	     .linkDistance(150)
	     .charge([-400]);
	force.start();
	console.log(nodes);//可以控制台参考数据已经发生变化
	console.log(edges);
	
	//绘图区
	var svg = d3.select("body")
	     .append("svg")
		 .attr("width",width)
		 .attr("height",height);
	//连线
	var svg_edges = svg.selectAll("line")//选择所有连线line元素，下面的append就是生成元素
	     .data(edges)
	     .enter()
	     .append("line")
	     .style("stroke","#ccc")
	     .style("stroke-width",1);
	//连线文字
	var line_text = svg.selectAll(".linetext")
	     .data(edges)
	     .enter()
	     .append("text")
	     .attr("class", "linetext")
	     .attr("x", function(d){ return (d.source.x + d.target.x) / 2})  //dx- x 轴方向的文本平移量   dy- y 轴方向的文本平移量
		 .attr("y", function(d){ return (d.source.y + d.target.y) / 2})
		 .text(function(d){
			 return d.relation;
		  })
		 .attr('fill',function(d,i){
              return _this.color(i);
          })
         .call(this.force.drag);
	//节点
	var svg_nodes = svg.selectAll("circle")
         .data(nodes)
         .enter()
         .append("circle")
         .attr("class", "self")
         .attr("r",20)
         .style("fill",function(d,i){
				return _this.color(i);
			})
		 .call(force.drag)	//使得节点能够拖动
		 .on('mouseover', function(d) {
	             /*if (_this.svg_nodes.mouseoutTimeout) {
	                 clearTimeout(_this.svg_nodes.mouseoutTimeout);
	                 _this.svg_nodes.mouseoutTimeout = null;
	             }*/
	             _this.highlightObject(d); //对选中的节点及关联点设置高亮
	     })
	     .on('mouseout', function() {
	             if (_this.svg_nodes.mouseoutTimeout) {
	                 clearTimeout(_this.svg_nodes.mouseoutTimeout);
	                 _this.svg_nodes.mouseoutTimeout = null;
	             }
	         _this.mouseoutTimeout=setTimeout(function() {
	                 _this.highlightObject(null);
	             }, 300);
	     })
	     .on("click", function (d, i) {
	     	if(d.name.length<4){$(".box").fadeOut()}
	     	else{
	     	$(".box").slideDown("slow");
	     	$("#company_name").html(d.name);
	     	$("#legal_man").html(d.legal_man);
	     	$("#date").html(d.establishment_date);
	     	$("#money").html(d.registered_capital+" 万人民币");
	     	$("#address").html(d.company_address);
	     	}
	    	  //updateNode(d);
	    	//$(".box").show();
	    	 // b.css("font-size","12px");
	    	 // svg.select("box").style("display":"block");
         });
	
    //节点文字
    var node_texts = svg.selectAll(".nodetext")
         .data(nodes)
         .enter()
         .append("text")
         .attr("class", "nodetext")
         .style("fill", "black")
		 .attr("dx", 20)  //dx- x 轴方向的文本平移量   dy- y 轴方向的文本平移量
		 .attr("dy", 8)
		 .text(function(d,i){
			 if (i==0)
			 {
				 return ""+ d.name;
			 }
			 return d.name;
		  });
	//tick事件，力导向图布局 force 有一个事件 tick，每进行到一个时刻，都要调用它，更新的内容就写在它的监听器里就好。
	force.on("tick", function(){
		//节点调整
		svg_nodes.attr("cx", function(d){return d.x;})
		         .attr("cy", function(d){return d.y;});
		//节点文字调整
		node_texts.attr("x", function(d){return d.x;})
                 .attr("y", function(d){return d.y;});
		//连线位置调整
		svg_edges.attr("x1", function(d){return d.source.x;})
		         .attr("y1", function(d){return d.source.y;})
		         .attr("x2", function(d){return d.target.x;})
		         .attr("y2", function(d){return d.target.y;});
		//连线关系调整
		line_text.attr("x", function(d){ return (d.source.x + d.target.x) / 2})
                 .attr("y", function(d){ return (d.source.y + d.target.y) / 2});
	})
	
	//更新节点
	var updateNode = function(item){
		debugger;
		name = item.name + Math.ceil(Math.random() * 5);
		nodes.push({'name': name});
		edges.push({'source': item.index, 'target': nodes.length - 1, relation:"east"});
		force.start();
		
		//绘图
		svg_edges = svg_edges.data(edges);
		svg_edges.enter()
			     .append("line")
			     .style("stroke","#ccc")
			     .style("stroke-width",1);
		//连线文字
		line_text = line_text.data(edges);
		line_text.enter()
		     .append("text")
		     .attr("class", "linetext")
	         .attr("x", function(d){ return (d.source.x + d.target.x) / 2})  //dx- x 轴方向的文本平移量   dy- y 轴方向的文本平移量
		     .attr("y", function(d){ return (d.source.y + d.target.y) / 2})
		     .text(function(d){
			     return d.relation;
		      })
		     .attr('fill',function(d,i){
                  return _this.color(i);
              })
             .call(this.force.drag);
		svg_edges.data(edges).exit().remove();
		
		//节点
		svg_nodes = svg_nodes.data(nodes);
	    svg_nodes.enter()
	         .append("circle")
	         .attr("r",20)
	         .style("fill",function(d,i){
					return _this.color(i);
				})
			 .call(force.drag)	//使得节点能够拖动
			 .on('mouseover', function(d) {
		             if (_this.svg_nodes.mouseoutTimeout) {
		                 clearTimeout(_this.svg_nodes.mouseoutTimeout);
		                 _this.svg_nodes.mouseoutTimeout = null;
		             }
		             _this.highlightObject(d); //对选中的节点及关联点设置高亮
		     })
		     .on('mouseout', function() {
		             if (_this.svg_nodes.mouseoutTimeout) {
		                 clearTimeout(_this.svg_nodes.mouseoutTimeout);
		                 _this.svg_nodes.mouseoutTimeout = null;
		             }
		         _this.svg_nodes.mouseoutTimeout=setTimeout(function() {
		                 _this.highlightObject(null);
		             }, 300);
		     })
		     .on("dblclick", function (d, i) {
	    	     updateNode(d);
             });
		
	    //节点文字
	    node_texts = node_texts.data(nodes);
	    node_texts.enter()
	         .append("text")
	         .attr("class", "nodetext")
	         .style("fill", "black")
			 .attr("dx", 20)  //dx- x 轴方向的文本平移量   dy- y 轴方向的文本平移量
			 .attr("dy", 8)
			 .text(function(d,i){
				 if (i==0)
				 {
					 return "原点-"+ d.name;
				 }
				 return d.name;
			  });
	    svg_nodes.data(nodes).exit().remove();
	}
	
	
	this.highlightObject=function(obj){
          if (obj) {
              if (obj !== highlighted) {
                  var objIndex= obj.index;
                  var depends=[objIndex];
                  edges.forEach(function(lkItem){
                      if(objIndex==lkItem['source']['index']){
                          depends=depends.concat([lkItem.target.index])
                      }else if(objIndex==lkItem['target']['index']){
                          depends=depends.concat([lkItem.source.index])
                      }
                  });
                  //classed("active",true)用法
                 // node_texts.classed("font",true);
                // obj.siblings().hide();
                //_this.node_texts.classed("te",true)
                _this.node_texts.classed('te',function(d){
                     return (depends.indexOf(d.index)==-1)
                 });
                 
                  _this.svg_nodes.classed('selfs',function(d){
                          return (depends.indexOf(d.index)==-1)
                  });
                  _this.svg_edges.classed('line', function(d) {
                      return (obj !== d.source && obj !== d.target);
                  });
                  _this.line_text.classed('inactive',function(d){
                      return (d.source.index !=obj.index && d.target.index!=obj.index)
                  });
              }
              highlighted = obj;
          } else {
              if (highlighted) {
                  _this.svg_nodes.classed('selfs', false);
                  _this.svg_edges.classed('line', false);
                  _this.line_text.classed('inactive', false);
                  _this.node_texts.classed('te', false);
              }
              highlighted = null;
          }
      };
		$(".remove").on("click",function(){
			$(".box").hide();
		})
</script>
</body>
</html>