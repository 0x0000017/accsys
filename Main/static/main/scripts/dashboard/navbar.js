
//Menu Toggle
let toggle = document.querySelector('.toggle');
let navigation = document.querySelector('.sideNavigation');
let main = document.querySelector('.main');
let topbar = document.querySelector('.topbar');

toggle.onclick = function(){
    navigation.classList.toggle('active');
    main.classList.toggle('active');
    topbar.classList.toggle('active');
}


// add hovered class in selected list item 
let list = document.querySelectorAll('.sideNavigation li');
function activeLink(){
    list.forEach((item) => 
        item.classList.remove('hovered')
    );
    this.classList.add('hovered');
}
list.forEach((item)=>
    item.addEventListener('mouseover', activeLink)
);