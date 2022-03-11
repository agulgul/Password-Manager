const pwFields = document.querySelectorAll(".password");
const submitbtn = document.querySelector('.submitbtn');
const pwShowHide = document.querySelectorAll(".showHidePw");
const myVar = document.querySelectorAll("#myVar");

pwShowHide.forEach(eyeIcon =>{
    eyeIcon.addEventListener("click", ()=>{
        var data = '{{vault|escapejs}}';
        
      pwFields.forEach(pwField =>{
          if(pwField.type ==="password"){
                pwField.type = "text";
                console.log(data);
                
                pwShowHide.forEach(icon =>{
                    icon.classList.replace("uil-eye-slash", "uil-eye");
                })
            }else{
                pwField.type = "password";
  
                pwShowHide.forEach(icon =>{
                    icon.classList.replace("uil-eye", "uil-eye-slash");
                })
            }
        }) 
    })
  })
