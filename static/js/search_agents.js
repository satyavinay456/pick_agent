$(document).ready(function() {
  // alert("sdg");
   $('#search_agents').keyup(function (e){
     if ($("#search_agents").val()==""){
       return;
     }
     $("#loader").show();
      $.ajax({
                url: "/search_agents",
                data : { 'search_word': $("#search_agents").val() } ,
                type: 'POST',
                success : function(data){
                    $("#loader").hide();
                    $("#agents_cards").html(data.html_data);
                    $("#agents_count").html(data.agents_count)
                },
                error: function (request, status, error) { $("#loader").hide();alert(request); }
          }); // end ajax url
    });
}); //end document ready
