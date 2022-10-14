 $(document).ready(function(){
      $("#typeForm").on("submit", function(event){
           $.ajax({
                 data: {
                     type: $("#type").val()   //get make from input
                 },//end data
                 type: 'POST',
                 url:"/addType"
           })//end ajax
           //Wait for response from Python without reloading Page
           .done(function(data){
                 if(data.error1){
                      //handle error
                      $("#warningAlert").text(data.error1).show();
                      $("#errorAlert").hide();
                      $("#successAlert").hide();
                 }
                 else if(data.error2){
                     //handle error
                      $("#warningAlert").hide();
                      $("#errorAlert").text(data.error2).show();
                      $("#successAlert").hide();
                 }
                 else {
                    //Handle a success
                      $("#warningAlert").hide();
                      $("#errorAlert").hide();
                      $("#successAlert").text(data.success).show();
                      $("#type").val("");
                 }
           });//end done

           event.preventDefault();
      });//end submit
  });//end ready