function songo(ab) {
    document.getElementById('show_series').innerHTML = ab.substring(0, 4);
    $("#number_prefix").css("display", "none");
    loadnumbers();
}
function songolt(dug)
{
    document.getElementById('show').innerHTML = dug.substring(0, 8);
    loadnumbers();
}


function loadnumbers()
{
    var prefix = document.getElementById("show").innerHTML;
    console.log("loadnumbers");
    console.log(prefix);
    var az = document.getElementById("az").value;
    console.log(az);
    var numbertype = document.getElementById("numbertype").value;
    var number_index = 0;
    $.getJSON("/getnumber?movedown=1&move="+number_index+"&prefix="+prefix+"&az="+az+"&numbertype="+numbertype,function (data) {
        console.log(data);
        console.log(data.length);
        var prefixes = "";
        /*if (data.length == 0){
            prefixes = prefixes+"<tr><th onclick=\"alert('Sorry. Number not found!');\" style=\"font-size:21px\">ДУГААР ОЛДСОНГҮЙ</th></tr>";
        }
        else{*/
        var empty_couter = Object.keys(data[0]).length;
        //console.log("empty_couter");
        //console.log(empty_couter);
        var number_index = parseInt(data[1]);
        //console.log(number_index);
        $.each(data[0],function (key,val) {
            //console.log("val and jey");
            //console.log(val);
            //console.log(key);
            prefixes = prefixes + "<div onclick=\"javascript:songolt('" + key + "');\" style=\"font-size:36px; width: 180px; float: left; cursor: pointer; padding-left: 10px; margin-left: 70px; margin-bottom: 30px\">" + val + "</div>";
        });
        if (empty_couter<20){
            var i = 20-empty_couter;
            if (i==20){
                prefixes = prefixes+"<tr><th onclick=\"alert('Sorry. Number not found!');\" style=\"font-size:21px\">ДУГААР ОЛДСОНГҮЙ</th></tr>";
                i--;
            }
            for(i;i>=0;i--) {
                prefixes = prefixes + "<tr><th  style='font-size:36px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th></tr>";
            }
        }

        $("#available_number").html(prefixes);
        $("#available_number").css("display", "block");
        $("#number_prefix").css("display", "none");

        $("#available_move").html(number_index);

        if(prefix.length==8){
            if (empty_couter==1){
                console.log("length same");
                $("#3g_order").html("<a href='javascript:order()' class=\"Rectangle Oval1 col-md-1 btn_modal\" data-toggle=\"modal\" data-target=\"#myModal\" style=\"width: 150px; margin-left: 900px\" id=\"myBtn\">\n" +
                    "            <p class=\"txt26\" style=\"padding-top: 20px\">СОНГОХ</p>\n" +
                    "        </a>");
            }
            else{
                console.log("ifelse");
                $("#3g_order").html("<div class=\"Rectangle col-md-1\" style=\"width: 150px; margin-left: 900px\" id=\"3g_order\">\n" +
                    "            <p class=\"txt26\" style=\"padding-top: 20px\">СОНГОХ</p>\n" +
                    "        </div>");
            }
        }
        else{
            console.log("else");
          $("#3g_order").html("<div class=\"Rectangle col-md-1\" style=\"width: 150px; margin-left: 900px\" id=\"3g_order\">\n" +
              "            <p class=\"txt26\" style=\"padding-top: 20px\">СОНГОХ</p>\n" +
              "        </div>");
        }
        //}


    });

}

function loadseri()
{
    var prefix = document.getElementById("show_series").innerHTML;//$('#show_series').innerHTML;////

    console.log("loadseri");
    console.log(prefix);
    var number_index = 0;
    var category = document.getElementById("selectednumbertype").value;
    console.log(category);

    $.getJSON("/getprefix?numbertype="+category+"&movedown=1&move="+number_index+"&show_series="+prefix,function (data) {
        console.log(data);
        var prefixes = "";
        var empty_couter = Object.keys(data[0]).length;
        var number_index = parseInt(data[1]);
        console.log(number_index);
        $.each(data[0],function (key,val) {
           prefixes = prefixes + "<div onclick=\"javascript:songo('" + key + "');\" style=\"font-size:36px; width: 180px; float: left; cursor: pointer; padding-left: 100px; margin-bottom: 30px\">" + val + "</div>";
        });
        if (empty_couter<10){
            var i = 9-empty_couter;
            if (i==9){
                prefixes = prefixes+"<tr><th onclick=\"alert('Sorry. Number not found!');\" style=\"font-size:21px\">дугаар олдсонгүй</th></tr>";
                i--;
            }
            for(i;i>=0;i--) {
                prefixes = prefixes + "<tr><th  style='font-size:36px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th></tr>";
            }


        }

        $("#number_prefix").html(prefixes);

        $("#available_number").css("display", "none");
        $("#number_prefix").css("display", "block");

        $("#move_index").html(number_index);

    });

}


