$(document).ready(function() {
 $("#tot_exp_filter").click(function() {
    $("#loader").show();
    $.ajax({
              url: "/tot_exp_filter",
              data:{"filter_on":"TotalExperience"},
              type: 'POST',
              success : function(data){
                  $("#loader").hide();
                  $("#agents_cards").html(data);
              },
              error: function (request, status, error) { $("#loader").hide(); alert(request); }
        }); // end ajax url
 }); //end submit_btn

 $("#current_city_filter").click(function() {
   $("#loader").show();
    $.ajax({
              url: "/tot_exp_filter",
              data:{"filter_on":"PresentExperience"},
              type: 'POST',
              success : function(data){
                  console.log(data);
                  $("#loader").hide();
                  $("#agents_cards").html(data);
              },
              error: function (request, status, error) { $("#loader").hide();alert(request); }
        }); // end ajax url
 }); //end submit_btn

 $("#sro_filter").click(function() {
   $("#loader").show();
    $.ajax({
              url: "/tot_exp_filter",
              data:{"filter_on":"SRO"},
              type: 'POST',
              success : function(data){
                  $("#loader").hide();
                  $("#agents_cards").html(data);
              },
              error: function (request, status, error) { $("#loader").hide();alert(request); }
        }); // end ajax url
 }); //end submit_btn
 $("#License_filter").click(function() {
   $("#loader").show();
    $.ajax({
              url: "/tot_exp_filter",
              data:{"filter_on":"Licenses"},
              type: 'POST',
              success : function(data){
                  $("#loader").hide();
                  $("#agents_cards").html(data);
              },
              error: function (request, status, error) { $("#loader").hide();alert(request); }
        }); // end ajax url
 }); //end submit_btn

});
