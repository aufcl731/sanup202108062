$(document).ready(function(){
  
  var i=0;
    
  $('.circle-chart').each(function(){
    var id = 'chart' + i;
    $(this).attr('id',id);
    drawCircleChart('#'+id);
    i++;
  })
  
  $('.circle-chart').click(function(){
    var thisId = $(this).attr('id');
    drawCircleChart('#'+thisId);
  })
  
  function drawCircleChart(id){
    $(id).empty().append("<p>" + $(id).data('percent') + "%</p>");
    addOneBar(id);
  }
  
  function addOneBar(id){
    var percent = $(id).data('percent');
    var noOfBars = .36*percent;
    if( $(id).children().length-1 < noOfBars ){
      $(id).append('<div class="bar"></div>');
        setTimeout(function() { addOneBar(id); },30);
    }
  }
  
})