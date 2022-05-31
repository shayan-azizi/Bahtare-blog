function validate(){


    let csrf_token = document.getElementsByName("csrf_token")[0].value;



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
           url : "/validation123",
           success : function(response){
                

                username_error = response["username_error"];
                password_error = response["password_error"];

                document.getElementById("username_error").innerHTML = username_error;
                

                
                document.getElementById("password_error").innerHTML = password_error;
                
                
                
                

           }

       });
  }