function seri(dugaar)
{
    document.getElementById('show_series').innerHTML = dugaar.substring(0, 2);
    document.getElementById('show_number').innerHTML = "";
    //$("#available_number").css("display", "none");
    loadseri();
    //loadnumbers();
}

function num(too)
{
    //var out = document.getElementById('show_number');
    var out_ser = document.getElementById('show');
    console.log("num");
    console.log(out_ser.innerHTML.length);
    //out_ser.innerHTML = out_ser.innerHTML.replace(/\*/g,"");
    if (too != '-')
    {
        if (out_ser.innerHTML.length < 8)
        {
            out_ser.innerHTML = out_ser.innerHTML + too;
            //loadseri();
        }
        /*else {
            if (out.innerHTML.length < 4)
                out.innerHTML = out.innerHTML + too;
            loadnumbers();
        }*/
    }
    else
    {
        /*if (out.innerHTML.length > 0)
        {
            out.innerHTML = out.innerHTML.slice(0, -1);
            loadnumbers();
        }
        else
        {*/
        if (out_ser.innerHTML.length > 0)
        {
            out_ser.innerHTML = out_ser.innerHTML.slice(0, -1);
            //loadseri();
        }
        //}
    }
    loadnumbers();
}

function order() {
    //console.log( document.getElementById("show").innerHTML);
    if (document.getElementById("show").innerHTML.length > 3) {
        var number = document.getElementById("show").innerHTML ;
        var category = document.getElementById("numbertype").value;
        var hel = document.getElementById("hel").value;
        var bagts = document.getElementById("bagts").value;
        var az = document.getElementById("az").value;

        console.log(hel);

        var pathArray = window.location.href.split("/");
        var protocol = pathArray[0];
        var host = pathArray[2];
        var url =protocol+"//" +host+ "/loadingselectednumber?hel="+hel+"&number="+number+"&numbertype="+category+"&bagts="+bagts+"&az="+az;
        window.location.href = url;
    }
}

function addStarR(le) {
    var star = "";
    if(le == 0){
        star = "**********";
    }
    if(le == 1){
        star = "*********";
    }
    if(le == 2){
        star = "********";
    }
    if(le == 3){
        star = "*******";
    }
    if(le == 4){
        star = "******";
    }
    if(le == 5){
        star = "*****";
    }
    if(le == 6){
        star = "****";
    }
    if(le == 7){
        star = "***";
    }
    if(le == 8){
        star = "**";
    }
    if(le == 9){
        star = "*";
    }
    return star;
}

function inputR(too){
    var out = document.getElementById('registr');
    out.innerHTML = out.innerHTML.replace(/\*/g,"");
    if (too != '-'){
        if (out.innerHTML.length < 10)
            out.innerHTML = out.innerHTML + too;
    }
    else{
        if (out.innerHTML.length > 0){
            out.innerHTML = out.innerHTML.slice(0, -1);
        }
    }
    out.innerHTML = out.innerHTML + addStarR(out.innerHTML.length);
}

function addUnder(le) {
    var star = "";
    if(le == 0){
        star = "";
    }
    return star;
}

function inp(too){
    var out = document.getElementById('mungunDun');
    out.innerHTML = out.innerHTML.replace(/\ /g,"");
    if (too != '-'){
        if (out.innerHTML.length < 6)
            out.innerHTML = out.innerHTML + too;
    }
    else{
        if (out.innerHTML.length > 0){
            out.innerHTML = out.innerHTML.slice(0, -1);
        }
    }
    out.innerHTML = out.innerHTML + addUnder(out.innerHTML.length);
}

