$(document).ready(function() {
    $('.dropdown > p').on('click', function(event) {
        let new_text = $(this).text()
        let id = $(this).parent().siblings().attr('id');
        console.log(id);
        $('.selector#' + id).html('<h4>' + new_text + '</h4>');
    });
    $('.lower_text > h2').on('click', function(event) {
        $('.students').toggleClass('hide_cards show_cards');
    })
});