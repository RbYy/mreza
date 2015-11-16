
$('#colorselector').colorselector();
var x=parseInt($('#mre').val().split('x')[0]);
var y=parseInt($('#mre').val().split('x')[1]);
var ime_mreze=$('#ime_mreze').val();

function povleciSeznamMrez(){
    $.getJSON('/povleci_mreze/', {}, function(data){
        for (i=1; i<data.length+1; i++){
            console.log(data[i-1]['fields']['datum']);
        }
        console.log(data);
    });
}
function ustvariMrezo(){    
    console.log(x,y);
    $.get('/ustvari_mrezo/',{
                            'sirina':x,
                            'visina':y,
                            'ime_mreze':ime_mreze},
                            function(data){
                                console.log('uspeh')
                            })
}

function izrisiMrezo(sirina,visina){
    for (var i=1; i<=visina; i++){
        $('.t').append("<tr id=vrsta_" + i + "></tr>");
        for (var j=1; j<=sirina; j++){
            $('#vrsta_'+ i).append('<td id=' + j + '_' + i +'></td>');
        }
    }
}

povleciSeznamMrez();
izrisiMrezo(sirina_default, visina_default);
    
$('#desno').on('click', '#dimenzije',function(){
    $('tr').remove();
    ustvariMrezo();
    izrisiMrezo(x,y);
});


var count=0;  
$('#desno').on('click', '#novbat',function(){
    count+=1;
    var barva=$(".btn-colorselector").css("background-color");
    $('table').append('<div class="lik" id="lik'+ count+'"><p name="'+count+'" id ="zapri">X</p><p class="naslov"></p></div>');
    var xx=parseInt($('#velikost').val().split('x')[0]);
    var yy=parseInt($('#velikost').val().split('x')[1]);
    var ime=$('#ime').val();
    var vrsta = 'vrsta'; /*to je za popravit -- drfault vrednost*/
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
                offx=ui.offset['left'];
                offy=ui.offset['top'];
                $.get('/shrani/',  {'offx': offx,
                                    'offy': offy,
                                    'visina': yy,
                                    'sirina': xx,
                                    'barva': barva,
                                    'ime': ime,
                                    'vrsta': vrsta}, function(data){ 
                });
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
