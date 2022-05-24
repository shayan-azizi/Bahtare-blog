function activeSignIn () {
    let signInButton = document.getElementById("s-in")
    let signUpButton = document.getElementById("s-up")

    signInButton.classList.remove("unactive")
    signInButton.classList.add("active")
    signUpButton.classList.remove("active")
    signUpButton.classList.add("unactive")
    
    let submitBtn = document.getElementsByClassName ("submitbtn")
    submitBtn.value = "ورود"


    let doYouHaveAcc = document.getElementsByClassName("signupbtn")
    doYouHaveAcc.value = "الان ثبت نام کن!"

    let parentDoYouHaveAcc = document.getElementById("parent-acc")
    parentDoYouHaveAcc.value = "اکانت نداری؟"

}

function activeSignUp () {
    let signInButton = document.getElementById("s-in")
    let signUpButton = document.getElementById("s-up")
    signInButton.classList.remove("active")
    signInButton.classList.add("unactive")
    signUpButton.classList.remove("unactive")
    signUpButton.classList.add("active")

    let submitBtn = document.getElementsByClassName ("submitbtn")
    submitBtn.value = "ثبت نام"


    let doYouHaveAcc = document.getElementsByClassName("signupbtn")
    doYouHaveAcc.value = "الان ورود کن!"

    let parentDoYouHaveAcc = document.getElementById("parent-acc")
    parentDoYouHaveAcc.value = "اکانت داری؟"

}

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