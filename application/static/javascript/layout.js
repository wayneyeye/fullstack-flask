document.addEventListener("DOMContentLoaded", function(event) {

    const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)
    
    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
    toggle.addEventListener('click', ()=>{
    // show navbar
    nav.classList.toggle('show')
    // change icon
    toggle.classList.toggle('bx-x')
    // add padding to body
    bodypd.classList.toggle('body-pd')
    // add padding to header
    headerpd.classList.toggle('body-pd')
    if (headerpd.classList.contains('body-pd')){
        if (typeof(Storage) !== "undefined") {
            // Save the state of the sidebar as "open"
            localStorage.setItem("sidebar", "opened");
            //console.log("Storage set sidebar to open ")
        }
    }
    else{
        if (typeof(Storage) !== "undefined") {
            // Save the state of the sidebar as "open"
            localStorage.setItem("sidebar", "closed");
            //console.log("Storage set sidebar to closed ")
        }
    }
    })
    }
    }
    
    showNavbar('header-toggle','nav-bar','body-pd','header')
    
    const div = document.getElementById('header-toggle');
    
    function openNav(toggleId, navId, bodyId, headerId) {
        const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId)
        // If localStorage is supported by the browser
        if (typeof(Storage) !== "undefined") {
            // Save the state of the sidebar as "open"
            localStorage.setItem("sidebar", "opened");
            //console.log("Storage set sidebar to open ")
        }
        // if no show then toggle else do nothing
        if(!div.classList.contains('bx-x')){
            nav.classList.toggle('show')
            // change icon
            toggle.classList.toggle('bx-x')
            // add padding to body
            bodypd.classList.toggle('body-pd')
            // add padding to header
            headerpd.classList.toggle('body-pd')
        }  
    }
    
    function closeNav(toggleId, navId, bodyId, headerId) {
        const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId)
        // If localStorage is supported by the browser
        if (typeof(Storage) !== "undefined") {
            // Save the state of the sidebar as "open"
            localStorage.setItem("sidebar", "closed");
        }
        if(div.classList.contains('bx-x')){
            nav.classList.toggle('show')
            // change icon
            toggle.classList.toggle('bx-x')
            // add padding to body
            bodypd.classList.toggle('body-pd')
            // add padding to header
            headerpd.classList.toggle('body-pd')
        } 
    }
    //openNav('header-toggle','nav-bar','body-pd','header')
    
    if(localStorage.getItem("sidebar") == "opened"){
        if(!div.classList.contains('bx-x')){
            openNav('header-toggle','nav-bar','body-pd','header')
        }
    }
    else{
        if(div.classList.contains('bx-x')){
            closeNav('header-toggle','nav-bar','body-pd','header')
        }
    }
    
    
    
    
    /*===== LINK ACTIVE =====*/
    // const linkColor = document.querySelectorAll('.nav_link')
    
    // function colorLink(){
    // if(linkColor){
    // linkColor.forEach(l=> l.classList.remove('active'))
    // this.classList.add('active')
    // }
    // }
    // linkColor.forEach(l=> l.addEventListener('click', colorLink))
    
    // Your code to run since DOM is loaded and ready
    });