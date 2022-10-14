$(document).ready(function(){
               var x = "";
               $(".gender").click(function () {
                      x = $(this).val();
               });

              $("#userForm").on("submit", function(event){
                  //alert(gender1);
                   $("#successAlert").text("Please wait.. Uploading Data").show();
                   $.ajax({
                         data: {
                             fname: $("#fname").val(),
                             lname: $("#lname").val(),
                             surname: $("#surname").val(),
                             gender: x,
                             role: $("#role").val(),
                             phone: $("#phone").val(),
                             email: $("#email").val(),
                         },//end data
                         type: 'POST',
                         url:"/addUser"
                   })//end ajax

           //Wait for response from Python without reloading Page
           .done(function(data){
                 if(data.errorFname){
                      //handle error
                      $("#errorFname").text(data.errorFname).show();
                      $("#errorLname").hide();  $("#errorGender").hide(); $("#errorRole").hide();
                      $("#errorSurname").hide(); $("#errorPhone").hide(); $("#errorEmail").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }
                 else if(data.errorLname){
                     //handle error
                      $("#errorLname").text(data.errorLname).show();
                      $("#errorFname").hide();
                      $("#errorGender").hide(); $("#errorRole").hide();
                      $("#errorSurname").hide(); $("#errorPhone").hide(); $("#errorEmail").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }

                  else if(data.errorSurname){
                     //handle error
                      $("#errorSurname").text(data.errorSurname).show();
                      $("#errorFname").hide();
                      $("#errorGender").hide(); $("#errorRole").hide();
                      $("#errorLname").hide(); $("#errorPhone").hide(); $("#errorEmail").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }

                  else if(data.errorGender){
                     //handle error
                      $("#errorGender").text(data.errorGender).show();
                      $("#errorFname").hide();
                      $("#errorSurname").hide(); $("#errorRole").hide();
                      $("#errorLname").hide(); $("#errorPhone").hide(); $("#errorEmail").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }

                 else if(data.errorRole){
                     //handle error
                      $("#errorRole").text(data.errorRole).show();
                      $("#errorFname").hide();
                      $("#errorSurname").hide(); $("#errorGender").hide();
                      $("#errorLname").hide(); $("#errorPhone").hide(); $("#errorEmail").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }

                  else if(data.errorPhone){
                     //handle error
                      $("#errorPhone").text(data.errorPhone).show();
                      $("#errorFname").hide();
                      $("#errorSurname").hide(); $("#errorGender").hide();
                      $("#errorLname").hide(); $("#errorRole").hide(); $("#errorEmail").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }

                   else if(data.errorEmail){
                     //handle error
                      $("#errorEmail").text(data.errorEmail).show();
                      $("#errorFname").hide();
                      $("#errorSurname").hide(); $("#errorGender").hide();
                      $("#errorLname").hide(); $("#errorRole").hide(); $("#errorPhone").hide();
                       $("#errorAlert").hide();
                       $("#successAlert").hide();
                 }
                  else if(data.error2){
                     //handle error
                      $("#errorAlert").text(data.error2).show();
                      $("#errorFname").hide();  $("#errorEmail").hide();
                      $("#errorSurname").hide(); $("#errorGender").hide();
                      $("#errorLname").hide(); $("#errorRole").hide(); $("#errorPhone").hide();
                      $("#successAlert").hide();
                 }
                 else {
                    //Handle a success
                      $("#successAlert").text(data.success).show();
                      $("#errorFname").hide();  $("#errorEmail").hide();
                      $("#errorSurname").hide(); $("#errorGender").hide();
                      $("#errorLname").hide(); $("#errorRole").hide(); $("#errorPhone").hide();
                      $("#errorAlert").hide();
                      $("#fname").val(""); $("#lname").val(""); $("#surname").val("");
                      $("#phone").val("");$("#email").val("");
                 }
           });//end done

           event.preventDefault();
      });//end submit
  });//end ready