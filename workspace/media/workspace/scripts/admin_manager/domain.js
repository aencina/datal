$(document).ready(function(){
    domain_regex = /^[a-zA-Z0-9\_\.\-]+$/;

    $.validator.addMethod("prevent_api_internal", function(value, element) {
      domain_internal = $('#id_account_domain_internal').val();
      if ((domain_internal.substring(0, 4)) == "api."){
        return false;
      }else{
        return true;
      };
    });

    $.validator.addMethod("prevent_api_external", function(value, element) {
      domain_external = $('#id_account_domain_external').val();
      if ((domain_external.substring(0, 4)) == "api."){
        return false;
      }else{
        return true;
      };
    });

    $form = $('#id_adminDomainForm');
    $form.validate({
      rules: {
        account_domain_internal: {
            regex: domain_regex,
            prevent_api_internal: true,
            remote: {
                  url: '/admin/check_domain/',
                  type: 'post',
                  data: {
                          csrfmiddlewaretoken: csrfmiddlewaretoken,
                          domain: function(){
                              return $('#id_account_domain_internal').val() + $('#id_defaultDomain').html();
                          }
                        }
            }
        },
        account_domain_external: {
            regex: domain_regex,
            prevent_api_external: true,
            remote: {
                  url: '/admin/check_domain/',
                  type: 'post',
                  data: {
                          csrfmiddlewaretoken: csrfmiddlewaretoken,
                          domain: function(){
                              return $('#id_account_domain_external').val();
                          }
                        }
            }
        }
      },
      messages:{
        account_domain_internal: { regex: gettext( "VALIDATE-REGEX" ), remote: gettext( "VALIDATE-DOMAIN" ), prevent_api_internal: gettext( "APP-NOT-API-DOMAIN-TEXT") },
        account_domain_external: { regex: gettext( "VALIDATE-REGEX" ), remote: gettext( "VALIDATE-DOMAIN" ), prevent_api_external: gettext( "APP-NOT-API-DOMAIN-TEXT") }
      },
      submitHandler: function(form){

        if(!confirm(gettext('APP-AREYOUSURE-TEXT'))) {
            return false;
        }

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
                imageURL = '/static/workspace/images/common/ic_validationOk32.png',
                sticky = false,
                time = 3500;

            if( _.isArray(messages) ){
                messages = messages.join('. ');
            }

            if(status == 'error'){
                title = 'Error';
                imageURL = '/static/workspace/images/common/ic_validationError32.png';
                sticky = true;
                time = 2500;
            }

            // Notification
            $.gritter.add({
                title: title,
                text: messages,
                image: imageURL,
                sticky: sticky,
                time: time
            });

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
              $('#ajax_loading_overlay').hide();
          }
        });
        return false;
      }
    });

    $('#id_account_domain_internal').EnableDisable({
      enabler: '[name=pick_a_domain][value=internal]',
      on_disable: function() {
          $('#id_account_domain_internal').val('');
          $('#id_account_domain_internal').next().hide();
      }
    });

    $('#id_account_domain_external').EnableDisable({
      enabler: '[name=pick_a_domain][value=external]',
      on_disable: function() {
          $('#id_account_domain_external').val('');
          $('#id_account_domain_external').next().hide();
      }
    });

    $('#id_account_domain_internal, #id_account_domain_external').keyup(function(){
        if ($(this).val().match(domain_regex)) {
            if ($(this).is('#id_account_domain_internal')) {
                var domain = $(this).val() + $('#id_defaultDomain').html();
                var apiDomain = $(this).val() + '.cloudapi.junar.com';
                // if in the future we use subdomains for transparency microsites var transparencyDomain = $(this).val() + '.' + gettext( "TRANSPARENCY-PREFIX" ) + '.junar.com';
            } else {
                var domain = $(this).val();
                var apiDomain = 'api.' + domain;
                // if in the future we use subdomains for transparency microsites var transparencyDomain = gettext( "TRANSPARENCY-PREFIX" ) + '.' + domain;
            }

            $('#id_account_domain').val(domain);

            $('#id_apiDomain').html(apiDomain);
            $('#id_account_api_domain').val(apiDomain);

            // if in the future we use subdomains for transparency microsites  $('#id_transparencyDomain').html(transparencyDomain);
            // if in the future we use subdomains for transparency microsites  $('#id_account_transparency_domain').val(transparencyDomain);

        }
    });
});
