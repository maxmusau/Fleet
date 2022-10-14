  $(document).ready(function(){
      $("#changeForm").on("submit", function(event){
           $.ajax({
                 data: {
                     current_password: $("#current_password").val(),
                     new_password: $("#new_password").val(),
                     confirm_password: $("#confirm_password").val()
                 },//end data
                 type: 'POST',
                 url:"/change_password"
           })//end ajax
           //Wait for response from Python without reloading Page
           .done(function(data){
                 if(data.currentWrong){
                      //handle error
                      $("#currentWrong").text(data.currentWrong).show();
                      $("#newWrong").hide();
                      $("#confirmWrong").hide(); $("#success").hide(); $("#error").hide();
                 }
                 else if(data.newWrong){
                     //handle error
                      $("#newWrong").text(data.newWrong).show();
                      $("#currentWrong").hide();
                      $("#confirmWrong").hide(); $("#success").hide(); $("#error").hide();
                 }

                 else if(data.confirmWrong){
                     //handle error
                      $("#confirmWrong").text(data.confirmWrong).show();
                      $("#newWrong").hide();
                      $("#currentWrong").hide(); $("#success").hide(); $("#error").hide();
                 }

                  else if(data.error){
                     //handle error
                      $("#error").text(data.error).show();
                      $("#newWrong").hide();
                      $("#currentWrong").hide(); $("#success").hide(); $("#confirmWrong").hide();
                 }

                 else {
                    //Handle a success
                      $("#success").text(data.success).show();
                      $("#newWrong").hide();
                      $("#currentWrong").hide(); $("#error").hide(); $("#confirmWrong").hide();
                      $("#current_password").val("");
                      $("#new_password").val("");
                      $("#confirm_password").val("");
                 }
           });//end done

           event.preventDefault();
      });//end submit
  });//end ready