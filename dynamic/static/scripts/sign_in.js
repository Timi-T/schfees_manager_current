$(document).ready(function () {
    $('.toggle_btn').on('click', function() {
        $(this).removeClass('other').siblings().addClass('other');
        if ($(this).attr('id') === 'signup_btn') {
            $('.login_input_group').css('display', 'none');
            $('.signup_input_group').css('display', 'flex');
            $('.right_container').css('height', '60%');
            $('#signup_click').css('display', 'block');
        }
        else {
            $('.login_input_group').css('display', 'flex');
            $('.signup_input_group').css('display', 'none');
            $('#signup_click').css('display', 'none');
            $('.right_container').css('height', '50%');
        }
    });

    const signup_form = document.getElementsByClassName('signup_input_group')
    $('#signup_click').on('click', function(){
        password = (signup_form[0][3]).value
        confirm_pwd = (signup_form[0][4]).value
        if (password != confirm_pwd) {
            (signup_form[0][3]).value = ''
            (signup_form[0][4]).value = ''
        }
        full_name = (signup_form[0][0]).value
        email = (signup_form[0][1]).value
        phone_no = (signup_form[0][2]).value
        password = (signup_form[0][3]).value
        confirm_pwd = (signup_form[0][4]).value
        signup_info = {}
        signup_info['name'] = full_name
        signup_info['email'] = email
        signup_info['phone_no'] = phone_no
        signup_info['password'] = password
    })

    login_form = document.getElementsByClassName('login_input_group')
    $('#login_click').on('click', function() {
        email = login_form[0][0].value
        password = login_form[0][1].value
        const login_info = {}
        login_info['email'] = email
        login_info['password'] = password
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/login',
            data: login_info,
            dataType: 'json',
            contentType: 'application/json',
            success: function () {
                window.location.assign("http://127.0.0.1:5000/api/v1/users");
            }
        });
        window.location.assign("http://127.0.0.1:5000/api/v1/login");
    });
});