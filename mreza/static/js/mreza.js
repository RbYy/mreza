
$('#colorselector').colorselector();
var x=parseInt($('#mre').val().split('x')[0]);
var y=parseInt($('#mre').val().split('x')[1]);
var ime_mreze=$('#ime_mreze').val();
var aktivna=pk_default;

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
        ime_mreze=$('#ime_mreze').val();
        $.get('/ustvari_mrezo/',{
                                'sirina':x,
                                'visina':y,
                                'ime_mreze':ime_mreze},
                                function(pk){
                                    aktivna = pk;
                                    console.log('uspeh');
                                    $('.seznam_mrez').append('<li class="mreza_v_seznamu"><a id="mreza_'+ pk +'">'+ ime_mreze +'</a></li>');
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
/*povleciSeznamMrez();*/
izrisiMrezo(sirina_default, visina_default, ime_default);
    
$('#desno').on('click', '#dimenzije',function(){
    shraniNoveDimenzijeMreze();
    $('tr').remove();
    izrisiMrezo(x,y);
});
$('#desno').on('click', '#shrani',function(){
    
    ustvariMrezo();
});

$('.seznam_mrez').on('click','.mreza_v_seznamu', function(event){
    pk=event.target.id.split('_')[1];
    aktivna=pk
    $.getJSON('/aktiviraj_drugo_mrezo/', {'pk':pk}, function(data){
        izrisiMrezo(data[0].fields.sirina, data[0].fields.visina, data[0].fields.ime);
        
    });
    console.log(pk, '... pk')
});



$('#desno').on('click', '#novbat',function(){
    var barva=$(".btn-colorselector").css("background-color");
    var vrsta = 'vrsta'; /*to je za popravit -- drfault vrednost*/
    
    var xx=parseInt($('#velikost').val().split('x')[0]);
    var yy=parseInt($('#velikost').val().split('x')[1]);
    var ime=$('#ime').val();
    var zacetni_offset_x = 500;
    var zacetni_offset_y = 400;
    $.get('/ustvari_batiment/',{
                    'ime': ime,
                    'vrsta': vrsta,
                    'sirina': xx,
                    'visina': yy,
                    'offx': zacetni_offset_x,
                    'offy': zacetni_offset_y,
                    'aktivna': aktivna},
                    function(data){
                        var batiment_id=data;
                        console.log(data);
                        $('table').append('<div class=" lik ' + vrsta + '" id="lik'+ data + '"><p class="zapri" name="'+ data +'" id ="zapri">X</p><p id="naslov_'+ batiment_id +'" class="naslov"></p></div>');
                            $( ".lik" ).draggable({
                                        stop: function( event, ui ) {
                                            tx= $('#mreza');
                                            tx=tx.offset();
                                            offx=ui.offset['left'];
                                            offy=ui.offset['top'],
                                            ox=offx-tx.left;
                                            oy=offy-tx.top;
                                            
                                            $.get('/shrani_nove_koordinate_batimenta/', 
                                                                {'offx': ox,
                                                                'offy': oy,
                                                                'id': batiment_id}, 
                                                                function(data){
                                                                    console.log(tx.left + '--'+tx.top+'--'+offx+'--'+offy);
                                                                   console.log('shranjujem nove koordinate '+data) 
                                                                });
                                                                }
                            });
                                        
                                            
                        $('#lik'+data).css({
                                    "position": "absolute",
                                    "background-color": barva, 
                                    "opacity": 0.7,
                                    "left": x*30,
                                    "top": 300,
                                    "width":xx*25, 
                                    "height":yy*25} 
                                    );
                        $("#naslov_"+batiment_id).text(ime);
                        var offset=$('#lik'+data).offset();
                        console.log(offset);                        

   
 

                        $(function() {
                            $( ".lik" ).draggable({
                                snap:'true',
                                snap: 'td',
                                snapMode:"both",
                                snapTolerance: 20 
                            });
                        
                        });
                              
                        
                        $('.lik').on('click', '.zapri', function(event){
                                console.log('event');
                                 id=$(this).attr("name");
                                 $("#lik"+id).remove();
                                 $.get('/zbrisi_batiment/', {'id': id},
                                                        function(data){
                                                        console.log(data)
                                                    });
                         });
    });
 });
  console.log('dsf')
