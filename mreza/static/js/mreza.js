$('#colorselector').colorselector();
    var x=parseInt($('#mre').val().split('x')[0]);
    var y=parseInt($('#mre').val().split('x')[1]);
    console.log(x,y);
    
    
    for (var i=1; i<y; i++){
        $('.t').append("<tr id=vrsta_" + i + "></tr>");
        for (var j=1; j<x; j++){
            $('#vrsta_'+ i).append('<td id=' + j + '_' + i +'></td>');
        }
    }
    
$('#desno').on('click', '#dimenzije',function(){
    $('tr').remove();
    var x=parseInt($('#mre').val().split('x')[0]);
    var y=parseInt($('#mre').val().split('x')[1]);
    console.log(x,y);
    
    
    for (var i=1; i<y; i++){
        $('.t').append("<tr id=vrsta_" + i + "></tr>");
        for (var j=1; j<x; j++){
            $('#vrsta_'+ i).append('<td id=' + j + '_' + i +'></td>');
        }
    }
});
var count=0;  
$('#desno').on('click', '#novbat',function(){
count+=1;
var barva=$(".btn-colorselector").css("background-color");
 $('table').append('<div class="lik" id="lik'+ count+'"><p name="'+count+'" id ="zapri">X</p><p class="naslov"></p></div>');
   var xx=parseInt($('#velikost').val().split('x')[0]);
   var yy=parseInt($('#velikost').val().split('x')[1]);
   var ime=$('#ime').val();
   console.log(count);
   $('.lik').on('click', '#zapri', function(){
        id=$(this).attr("name");
        $("#lik"+id).remove();
        console.log(id);
    });
  $(function() {
    $( ".lik" ).draggable({
        snap:'true',
        snap: 'td',
        snapMode:"both",
        snapTolerance: 20 
    });
    $( ".lik" ).draggable({
        stop: function( event, ui ) {
            console.log(ui.offset);
        }
});
  });
    $('#lik'+count).css({
                    "position": "absolute",
                    "background-color": barva, 
                    "opacity": 0.7,
                    "left": x*30,
                    "top": 300,
                    "width":xx*25, 
                    "height":yy*25} 
                    );
    $(".naslov").text(ime);
    var offset=$('#lik'+count).offset();
    console.log(offset);

});

  console.log('dsf')
