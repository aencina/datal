$(document).ready(function(){

    // OVERLAY
    $formContainer = $('#id_userFormContainer');
    $formContainer.overlay({ top: 'center', left: 'center', mask: {color: '#000', loadSpeed: 200, opacity: 0.5, zIndex: 99999}, closeOnClick: false, closeOnEsc: true, load: false});

    $form = $('#id_userForm');

    // EDIT
    $('#id_usersTable .edit a').click(function(event){
        event.preventDefault();
        var $tr = $(this).parents('tr');
        var id = $tr.attr('data-id');
        var name = $tr.find('span.name').html();
        var username = $tr.find('td.username').html();
        var email = $tr.attr('data-email');
        var role = $tr.attr('data-role');
        $form.find('#id_id').val(id);
        $form.find('#id_name').val(name);
        $form.find('#id_username').val(username);
        $form.find('#id_email').val(email);
        $form.find('#id_confirm_email').val(email);
        $form.find('#id_role').val(role);
        $form.attr('action', '/admin/edit_user/');
        $formContainer.data('overlay').load();
    });

    // CREATE
    $('#id_create_user').click(function(event){
        event.preventDefault();
        $form.find('#id_id').val('');
        $form.find('#id_name').val('');
        $form.find('#id_username').val('');
        $form.find('#id_email').val('');
        $form.find('#id_confirm_email').val('');
        $form.find('#id_role').val('');
        $form.attr('action', '/admin/create_user/');

        $formContainer.data('overlay').load();
    });

    $form.validate({
        rules: {
                name: { required: true },
                username: { 
                    required: true,
                    regex: /^[a-zA-Z0-9\_\.\-]+$/,
                    maxlength: 30,
                    remote: { 
                        url: '/admin/check_username/',
                        type: 'post',
                        data: {
                                csrfmiddlewaretoken: csrfmiddlewaretoken,
                                user_id: function(){ return $('#id_id').val() }
                              }
                    }
                   },
                email: {
                    required: true,
                    email: true,
                    maxlength: 75,
                    remote: {
                        url: '/admin/check_email/',
                        type: 'post',
                        data: {
                                csrfmiddlewaretoken: csrfmiddlewaretoken,
                                user_id: function(){ return $('#id_id').val() }
                              }
                    }
                   },
                confirm_email: { equalTo: '#id_email'},
                password: {required: true},
                confirm_password: { equalTo: '#id_password'},
                role: { required: true }
          },
          messages: {
            username: {
               remote: gettext( "VALIDATE-USERNAME" ),
               regex: gettext( "VALIDATE-REGEX" )
             },
             email: {
               remote: gettext( "VALIDATE-EMAIL" )
             }
           },
        submitHandler: function(form){
            $form = $(form);
            $('#ajax_loading_overlay').show();
            $.ajax({
                url: $form.attr('action'),
                data: $form.serialize(),
                type: $form.attr('method'),
                success: function(response){

                    var messages = response.messages;
                        status = response.status,
                        title = gettext('APP-SETTINGS-SAVE-OK-TITLE'),
                        imageURL = '/static/workspace/images/common/ic_validationOk32.png';

                    if( _.isArray(messages) ){
                        messages = messages.join('. ');
                    }

                    if(status == 'error'){
                        title = 'Error';
                        imageURL = '/static/workspace/images/common/ic_validationError32.png';
                    }

                    // Notification
                    $.gritter.add({ title: title, text: messages, image: imageURL, sticky: true });

                    if(status == 'ok'){
                        if (undefined !== response.redirect)
                            {window.location = response.redirect;}
                        else{
                            $('#gritter-notice-wrapper').css({'z-index': 100000001});
                            $('#ajax_loading_overlay').show();
                            
                            setTimeout(function(){ window.location.reload(true); }, 2000);
                            }
                    }

                },
                error: function(response){
                    var response = JSON.parse(response.responseText),
                        messages = response.messages;

                    if( _.isArray(messages) ){
                        messages = messages.join('. ');
                    }

                    // Notification
                    $.gritter.add({
                        title: 'Error',
                        text: messages,
                        image: '/static/workspace/images/common/ic_validationError32.png',
                        sticky: true,
                        time: 2500
                    });
                },
                complete: function(){
                    $formContainer.data('overlay').close();
                    $('#ajax_loading_overlay').hide();
                }
            });
            return false;
        }
    });
});
