  $(document).ready(function(){
      $("#driverForm").on("submit", function(event){
           $("#success").text("Please wait.. Uploading Data").show();

           var form_data = new FormData();
           form_data.append("files[]", document.getElementById("passport_pic").files[0])
           form_data.append("fname", $("#fname").val())
           form_data.append("lname", $("#lname").val())
           form_data.append("surname", $("#surname").val())
           form_data.append("phone", $("#phone").val())
           form_data.append("email" , $("#email").val())
           form_data.append("dl_no", $("#dl_no").val())
           form_data.append("dl_no_expiry", $("#dl_no_expiry").val())
           form_data.append("loc_id", $("#loc_id").val())
           form_data.append("dob", $("#dob").val())
           $.ajax({
                 data: form_data,
                 type: 'POST',
                 url:"/addDriver",
                 cache: false,
                 contentType: false,
                 processData: false
           })//end ajax
           //Wait for response from Python without reloading Page
           .done(function(data){
                 if(data.error){
                      //handle error
                      $("#error").text(data.error).show();
                      $("#error2").hide();
                      $("#success").hide();
                 }
                 else if(data.error2){
                     //handle error
                      $("#error2").text(data.error2).show();
                      $("#error").hide();
                      $("#success").hide();
                 }
                 else {
                    //Handle a success
                      $("#success").text(data.success).show();
                      $("#error2").hide();
                      $("#error").hide();
                 }
           });//end done
           event.preventDefault();
      });//end submit
  });//end ready