function inpt(too){
    var out = document.getElementById('show_number');
    var out_ser = document.getElementById('show_series');

    out.innerHTML = out.innerHTML.replace(/\*/g,"");
    out_ser.innerHTML = out_ser.innerHTML.replace(/\*/g,"");
    if (too != '-'){
        if (out_ser.innerHTML.length < 4){
            out_ser.innerHTML = out_ser.innerHTML + too;
            //console.log(out_ser.innerHTML)
        }
        else {
            if (out.innerHTML.length < 4)
                out.innerHTML = out.innerHTML + too;
        }
    }
    else{
        if (out.innerHTML.length > 0){
            out.innerHTML = out.innerHTML.slice(0, -1);
        }
        else{
            if (out_ser.innerHTML.length > 0){
                out_ser.innerHTML = out_ser.innerHTML.slice(0, -1);
            }
        }
    }
    out_ser.innerHTML = out_ser.innerHTML + addStar(out_ser.innerHTML.length);
    out.innerHTML = out.innerHTML + addStar(out.innerHTML.length);
}

function addStar(le) {
    var star = "";
    if(le == 0){
        star = "****";
    }
    if(le == 1){
        star = "***";
    }
     if(le == 2){
        star = "**";
    }
     if(le==3){
        star = "*";
    }
    return star;
}


function modalCheckNumber(turul, hel, day_type, owner) {
    var number = document.getElementById("show_series").innerHTML + document.getElementById("show_number").innerHTML;
    var pathArray = window.location.href.split("/");
    var protocol = pathArray[0];
    var host = pathArray[2];
    console.log(number);
    var url = "";
    if(turul == "payment"){
        url = protocol+"//" +host+ "/"+turul+"/modalTulburiinSongolt?hel="+hel+"&number="+number+"&owner="+owner+"&turul="+turul;
        console.log("modalCheckNumber");
        console.log(url);
        $.get(url, function(data, status) {
            console.log(status);
            console.log("Ajax function");
            console.log(data);
            $("#myModal .modal-content").html(data);
            $("#myModal").css('display', 'block');
            if(status == "success") {

            }
        });
    }
    else{
        if(turul == "restoresim"){
            url = protocol+"//" +host+ "/"+turul+"/loadingModalCheckNumber?hel="+hel+"&number="+number;
        }
        else{
            url = protocol+"//" +host+ "/"+turul+"/select_product?hel="+hel+"&number="+number+"&turul="+turul+"&day_type="+day_type;
        }
        window.location.href = url;
    }
}

function cashOrCard(number, hel, tulbur, owner, turul, register) {
    var mungunDun = document.getElementById("mungunDun").innerHTML;
    var pathArray = window.location.href.split("/");
    var protocol = pathArray[0];
    var host = pathArray[2];
    console.log(mungunDun);
    if(tulbur == "kartaar"){
        var url =protocol+"//" +host+ "/"+turul+"/cashOrCard?hel="+hel+"&number="+number+"&mungunDun="+mungunDun+"&tulbur="+tulbur+"&owner="+owner+"&turul="+turul+"&register="+register;
        window.location.href = url;
    }
    else{
        var url =protocol+"//" +host+ "/"+turul+"/cashOrCard?hel="+hel+"&number="+number+"&mungunDun="+mungunDun+"&tulbur="+tulbur+"&owner="+owner+"&turul="+turul+"&register="+register;
        console.log(url);
        $.get(url, function(data, status) {
            console.log(status);
            console.log("Ajax function");
            console.log(data);

            $("#myModal .modal-content").html(data);
            $("#myModal").css('display', 'block');

            if(status == "success") {

            }
        });
    }

}

function login() {
    var ner = document.getElementById("ner").value;
    var nuutsUg = document.getElementById("nuutsUg").value;
    var pathArray = window.location.href.split("/");
    var protocol = pathArray[0];
    var host = pathArray[2];
    var url =protocol+"//" +host+"/niitShaardah?ner="+ner+"&nuutsUg="+nuutsUg;
    console.log(url);
    window.location.href = url;
}

function modalBtnClick() {
    var url = $(this).attr("href");
    var final_url = url;
    console.log("modalBtnClick");
    console.log(final_url);

    $.get(final_url, function(data, status) {

        console.log(data);

        $("#myModal .modal-content .modal_data").html(data);
        $("#myModal").css('display', 'block');

        if(status == "success") {

        }
    });

    return false;
}

function move(time) {
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, time);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
}

