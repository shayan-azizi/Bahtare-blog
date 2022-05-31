function validate(){
    let csrf_token = "{{ csrf_token() }}";
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value; 

     $.ajax({
          
           type : "POST",
           headers : {
             "X-CSRFToken" : csrf_token,
           },
           data : {
             "username" : username,
             "password" : password,
           },
           url : "{{ url_for('validation_endpoint') }}",
           success : function(response){
                error = response["error"]
                
                if (error != ""){
                  console.log(error);
                }
           }

       });
  }
