var x=parseInt($('#mre').val().split('x')[0]);
var y=parseInt($('#mre').val().split('x')[1]);
var ime_mreze=$('#ime_mreze').val();
var aktivna=pk_default;
var barve = {
    "1":"green",
    "2":"red",
    "3":"blue",
    "4":"brown",
    "5":"yellow",
    "6":"orange",
    "7":"salmon",
    "8":"dimgray"
};

function aktivirajDrugoMrezo(pk){
    $.getJSON('/aktiviraj_drugo_mrezo/', {'pk':pk}, function(data){
        izrisiMrezo(data[0].fields.sirina, data[0].fields.visina, data[0].fields.ime);
        jQuery.each(data.slice(2), function(i, val) {
            args=val['fields'];
            izrisi_batiment(val['pk'], 
                            args.sirina_bat, 
                            args.visina_bat, 
                            args.pozx, 
                            args.pozy, 
                            args.ime, 
                            args.vrsta, 
                            args.vrsta);         
        }); 
    });
}

function ustvariMrezo(ime_mreze){    
/*ne izrisuje mreze; ustvari novo v bazi in doda na seznam*/
    ime_mreze=$('#ime_mreze').val();
    $.get('/ustvari_mrezo/',{
                            'ime_mreze':ime_mreze},
                            function(pk){
                                var aktivna = pk;
                                $('.seznam_mrez').append('<li class="mreza_v_seznamu"><a id="mreza_'+ pk +'">'+ ime_mreze +'</a></li>');
                            });
        return aktivna;
    }

function izrisiMrezo(sirina,visina,ime){
    /*samo graficno izrise mrezo; tudi caption*/
    $('.grid').remove();
    $('caption').text(ime+'  '+sirina+'x'+visina);
    for (var i=1; i<=visina; i++){
        $('.t').append("<tr class='grid' id=vrsta_" + i + "></tr>");
        for (var j=1; j<=sirina; j++){
            $('#vrsta_'+ i).append('<td id=' + j + '_' + i +'></td>');
        }
    }
}

function shraniNoveDimenzijeMreze(x,y){
    /*ne preminja videza strani*/
    $.get('/shrani_nove_dimenzije_mreze/',{
                            'sirina':x,
                            'visina':y,},
                            function(data){
                            });
}

function izrisi_batiment(data, sirina, visina, x, y, ime, vrsta,barva){
    /*ustvarjanje novega batimenta z event handlerji*/
    barva=barve[vrsta];
    var batiment_id=data;
    sirina=parseInt(sirina);
    visina=parseInt(visina);
    $('table').append('<div class=" lik ' + vrsta + '" id="lik'+ batiment_id + '"><p class="zapri" name="'+ batiment_id +'" id ="zapri">X</p><p id="naslov_'+ batiment_id +'" class="naslov"></p></div>');
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
                                             'id': $(this).attr('id').slice(3)}, 
                                             function(data){
                                             });
                                             }
         });
                               
     $('#lik'+batiment_id).css({
                 "position": "absolute",
                 "background-color": barva, 
                 "opacity": 0.7,
                 "left": x,
                 "top": y,
                 "width":sirina*25, 
                 "height":visina*25,} 
                 );
     $("#naslov_"+batiment_id).text(ime);
    
     $(function() {
         $( ".lik" ).draggable({
             snap:'true',
             snap: 'td',
             snapMode:"both",
             snapTolerance: 20 
         });
     });
           
     $('.lik').on('click', '.zapri', function(event){
              id=$(this).attr("name");
              $("#lik"+id).remove();
              $.get('/zbrisi_batiment/', {'id': id},
                                     function(data){
                                 });
      });
}                         
       
function izrisiZacetnoStanje(){                         
    $.getJSON('/poslji_komplet/', {}, function(data){
        izrisiMrezo(data[0].fields.sirina, data[0].fields.visina, data[0].fields.ime);
        jQuery.each(data.slice(2), function(i, val) {
            args=val.fields;
            izrisi_batiment(val.pk, 
                            args.sirina_bat, 
                            args.visina_bat, 
                            args.pozx, 
                            args.pozy, 
                            args.ime, 
                            args.vrsta, 
                            args.vrsta);         
        }); 
    });
}    


izrisiZacetnoStanje();

    
$('#desno').on('click', '#dimenzije',function(){
    /*klik na gumb za potrditev spremembe dimenzije mreze*/
    x=parseInt($('#mre').val().split('x')[0]);
    y=parseInt($('#mre').val().split('x')[1]);
    izrisiMrezo(x,y,ime_mreze);
    shraniNoveDimenzijeMreze(x,y);
    $('form')[0].reset();
});

$('#desno').on('click', '#shrani',function(){
    /*klik na gumb za shranjevanje trenutne mreze in postavitve*/    
    var pk=ustvariMrezo(ime_mreze);
    aktivirajDrugoMrezo(pk);
    $('form')[0].reset();
});

$('.seznam_mrez').on('click','.mreza_v_seznamu', function(event){
    /* preklapljanje med shranjenimi mrezammi */
    $('.lik').remove();
    pk=event.target.id.split('_')[1];
    aktivna=pk
    aktivirajDrugoMrezo(pk);
});
                         
$('#desno').on('click', '#novbat',function(){
    /*klik na gumb ustvari nov batiment*/
    barva=$("#vrsta").val();
    vrsta = $("#vrsta").val();
    var xx=parseInt($('#velikost').val().split('x')[0]);
    var yy=parseInt($('#velikost').val().split('x')[1]);
    var ime=$('#ime').val();
    var zacetni_offset_x = 500;
    var zacetni_offset_y = 400;
    $.get('/ustvari_batiment/',{
                    'ime': ime,
                    'vrsta': $("#vrsta").val(),
                    'sirina': xx,
                    'visina': yy,
                    'offx': zacetni_offset_x,
                    'offy': zacetni_offset_y,
                    'aktivna': aktivna},
                    function(data){
                        izrisi_batiment(data, 
                                        xx, 
                                        yy, 
                                        zacetni_offset_x, 
                                        zacetni_offset_y, 
                                        ime, 
                                        vrsta, 
                                        barva);
                    });
});


