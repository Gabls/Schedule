$(document).ready(function(){
    //Adicionar Evento
    $("#btnAddEvent").click(function(){
        $("#addEvent").css("display", "flex").hide().fadeIn();
    });
    $("#addEvent .background").click(function(){
        $("#addEvent").fadeOut();
    });
    
    //Adicionar Usuário
    $("#btnAddUser").click(function(){
        $("#addUser").css("display", "flex").hide().fadeIn();
    });
    $("#addUser .background").click(function(){
        $("#addUser").fadeOut();
    });

    //Entrar Evento
    $("#btnEnterEvent").click(function(){
        $("#enterEvent").css("display", "flex").hide().fadeIn();
    });
    $("#enterEvent .background").click(function(){
        $("#enterEvent").fadeOut();
    });

    //Alerta
    $("#alert").css("display", "flex").hide().fadeIn();
    $("#alert .background").click(function(){
        $("#alert").fadeOut();
    });

});