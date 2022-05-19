$(document).ready(function() {
    user = $('body > p').attr('id')
    var all_classes = $('.students > div');
    classes = Object.assign([], all_classes)
    first_sch = $('.selected_school').attr('id')
    let current_classes;

    /* Load all the percentages once the page loads */
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/api/v1/schools/' + first_sch + '/classrooms',
        dataType: 'json',
        success: function (data) {
            current_classes = data 
        }
    });
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/api/v1/schools/' + first_sch + '/students',
        dataType: 'json',
        success: function (data) {
            for (const [key, stu] of Object.entries(data)) {
                for (const [key, stu_cls] of Object.entries(current_classes)) {
                    if (stu.cls_id === stu_cls.id) {
                        stu_percent = parseInt(stu.fees_paid / stu_cls.fees_expected * 100)
                        $('.student#' + stu.id + ' > .stu_info > .stu_text > h1').html('')
                        $('.student#' + stu.id + ' > .stu_info > .stu_text > h1').html(stu_percent + '%')
                        if (stu_percent > 100) {
                            stu_percent = 100;
                        }
                        $('.student#' + stu.id + ' > .stu_info > .stu_percent_bar > .stu_bar').css('width', stu_percent + '%')
                    }
                }
            }
        }
    });
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/api/v1/users/' + user + '/schools/' + first_sch,
        dataType: 'json',
        success: function (data) {
            for (let key in data) {
                sch_percent = (data[key]).sch_percent
                $('.cls_bar').css('width', sch_percent + '%')
                $('.cls_text > h1').html(sch_percent + '%')
            }
        }
    });


    /* When a school is selected from the dropdowm */
    $('#sch_drop > div > p').on('click', function(event) {
        let new_text = $(this).text()
        let id = $(this).parent().parent().siblings().attr('id');
        sch_id = $(this).attr('id');
        $('#' + id + ' > div').html('<h4 class=selected_school id=' + sch_id + '>' + new_text + '</h4>');
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/api/v1/users/' + user + '/schools/' + sch_id,
            dataType: 'json',
            success: function (data_obj) {
                for (let k in data_obj) {
                    data = data_obj[k]
                }
                sch_text = "<h5>School name: <span>" + data.name + "</span></h5>";
                sch_text += "<h5>School address: <span>" + data.address + "<span></span></h5>";
                sch_text += "<h5 class=current_sch id=" + data.id + ">School ID: <span>" + data.id + "</span></h5>";
                sch_text += "<h5>Level: <span>" + data.level + "</span></h5>";
                sch_text += "<h5>Fees paid: <span>NGN " + data.fees_paid + "</span></h5>";
                sch_text += "<h5>No. of classes: <span>" + data.no_of_classes + "</span></h5>";
                sch_text += "<h5>No. of students: <span>" + data.no_of_students + "</span></h5>";
                sch_text += "<h1>" + data.sch_percent + "%</h1>";
                $('.cls_bar').css('width', data.sch_percent + '%')
                $('.cls_text').html(sch_text);
                $('body > header > .cls_name').html('')
                $('body > header > .cls_name').html(data.name)
                $('body > .cls_addr > p').html(data.address)
                $('.del_edit').html('')
                new_txt = ''
                new_txt += '<div class="del_sch">'
                new_txt += '<p>Delete</p>'
                new_txt += '<form class="signup_input_group hide_cards" id=' + sch_id + 'delete>'
                new_txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin Password" required>'
                new_txt += '<p class="warn">CAREFUL HERE, YOU CANNOT UNDO THIS!</p>'
                new_txt += '<button class="submit_btn" id="del_sch" >Delete school</button><br>'
                new_txt += '</form></div>'
                new_txt += '<div class="edit_sch">'
                new_txt += '<p>Edit</p>'
                sch_name = data.name.replaceAll(' ', '_')
                sch_addr = data.address.replaceAll(' ', '_')
                new_txt +=  '<form class="signup_input_group hide_cards" id=' + data.id + 'edit>'
                new_txt += '<input type="text" class="input_fields" name="name" id="name" required minlength="5" value=' + sch_name + '>'
                new_txt += '<input type="text" class="input_fields" name="address" id="address" required minlength="15" value=' + sch_addr + '>'
                new_txt += '<input type="text" class="input_fields" name="level" id="level" required value=' + data.level + '>'
                new_txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin password" required>'
                new_txt += '<button class="submit_btn" id="edit_sch" >Edit school</button><br>'
                new_txt += '</form></div>'
                $('.del_edit').html(new_txt)
            }
        });
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/classrooms',
            dataType: 'json',
            success: function (data) {
                $('#cls_drop').html('');
                $('#stu_drop').html('');
                txt_stu = '';
                txt_cls = '';
                sch_id = $('.current_sch').attr('id')
                for (let key in data) {
                    if (data['code']) {
                        break;
                    }
                    link = 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/classrooms/' + (data[key]).id,
                    txt_stu += '<div><p class=cl_item id=' + (data[key]).id + '>' + (data[key]).name + '</p></div>'
                    txt_cls += '<div><p class=cl_item id=' + (data[key]).id + '>' + (data[key]).name + '</p></div>'
                }
                $('#cls_drop').html(txt_cls);
                $('#stu_drop').html(txt_stu);
                if (data['code']) {
                    $('#cls_sel > div >h4').html("<p>...</p>");
                    $('#stu_sel > div >h4').html("<p>...</p>");
                }
                else {
                    $('#cls_sel > div >h4').html("<p>Select class</p>");
                    $('#stu_sel > div >h4').html("<p>Select class</p>");
                }
            }
        });
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/students',
            dataType: 'json',
            success: function (data) {
                $('.students').html('')
                if (data['code']) {
                    return
                }
                txt = ''
                console.log(data)
                for (const [key, stu] of Object.entries(data)) {
                    txt += '<div class="student_class" id=' + stu.cls_id
                    txt += '><div class=hide_cards><i class="fas fa-caret-down close_view hide_cards"></i></div>'
                    txt += '<h4 class="student shrink_view" id=' + stu.id + '><p>' + stu.name
                    txt += '</p><div class="stu_info hide_cards">'
                    txt += '<div class="stu_text">'
                    txt += '<h5>Student name: <span>' + stu.name + '</span></h5>'
                    txt += '<h5>Age: <span>' + stu.age + '<span></span></h5>'
                    txt += '<h5>Sex: <span>' + stu.sex + '<span></span></h5>'
                    txt += '<h5>Student ID: <span>' + stu.id + '</span></h5>'
                    txt += '<h5>Class: <span>' + stu.cls + '</span></h5>'
                    txt += '<h5>Fees paid: <span>NGN ' + stu.fees_paid +  '</span></h5>'
                    fees_percent = stu.fees_percent
                    txt += '<h1>' + fees_percent + '%</h1>'
                    txt += '</div>'
                    txt += '<div class="stu_percent_bar">'
                    if (fees_percent > 100) {
                        fees_percent = 100;
                    }
                    txt += '<div style="width:' + fees_percent + '%" class="stu_bar" id=' + stu.id + 'percent></div>'
                    txt += '</div>'
                    txt += '<div class="options" id=' + (stu.name).replace(' ', '_') + '>'
                    txt += '<h5><i class="fas fa-bars"></i></h5>'
                    txt += '</div>'
                    txt += '<div class="del_edit hide_cards">'
                    txt += '<div class="del_obj">'
                    txt += '<p>Delete</p>'
                    txt += '<form class="signup_input_group hide_cards" id=' + stu.id + 'delete>'
                    txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin Password" required>'
                    txt += '<p class="warn">CAREFUL HERE, YOU CANNOT UNDO THIS!</p>'
                    txt += '<button class="submit_btn" id="del_stu" >Delete student</button><br>'
                    txt += '</form></div>'
                    txt += '<div class="edit_obj">'
                    txt += '<p>Edit</p>'
                    txt += '<form class="signup_input_group hide_cards" id=' + stu.id + 'edit>'
                    display_name = (stu.name).replaceAll(' ', '_')
                    txt += '<input type="text" class="input_fields" name="name" id="name" required minlength="5" value=' + display_name + '>'
                    txt += '<input type="text" class="input_fields" name="age" id="age" required value=' + stu.age + '>'
                    txt += '<input type="text" class="input_fields" name="sex" id="sex" required value=' + stu.sex + '>'
                    txt += '<input type="text" class="input_fields" name="parent_phone" id="parent_phone" required minlength="11" value=' + stu.parent_phone + '>'
                    txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin password" required>'
                    txt += '<button class="submit_btn" id="edit_stu" >Edit student</button><br>'
                    txt += '</form></div>'
                    txt += '<div class="add_pay">'
                    txt += '<p>Make payment</p>'
                    txt += '<form class="signup_input_group hide_cards" id=' + stu.id + 'pay>'
                    txt += '<input type="text" class="input_fields" name="payer_name" id="payer_name" placeholder="Payer name" required minlength="5">'
                    txt += '<input type="number" class="input_fields" name="amount" id="amount" placeholder="Amount" required>'
                    txt += '<input type="text" class="input_fields" name="purpose" id="purpose" placeholder="Purpose" required>'
                    txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin password" required>'
                    txt += '<button class="submit_btn" id="add_pay" >Make payment</button><br>'
                    txt += '</form></h4></div></div>'
                }
                $('.students').html(txt);
            }
        })
        classes = Object.assign([], all_classes)
    });

    /* When a classroom is selected from the dropdown to register student*/
    $('body').on('click', '#stu_drop > div > p', function(event) {
        let new_text = $(this).text();
        let id = $(this).parent().parent().siblings().attr('id');
        cls_id = $(this).attr('id');
        $('#' + id + ' > div').html('<h4 class=selected_class id=' + cls_id + '>' + new_text + '</h4>');
    });

    /* When a classroom is selected from the classrooms dropdown */
    $('body').on('click', '#cls_drop > div > p', function(event) {
        cls_id = event.target.id
        sch_id = $('.selected_school').attr('id')
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/classrooms/' + cls_id,
            dataType: 'json',
            success: function (data) {
                for (let key in data) {
                    obj = data[key]
                }
                console.log(obj)
                $('.cls_text').html('');
                new_text = ''
                new_text += '<h5>Class name: <span>' + obj.name + '</span><h5>'
                new_text += '<h5>Class Teacher: <span>' + obj.class_teacher + '</span><h5>'
                new_text += '<h5>Class ID: <span>' + obj.id + '</span><h5>'
                new_text += '<h5>Fees Paid: <span>' + obj.fees_paid + '</span><h5>'
                new_text += '<h5>No. of students: <span>' + obj.no_of_students + '</span><h5>'
                new_text += '<h1>' + obj.fees_percent + '%</h1>'
                $('.cls_bar').css('width', obj.fees_percent + '%')
                $('.cls_text').html(new_text);

                $('.del_edit').html('')
                new_txt = ''
                new_txt += '<div class="del_sch">'
                new_txt += '<p>Delete</p>'
                new_txt += '<form class="signup_input_group hide_cards" id=' + cls_id + 'delete>'
                new_txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin Password" required>'
                new_txt += '<p class="warn">CAREFUL HERE, YOU CANNOT UNDO THIS!</p>'
                new_txt += '<button class="submit_btn" id="del_cls" >Delete class</button><br>'
                new_txt += '</form></div>'
                new_txt += '<div class="edit_sch">'
                new_txt += '<p>Edit</p>'
                cls_name = obj.name.replaceAll(' ', '_')
                cls_teacher = obj.class_teacher.replaceAll(' ', '_')
                new_txt +=  '<form class="signup_input_group hide_cards" id=' + obj.id + 'edit>'
                new_txt += '<input type="text" class="input_fields" name="name" id="name" required minlength="5" value=' + cls_name + '>'
                new_txt += '<input type="text" class="input_fields" name="class_teacher" id="class_teacher" required value=' + cls_teacher + '>'
                new_txt += '<input type="password" class="input_fields" name="password" id="password" placeholder="Admin password" required>'
                new_txt += '<button class="submit_btn" id="edit_cls" >Edit class</button><br>'
                new_txt += '</form></div>'
                $('.del_edit').html(new_txt)

                /*stds = []
                for (let i = 0; i < classes.length; i++) {
                    if (classes[i].id === cls_id) {
                        stds.push(classes[i])
                    }
                }
                $('.students').html('')
                $('.students').html(stds)*/
            }
        });
        let new_text = $(this).text()
        let id = $(this).parent().parent().siblings().attr('id');
        cls_id = $(this).attr('id');
        $('#' + id + ' > div').html('<h4 class=selected_class id=' + cls_id + '>' + new_text + '</h4>');
    });

    /* When the students view is expanded */
    $('.lower_text > h5').on('click', function(event) {
        $('.students').toggleClass('hide_cards show_cards');
        $('#register_student').toggleClass('hide_cards show_cards');
    });

    /* When resister school button is clicked */
    $('#register_school').on('click', function(event) {
        $('.sch_reg_form').toggleClass('hide_cards show_cards');
    });

    /* When register class is clicked */
    $('#register_class').on('click', function(event) {
        $('.class_reg_form').toggleClass('hide_cards show_cards');
    });

    /* When options in each view is clicked (delete/edit buttons) */
    $('body').on('click', '.options', function(event) {
        id = $(this).attr('id')
        console.log(id)
        $('.options#' + id).siblings('.del_edit').toggleClass('hide_cards show_cards');
    });

    $('.cancel_popup').on('click', function() {
        $('.pop_up').toggleClass('hide_cards show_cards');
    });

    /* Register a student */
    $('#register_student').on('click', function() {
        $('.stu_reg_form').toggleClass('hide_cards show_cards')
    });

    /* Get a student view */
    $('body').on('click', '.student', function(event) {
        $(this).removeClass('shrink_view')
        $(this).addClass('expand_view')
        $(this).css('color', 'black')
        const id = $(this).attr('id')
        $('.student#' + id + '> .stu_info').removeClass('hide_cards')
        $('.student#' + id + '> .stu_info').addClass('show_cards')
        $('.student#' + id).siblings().removeClass('hide_cards')
    })

    /* Close student view */
    $('body').on('click', '.close_view', function() {
        id = $(this).parent().siblings().attr('id')
        $('.student#' + id + ' > .stu_info').removeClass('show_cards')
        $('.student#' + id + ' > .stu_info').addClass('hide_cards')
        $('.student#' + id).css('color', 'grey')
        $('.student#' + id).removeClass('expand_view')
        $('.student#' + id).addClass('shrink_view')
        $(this).parent().addClass('hide_cards')
    })

    /* When delete under student is clicked */
    $('body').on('click', '.del_obj > p', function() {
        id = $(this).siblings('form').attr('id')
        console.log(id)
        $('.signup_input_group#' + id).toggleClass('hide_cards show_cards')
    })
    /* When delete student button is clicked */
    $('body').on('click', '.submit_btn#del_stu', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        stu_id = (id.split('delete'))[0]
        const stu_del_form  = document.getElementById(stu_id + 'delete');
        sch_id = $('.selected_school').attr('id')
        console.log(stu_id)
        console.log(sch_id)
        let post_dict = {}
        post_dict['password'] = (stu_del_form.elements['password']).value;
        $.ajax({
            type: 'DELETE',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/students/' + stu_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Deleted') {
                    alert("Student has been deleted successfully")
                    stu_del_form.reset();
                    $('.stu_del_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#stu_del_pop').css('background-color', 'lightcoral')
                    $('#stu_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When edit under student is clicked */
    $('body').on('click', '.edit_obj > p', function() {
        id = $(this).siblings('form').attr('id')
        console.log(id)
        $('.signup_input_group#' + id).toggleClass('hide_cards show_cards')
    })
    /* When edit student button is clicked */
    $('body').on('click', '.submit_btn#edit_stu', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        stu_id = (id.split('edit'))[0]
        const stu_edit_form  = document.getElementById(stu_id + 'edit');
        sch_id = $('.selected_school').attr('id')
        console.log(stu_id)
        console.log(sch_id)
        let post_dict = {}
        post_dict['password'] = (stu_edit_form.elements['password']).value;
        post_dict['name'] = (stu_edit_form.elements['name']).value;
        post_dict['age'] = (stu_edit_form.elements['age']).value;
        post_dict['sex'] = (stu_edit_form.elements['sex']).value;
        post_dict['parent_phone'] = (stu_edit_form.elements['parent_phone']).value;
        $.ajax({
            type: 'PUT',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/students/' + stu_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Updated') {
                    alert("Student has been updated successfully")
                    stu_edit_form.reset();
                    $('.stu_edit_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#stu_del_pop').css('background-color', 'lightcoral')
                    $('#stu_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When pay under student is clicked */
    $('body').on('click', '.add_pay > p', function() {
        id = $(this).siblings('form').attr('id')
        console.log(id)
        $('.signup_input_group#' + id).toggleClass('hide_cards show_cards')
        //$('#delete_student').toggleClass('hide_cards show_cards')
    })
    /* When make payment is clicked is clicked */
    $('body').on('click', '.submit_btn#add_pay', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        stu_id = (id.split('pay'))[0]
        const stu_pay_form  = document.getElementById(stu_id + 'pay');
        sch_id = $('.selected_school').attr('id')
        console.log(stu_id)
        console.log(sch_id)
        let post_dict = {}
        post_dict['payer_name'] = (stu_pay_form.elements['payer_name']).value;
        post_dict['amount'] = (stu_pay_form.elements['amount']).value;
        post_dict['purpose'] = (stu_pay_form.elements['purpose']).value;
        post_dict['student_id'] = stu_id;
        post_dict['password'] = (stu_pay_form.elements['password']).value;
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/students/' + stu_id + '/fees',
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Success') {
                    alert("Payment successful")
                    stu_pay_form.reset();
                    $('.stu_pay_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#stu_del_pop').css('background-color', 'lightcoral')
                    $('#stu_del_pop').toggleClass('hide_cards show_cards');
                }
                else if (data['code'] === 'Invalid credentials') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#stu_del_pop').css('background-color', 'lightcoral')
                    $('#stu_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When delete under student is clicked */
    $('body').on('click', '.del_obj > p', function() {
        id = $(this).siblings('form').attr('id')
        console.log(id)
        $('.signup_input_group#' + id).toggleClass('hide_cards show_cards')
    })
    /* When delete student button is clicked */
    $('body').on('click', '.submit_btn#del_stu', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        stu_id = (id.split('delete'))[0]
        const stu_del_form  = document.getElementById(stu_id + 'delete');
        sch_id = $('.selected_school').attr('id')
        console.log(stu_id)
        console.log(sch_id)
        let post_dict = {}
        post_dict['password'] = (stu_del_form.elements['password']).value;
        $.ajax({
            type: 'DELETE',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/students/' + stu_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Deleted') {
                    alert("Student has been deleted successfully")
                    stu_del_form.reset();
                    $('.stu_del_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#stu_del_pop').css('background-color', 'lightcoral')
                    $('#stu_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When delete under school is clicked */
    $('body').on('click', '.del_sch > p', function() {
        id = $(this).siblings('form').attr('id')
        console.log(id)
        $('.signup_input_group#' + id).toggleClass('hide_cards show_cards')
    })
    /* When delete school button is clicked */
    $('body').on('click', '.submit_btn#del_sch', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        sch_id = (id.split('delete'))[0]
        const sch_del_form  = document.getElementById(sch_id + 'delete');
        console.log(sch_id)
        let post_dict = {}
        post_dict['password'] = (sch_del_form.elements['password']).value;
        $.ajax({
            type: 'DELETE',
            url: 'http://127.0.0.1:5000/api/v1/users/' + user + '/schools/' + sch_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Deleted') {
                    alert("School has been deleted successfully")
                    sch_del_form.reset();
                    $('.sch_del_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#sch_del_pop').css('background-color', 'lightcoral');
                    $('#sch_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When edit under school is clicked */
    $('body').on('click', '.edit_sch > p', function() {
        id = $(this).siblings('form').attr('id')
        console.log(id)
        $('.signup_input_group#' + id).toggleClass('hide_cards show_cards')
    })
    /* When edit school button is clicked */
    $('body').on('click', '.submit_btn#edit_sch', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        sch_id = (id.split('edit'))[0]
        const sch_edit_form  = document.getElementById(sch_id + 'edit');
        console.log(sch_id)
        let post_dict = {}
        post_dict['password'] = (sch_edit_form.elements['password']).value;
        post_dict['name'] = (sch_edit_form.elements['name']).value
        post_dict['address'] = (sch_edit_form.elements['address']).value;
        post_dict['level'] = (sch_edit_form.elements['level']).value;
        $.ajax({
            type: 'PUT',
            url: 'http://127.0.0.1:5000/api/v1/users/' + user + '/schools/' + sch_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Updated') {
                    alert("School has been updated successfully")
                    sch_edit_form.reset();
                    $('.sch_edit_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#sch_del_pop').css('background-color', 'lightcoral')
                    $('#sch_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When delete class button is clicked */
    $('body').on('click', '.submit_btn#del_cls', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        cls_id = (id.split('delete'))[0]
        sch_id = $('.selected_school').attr('id')
        const cls_del_form  = document.getElementById(cls_id + 'delete');
        console.log(cls_id)
        let post_dict = {}
        post_dict['password'] = (cls_del_form.elements['password']).value;
        $.ajax({
            type: 'DELETE',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/classrooms/' + cls_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Deleted') {
                    alert("Class has been deleted successfully")
                    cls_del_form.reset();
                    $('.cls_del_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#cls_del_pop').css('background-color', 'lightcoral');
                    $('#cls_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });
    /* When edit class button is clicked */
    $('body').on('click', '.submit_btn#edit_cls', function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        cls_id = (id.split('edit'))[0]
        sch_id = $('.selected_school').attr('id')
        const cls_edit_form  = document.getElementById(cls_id + 'edit');
        console.log(cls_id)
        let post_dict = {}
        post_dict['password'] = (cls_edit_form.elements['password']).value;
        post_dict['name'] = (cls_edit_form.elements['name']).value
        post_dict['class_teacher'] = (cls_edit_form.elements['class_teacher']).value;
        $.ajax({
            type: 'PUT',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/classrooms/' + cls_id,
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Updated') {
                    alert("Classroom has been updated successfully")
                    cls_edit_form.reset();
                    $('.cls_edit_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#cls_del_pop').css('background-color', 'lightcoral')
                    $('#cls_del_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When a new school is created */
    const sch_reg_form  = document.getElementById('new_school');
    sch_reg_form.addEventListener('submit', (event) => {
        event.preventDefault()
        const name = (sch_reg_form.elements['name']).value;
        const address = (sch_reg_form.elements['address']).value;
        const level = (sch_reg_form.elements['level']).value;
        const pwd = (sch_reg_form.elements['password']).value;
        const user_id = (sch_reg_form.elements['user_id']).value;
        let post_dict = {}
        post_dict['name'] = name
        post_dict['address'] = address
        post_dict['level'] = level
        post_dict['password'] = pwd
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/users/' + user_id + '/schools',
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'School created') {
                    alert("School created!")
                    sch_reg_form.reset();
                    $('.sch_reg_form').toggleClass('hide_cards show_cards');
                    setTimeout("location.reload(true);",1500);
                }
                else if (data['code'] === 'School exists') {
                    $('.message').html('<p>School with that name exists already!</p>');
                    $('#sch_form_pop').css('background-color', 'lightcoral')
                    $('#sch_form_pop').toggleClass('hide_cards show_cards');
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#sch_form_pop').css('background-color', 'lightcoral')
                    $('#sch_form_pop').toggleClass('hide_cards show_cards');
                }
                else {
                    $('.message').html('<p>Unknown error</p>');
                    $('#sch_form_pop').css('background-color', 'lightcoral')
                    $('#sch_form_pop').toggleClass('hide_cards show_cards');
                }
            }
        });
    });

    /* When a new class is created */
    const cls_reg_form  = document.getElementById('new_class');
    cls_reg_form.addEventListener('submit', (event) => {
        event.preventDefault()
        const name = (cls_reg_form.elements['name']).value;
        const class_teacher = (cls_reg_form.elements['class_teacher']).value;
        const fees_expected = (cls_reg_form.elements['fees_expected']).value;
        const pwd = (cls_reg_form.elements['password']).value;
        
        const sch_id = $('.current_sch').attr('id')
        console.log(sch_id)
        let post_dict = {}
        post_dict['name'] = name
        post_dict['class_teacher'] = class_teacher
        post_dict['fees_expected'] = fees_expected
        post_dict['password'] = pwd
        post_dict['sch_id'] = sch_id
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/classrooms',
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Created') {
                    alert("Class added!")
                    cls_reg_form.reset()
                    $('.class_reg_form').toggleClass('hide_cards show_cards')
                    setTimeout("location.reload(true);", 1500);
                }
                else if (data['code'] === 'Class exists') {
                    $('.message').html('<p>Class with that name exists already!</p>');
                    $('#cls_form_pop').css('background-color', 'lightcoral')
                    $('#cls_form_pop').toggleClass('hide_cards show_cards');
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#cls_form_pop').css('background-color', 'lightcoral')
                    $('#cls_form_pop').toggleClass('hide_cards show_cards');
                }
                else {
                    $('.message').html('<p>Unknown error</p>');
                    $('#cls_form_pop').css('background-color', 'lightcoral')
                    $('#cls_form_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });

    /* When a new student is created */
    const stu_reg_form  = document.getElementById('new_student');
    stu_reg_form.addEventListener('submit', (event) => {
        event.preventDefault()
        const name = (stu_reg_form.elements['name']).value;
        const age = (stu_reg_form.elements['age']).value;
        const sex = (stu_reg_form.elements['sex']).value;
        const parent_phone = (stu_reg_form.elements['parent_phone']).value
        const pwd = (stu_reg_form.elements['password']).value;
        
        const sch_id = $('.selected_school').attr('id')
        const cls = $('#stu_sel > div > h4').text()
        const cls_id = $('#stu_sel > div > h4').attr('id')
        console.log(cls)
        console.log(cls_id)
        let post_dict = {}
        post_dict['name'] = name
        post_dict['age'] = age
        post_dict['sex'] = sex
        post_dict['parent_phone'] = parent_phone
        post_dict['cls_id'] = cls_id
        post_dict['cls'] = cls
        post_dict['password'] = pwd
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/schools/' + sch_id + '/students',
            data: JSON.stringify(post_dict),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data['code'] === 'Created') {
                    alert("Student added!")
                    stu_reg_form.reset()
                    $('.stu_reg_form').toggleClass('hide_cards show_cards')
                    setTimeout("location.reload(true);", 1500);
                }
                else if (data['code'] === 'Student exists') {
                    $('.message').html('<p>Student with that name exists already!</p>');
                    $('#stu_form_pop').css('background-color', 'lightcoral')
                    $('#stu_form_pop').toggleClass('hide_cards show_cards');
                }
                else if (data['code'] === 'Wrong password') {
                    $('.message').html('<p>Wrong password!</p>');
                    $('#stu_form_pop').css('background-color', 'lightcoral')
                    $('#stu_form_pop').toggleClass('hide_cards show_cards');
                }
                else {
                    $('.message').html('<p>Unknown error</p>');
                    $('#stu_form_pop').css('background-color', 'lightcoral')
                    $('#stu_form_pop').toggleClass('hide_cards show_cards');
                }
                console.log(data['code'])
            }
        });
    });
});