/**
 * Created by Carlos on 2/28/2015.
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getWidth() {
    var x = 0;
    if (typeof(document.body.clientWidth) == 'number') {
// Newer generation of browsers
        x = document.body.clientWidth;
    }
    else if (typeof( window.innerWidth ) == 'number') {
//None Internet Explorer
        x = window.innerWidth;
    }
    else if (document.documentElement && document.documentElement.clientWidth) {
//Internet Explorer 6 and above in 'standards compliant mode'
        x = document.documentElement.clientWidth;
    }
    return x;
}

function getHeight() {
    var x = 0;
    if (typeof( window.innerHeight ) == 'number') {
//None Internet Explorer
        x = window.innerHeight;
    }
    else if (document.documentElement && document.documentElement.clientHeight) {
//Internet Explorer 6 and above in 'standards compliant mode'
        x = document.documentElement.clientHeight;
    }
    return x;
}

//If top=false the comments are placed on top of the div.
function insert_comments(data, top, lang) {
    var big_comments_div = document.getElementById("comentarios");

    for (var i = 0; i < data['comentarios'].length; i++) {
        var x = data['comentarios'][i];
        var new_div = document.createElement("div");
        new_div.classList.add("comentario");
        new_div.id = x[2];
        if (top == true || (big_comments_div.firstChild == undefined) || (big_comments_div.firstChild == null)) {
            big_comments_div.appendChild(new_div);
        }
        else {
            //big_div.appendChild(new_div);
            big_comments_div.insertBefore(new_div, big_comments_div.firstChild);
        }
        var p_title = document.createElement("p");
        if (lang == "es")
            p_title.innerHTML = x[3] + " " + x[0] + " comentó";
        else
            p_title.innerHTML = x[3] + " " + x[0] + " commented";
        //p_title.style.fontStyle = "italic";
        new_div.appendChild(p_title);
        var p_text = document.createElement("p");
        p_text.textContent = x[1];
        new_div.appendChild(p_text);
        $("#" + x[2]).fadeIn(750);
        if (document.getElementById("number_comentarios" != null)) {
            var num_com = parseInt(document.getElementById("number_comentarios").innerText, 10) + 1;
            document.getElementById("number_comentarios").innerText = num_com.toString();
        }
    }
    var num_comments = $("#number_comentarios");
    if (num_comments.length > 0) {
        num_comments[0].innerText = parseInt(num_comments[0].innerText, 10) + data['comentarios'].length;
    }
}

function updateComments(id, language) {
    var a = $("#comentarios").find("> div:first")[0];
    if (a == undefined)
        a = -1;
    else {
        a = a.id;
    }

    var request = $.post("/ajax_noticias/" + id + "/", {pk_last_comment: a, language: language});
    request.done(function (data) {
        insert_comments(data, false, language);
    });
}

//Parent node is the node which id is comentarios
function insert_commentsImg(data, top, parent_node, lang) {
    for (var i = 0; i < data['comentarios'].length; i++) {
        var x = data['comentarios'][i];
        var new_div = document.createElement("div");
        new_div.classList.add("comentario");
        new_div.id = x[2];
        if (top == true || (parent_node.firstChild == undefined) || (parent_node.firstChild == null)) {
            parent_node.appendChild(new_div);
        }
        else {
            //big_div.appendChild(new_div);
            parent_node.insertBefore(new_div, parent_node.firstChild);
        }
        var p_title = document.createElement("p");
        if (lang == "es")
            p_title.innerHTML = x[3] + " " + x[0] + " comentó";
        else
            p_title.innerHTML = x[3] + " " + x[0] + " commented";
        //p_title.style.fontStyle = "italic";
        new_div.appendChild(p_title);
        var p_text = document.createElement("p");
        p_text.textContent = x[1];
        new_div.appendChild(p_text);
        $("#" + x[2]).fadeIn(750);
        if (document.getElementById("number_comentarios" != null)) {
            var num_com = parseInt(document.getElementById("number_comentarios").innerText, 10) + 1;
            document.getElementById("number_comentarios").innerText = num_com.toString();
        }
    }
    var num_comments = $("#number_comentarios");
    if (num_comments.length > 0) {
        num_comments[0].innerText = parseInt(num_comments[0].innerText, 10) + data['comentarios'].length;
    }
}

function updateCommentsImageNode(id, language, parent_node) {
    var a = $("#comentarios").find("> div:first");
    var no_com_tit = $("#no_comments_title");
    if (a.length == 0) {
        a = -1;
        if (no_com_tit.length == 0) {

        }
    }
    else {
        a = a[0].id;
    }

    var request = $.post("/imagen/" + id + "/", {pk_last_comment: a, language: language});
    request.done(function (data) {
        var no_com_tit = $("#no_comments_title");
        if (a == -1 && (no_com_tit.length == 0) && (data['comentarios'].length == 0)) {
            var title_node = document.createElement("h5");
            title_node.id = "no_comments_title";
            if (language == "es")
                title_node.innerText = "Esta imagen no tiene comentarios ¡Se el primero en comentar!";
            else
                title_node.innerText = "This imagen has no comments. Be the first to comment!";
            document.getElementById("comentarios").appendChild(title_node);
        }
        else {
            if (no_com_tit.length > 0 && data['comentarios'].length > 0) {
                no_com_tit.fadeOut('slow');
                no_com_tit.remove();
            }
        }
        insert_commentsImg(data, false, parent_node, language);
    });
}


function updateCommentsImage(id, language) {
    var a = $("#comentarios").find("> div:first");
    var no_com_tit = $("#no_comments_title");
    if (a.length == 0) {
        a = -1;
        if (no_com_tit.length == 0) {

        }
    }
    else {
        a = a[0].id;
    }

    var request = $.post("/imagen/" + id + "/", {pk_last_comment: a, language: language});
    request.done(function (data) {
        var no_com_tit = $("#no_comments_title");
        if (a == -1 && (no_com_tit.length == 0) && (data['comentarios'].length == 0)) {
            var title_node = document.createElement("h5");
            title_node.id = "no_comments_title";
            if (language == "es")
                title_node.innerText = "Esta imagen no tiene comentarios ¡Se el primero en comentar!";
            else
                title_node.innerText = "This imagen has no comments. Be the first to comment!";
            document.getElementById("comentarios").appendChild(title_node);
        }
        else {
            if (no_com_tit.length > 0 && data['comentarios'].length > 0) {
                no_com_tit.fadeOut('slow');
                no_com_tit.remove();
            }
        }
        insert_commentsImg(data, false, document.getElementById("comentarios"), language);
    });
}

function validateEmail(email) {
    var re;
    re = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])/;
    return re.test(email);
}


function emailValidationOnTheFly(objeto) {
    if (validateEmail(objeto.value)) {
        objeto.style.color = "green";
        //$("#message").text("");
    }
    else {
        objeto.style.color = "red";
        //$("#message").text(objeto.value).show();
    }
}

function CookiesName(user_node) {
    var usuario = getCookie('buenviaje_usuario');
    if (usuario != null) {
        if (usuario.split('"')[1] != undefined) {
            user_node.value = usuario.split('"')[1];
        }
        else {
            user_node.value = usuario;
        }
    }
}

function CookiesEmail(email_node) {
    var correo = getCookie('buenviaje_correo');
    if (correo != null) {
        email_node.value = correo.split('"')[1];
    }
}


function CookiesNotify(unotify_node) {
    var notify = getCookie('buenviaje_notify');
    if (notifyme) {
        if (notify != null) {
            notify_node.checked = true;
        }
    }
}

function CookiesJob() {
    var usuario = getCookie('buenviaje_usuario');
    if (usuario != null) {
        if (usuario.split('"')[1] != undefined) {
            document.getElementById("POST-name").value = usuario.split('"')[1];
        }
        else {
            document.getElementById("POST-name").value = usuario;
        }
    }
    var correo = getCookie('buenviaje_correo');
    if (correo != null) {
        document.getElementById("POST-email").value = correo.split('"')[1];
    }
    var notify = getCookie('buenviaje_notify');
    if (notify != null) {
        document.getElementById("checkbox").checked = true;
    }
}

//This function recieves a node (should be a div) and shows it like a modal. Remove indicates if the node should be removed when the modal is not showing.
function show_node(node, remove, id_to_save, function_remove) {
    var big_div = document.createElement("div");
    big_div.id = "big_div";

    //This creates the shadow effect
    var background_div = document.createElement("div");
    background_div.id = "background_div";
    background_div.onclick = function () {
        $("#big_div").fadeOut("slow", function () {
            var bg_dv = document.getElementById("big_div");
            node.classList.remove("container_div");
            node.style.display = "none";
            if (remove)
                document.getElementsByTagName("body")[0].appendChild(node);
            if (id_to_save)
                document.getElementsByTagName("body")[0].appendChild(document.getElementById(id_to_save));
            clearInterval(pictureInterval);
            function_remove();
            document.getElementsByTagName("body")[0].removeChild(bg_dv);
        });
    };

    node.classList.add("container_div");

    big_div.appendChild(background_div);
    big_div.appendChild(node);

    document.getElementsByTagName("body")[0].appendChild(big_div);
    node.style.display = "block";

    $("#big_div").fadeIn("slow");
}

function prep_the_pictures(id, info, lang) {
    var image_container = document.getElementById("demo" + id);
    for (var i = 0; i < info.length; i++) {
        var divv = document.createElement("div");
        divv.className = "item";
        divv.setAttribute("data-w", info[i][0][1]);
        divv.setAttribute("data-h", info[i][0][2]);
        divv.setAttribute("data-id", info[i][2]);
        divv.setAttribute("data-width_big", info[i][3][1]);
        divv.setAttribute("data-height_big", info[i][3][2]);
        divv.setAttribute("data-src_big", info[i][3][0]);
        divv.setAttribute("data-usuario", info[i][4]);
        divv.setAttribute("data-description", info[i][5]);
        divv.setAttribute("rel", "tooltip");
        divv.setAttribute("data-trigger", "hover");
        divv.setAttribute("data-html", "True");
        if (lang == "es")
            divv.setAttribute("data-original-title", "<p>" + info[i][5] + "</p><p>Subida por " + info[i][4] + "</p> <p>" + info[i][1] + " comentarios</p>");
        else
            divv.setAttribute("data-original-title", "<p>" + info[i][5] + "</p><p>Uploaded by " + info[i][4] + "</p> <p>" + info[i][1] + " comments</p>");


        var img = document.createElement("img");
        img.src = info[i][0][0];
        var tag = document.createElement("a");
        //{#            tag.innerHTML = info[i][2];#}
        tag.setAttribute("href", "/imagen/" + info[i][2] + "/#img_container_big");
        divv.appendChild(tag);
        tag.appendChild(img);
        //DONE: Check is the viewport.width is less than 768, if that's the case don't rewrite the onclick.
        tag.onclick = modal_launcher(divv, lang);
        image_container.appendChild(divv);
    }
    $('[rel=tooltip]').tooltip();
    $("#demo" + id).fadeIn('slow').flexImages({rowHeight: 200});
}

function modal_launcher(node, lang) {
    return function () {
        var img_id = node.getAttribute("data-id");
        var img_width = node.getAttribute("data-width_big");
        var img_heigth = node.getAttribute("data-height_big");
        var img_src = node.getAttribute("data-src_big");
        var img_usuer = node.getAttribute("data-usuario");
        var img_descr = node.getAttribute("data-description");
        if (parseInt(img_width, 10) + 80 + 520 < getWidth()) {
            var height_modal = getHeight() - ( parseInt(img_heigth, 10) + 144);
            if (height_modal > 20) {
                prep_img_modal(img_id, img_width, img_heigth, img_src, img_usuer, img_descr, lang, height_modal);
                return false;
            }
        }
        node.firstChild.href = "/imagen/" + img_id + "/?languague=es" + "&width=" + getWidth() + "&height=" + getHeight() + "#img_container_big";
    };
}

function submitFunction(img_id, parent_node, lang) {
    return function () {
        var trext = document.getElementById("textarea").value;
        var nombre = document.getElementById("POST-name").value;
        var email = document.getElementById("POST-email").value;
        var check = document.getElementById("checkbox").checked;
        if (trext == "") {
            $("#textarea").tooltip('show');
            hideTooltipMessage("textarea");
            return false;
        }
        else {
            if (nombre == "" && email == "") {
                $("#POST-name").tooltip('show');
                hideTooltipMessage("POST-name");
                return false;
            }
            else {
                if (check == true && email == "") {
                    $("#checkbox").tooltip('show');
                    hideTooltipMessage("checkbox");
                    return false;
                }
            }

        }
        var a = $("#comentarios").find("> div:first")[0];
        if (a == undefined)
            a = -1;
        else {
            a = a.id;
        }
        if (check == true) {
            var request = $.post("/imagen/" + img_id + "/", {
                texto: trext,
                nombre: nombre,
                email: email,
                pk_last_comment: a,
                noti: "true",
                language: lang
            });
        }
        else {
            var request = $.post("/imagen/" + img_id + "/", {
                texto: trext,
                nombre: nombre,
                email: email,
                pk_last_comment: a,
                language: lang
            });
        }
        request.done(function (data) {
            if (data['error']) {
                $("#POST-email").tooltip('show');
                hideTooltipMessage("POST-email");
            }
            else {
                document.getElementById("textarea").value = "";
                var no_com_tit = $("#no_comments_title");
                if (no_com_tit.length > 0) {
                    no_com_tit.fadeOut('slow');
                    no_com_tit.remove();
                }
                insert_commentsImg(data, false, parent_node, lang);
            }
        });
        return false;
    }
}

function prep_img_modal(img_id, img_width, img_heigth, img_src, img_usuer, img_descr, lang, modal_height) {
    var new_img_container = document.createElement("div");
    new_img_container.classList.add("my_modal_div");
    new_img_container.style.top = modal_height / 4 + "px";

    //This must be done here so we can pass the node comments_content to submitFunction.
    var comments_content = document.createElement("div");
    comments_content.id = "comentarios";

    //The submit buttom part (a f**cking nightmare)
    var submit_buttom = document.createElement("input");
    submit_buttom.type = "submit";
    submit_buttom.classList.add("form-control");
    submit_buttom.classList.add("btn");
    submit_buttom.classList.add("default-btn");
    submit_buttom.classList.add("img_form_element");
    if (lang == 'es')
        submit_buttom.value = "Comentar";
    else
        submit_buttom.value = "Comment";
    submit_buttom.id = "submit";
    submit_buttom.onclick = submitFunction(img_id, comments_content, lang);

    document.getElementById("comment_form").insertBefore(submit_buttom, document.getElementById("checkbox"));

    //Image side
    var imagen_div = document.createElement("div");
    imagen_div.classList.add("img_left_container");
    imagen_div.style.width = parseInt(img_width, 10) + "px";
    var imagen = document.createElement("img");
    imagen.src = img_src;
    var description = document.createElement("p");
    description.innerText = img_descr;
    var uploader = document.createElement("p");
    if (lang == "es")
        uploader.innerHTML = "<strong>Imagen subida por </strong>" + img_usuer;
    else
        uploader.innerHTML = "<strong>Uploaded by </strong>" + img_usuer;
    imagen_div.appendChild(imagen);
    imagen_div.appendChild(description);
    imagen_div.appendChild(uploader);

    //Comments side
    var comments_div = document.createElement("div");
    comments_div.classList.add("comm_right_container");
    comments_div.style.width = 520 + "px";
    var comment_form = document.getElementById("comment_form");
    comment_form.style.display = "block";

    comments_content.classList.add("comm_right_container");
    comments_content.style.height = parseInt(img_heigth, 10) + 5 + "px";
    comments_content.style.border = 0 + "px";
    comments_div.appendChild(comments_content);
    comments_div.appendChild(comment_form);


    new_img_container.style.width = parseInt(img_width, 10) + 80 + 520 + "px";


    new_img_container.appendChild(imagen_div);
    new_img_container.appendChild(comments_div);

    //If something breaks change those methods, just call the old ones
    updateCommentsImageNode(img_id, lang, comments_content);

    pictureInterval = setInterval(function () {
        updateCommentsImageNode(img_id, lang, comments_content)
    }, 10000);


    show_node(new_img_container, false, "comment_form", function () {
        document.getElementById("comment_form").removeChild(document.getElementById("submit"));
        document.getElementById("comment_form").style.display = "none";
    });

    CookiesJob();
}

function hideTooltipMessage(id_tooltip) {
    window.setTimeout(function () {
        $("#" + id_tooltip).tooltip('hide');
    }, 1500);
}
