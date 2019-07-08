$(document).ready(function() {
 $("#submit_btn").click(function() {

    //console.log($("#entered_city").val());
    if ($("#entered_city").val()==""){
      alert("Please enter valid text");
      return;
    }
    // alert($("#entered_city").val());
    $.ajax({
              url: "/city_code",
              data : { 'entered_city': $("#entered_city").val() } ,
              type: 'POST',
              success : function(data){
                // if (response=="by_success"){
                //   $("#main_card .card-body "+id+"ed").show();
                // }
                window.location = data;
              },
              error: function (request, status, error) { alert(request); }
        }); // end ajax url
 }); //end submit_btn


 $('#entered_city').keydown(function (e){
    if(e.keyCode == 13){
      if ($("#entered_city").val()==""){
        alert("Please enter valid text");
        return;
      }
      // alert($("#entered_city").val());
      $.ajax({
                url: "/city_code",
                data : { 'entered_city': $("#entered_city").val() } ,
                type: 'POST',
                success : function(data){
                  // if (response=="by_success"){
                  //   $("#main_card .card-body "+id+"ed").show();
                  // }
                  window.location = data;
                },
                error: function (request, status, error) { alert(request); }
          }); // end ajax url
    }
})

});
