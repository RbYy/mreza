
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
    console.log(x,y,ime_mreze);
    if (ime_mreze !==null && x!==null && y!==null){
        console.log('pravilni vnosi')
        $.get('/ustvari_mrezo/',{
                                'sirina':x,
                                'visina':y,
                                'ime_mreze':ime_mreze},
                                function(data){
                                    console.log('uspeh')
                                })
        }
    else{
        console.log('nepepolni vnosi')
    }
}

function izrisiMrezo(sirina,visina,ime){
    $('.grid').remove();
    $('caption').text(ime);
    for (var i=1; i<=visina; i++){
        $('.t').append("<tr class='grid' id=vrsta_" + i + "></tr>");
        for (var j=1; j<=sirina; j++){
            $('#vrsta_'+ i).append('<td id=' + j + '_' + i +'></td>');
        }
    }
}
function shraniNoveDimenzijeMreze(){
    $.get('/shrani_nove_dimenzije_mreze/',{
                            'sirina':x,
                            'visina':y,},
                            function(data){
                                console.log('shranjeno');
                            });
}
povleciSeznamMrez();
izrisiMrezo(sirina_default, visina_default, ime_default);
    
$('#desno').on('click', '#dimenzije',function(){
    shraniNoveDimenzijeMreze()
    $('tr').remove();
    izrisiMrezo(x,y);
});
$('#desno').on('click', '#shrani',function(){
    ustvariMrezo();
});

$('.seznam_mrez').on('click','.mreza_v_seznamu', function(event){
    pk=event.target.id.split('_')[1];
    $.getJSON('/aktiviraj_drugo_mrezo/', {'pk':pk}, function(data){
        izrisiMrezo(data[0].fields.sirina, data[0].fields.visina, data[0].fields.ime)
        
    });
    console.log(pk, '... pk')
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
