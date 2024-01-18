function lastMessageScroll(b) {
    var e = document.querySelector('.wrapper_Scrollbottom');
    if (!e) return ; 
    
    e.scrollIntoView({
        behavior: b || 'auto',
        block: 'end',
    });
}