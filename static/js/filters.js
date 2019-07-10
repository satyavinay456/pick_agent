$(document).ready(function() {
 $("#tot_exp_filter").click(function() {
    $("#loader").show();
    $.ajax({
              url: "/tot_exp_filter",
              data:{"filter_on":"TotalExperience"},
              type: 'POST',
              success : function(data){
                $("#loader").hide();
                $("#agents_cards").html(data.html_data);
                $("#agents_count").html(data.agents_count);
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
                $("#loader").hide();
                $("#agents_cards").html(data.html_data);
                $("#agents_count").html(data.agents_count);
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
                $("#agents_cards").html(data.html_data);
                $("#agents_count").html(data.agents_count);
              },
              error: function (request, status, error) { $("#loader").hide();alert(request); }
        }); // end ajax url
 }); //end submit_btn

 $("#exam_apply").click(function() {
   $("#loader").show();
   var exams_checked = [];
    $(':checkbox:checked').each(function(i){
            exams_checked[i] = $(this).val();
    });
    console.log(exams_checked);
    console.log($.type(exams_checked));

   //alert($('input[name=exam_checkboxes]:checked').length);
   if ($('input[name=exam_checkboxes]:checked').length<1){
     $("#loader").hide();
     return;
   }
   $.ajax({
             url: "/exams_filter",
             data:{"filter_on":$('input[name=exam_checkboxes]:checked').length,"exams_checked":exams_checked},
             type: 'POST',
             success : function(data){
               $("#loader").hide();
               $("#agents_cards").html(data.html_data);
               $("#agents_count").html(data.agents_count);
             },
             error: function (request, status, error) { $("#loader").hide(); alert(request); }
       }); // end ajax url
 });

});
