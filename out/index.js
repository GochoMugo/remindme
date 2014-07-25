// Affix
$('#navigation ul').affix({
    offset: {
        top: $('#top').height(true),
        bottom: $("body footer").height(true) + 100
    }
});
