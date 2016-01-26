var SharePrivateOverlay = Backbone.Model.extend({

    defaults: {
        $Container: null
        , $Button: null
        , $AddEmailSelect: null
        , $AddEmailButton: null
        , codeTemplate: null
        , $ColaboratorsContainer: null
        , $Form: null
        , $SaveButton: null
    }

    , initialize: function(){

        var att = this.attributes;
        att.$AddEmailSelect = att.$Container.find('#id_private_share_form_collaborators_addEmail');
        att.$AddEmailButton = att.$Container.find('#id_private_share_form_collaborators_addEmailButton');
        att.$AddRoleSelect = $('#id_private_share_form_collaborators_addRole');
        att.$ColaboratorsContainer = att.$Container.find('.colaboratorsContainer');
        att.$SaveButton = att.$Container.find('#id_private_share_form_collaborators_saveButton');

        att.$ColaboratorsContainer.find('.collaborator').each(function(){
            $(this).attr('id', $(this).attr('data-email').replace(/[\.\@]/g, '_').toLowerCase());
        });

        att.$Button.click(_.bind(this.display, this));
        att.$Container.overlay({ top: 'center'
                                , left: 'center'
                                , mask: {
                                    color: '#000'
                                    , loadSpeed: 200
                                    , opacity: 0.5
                                    , zIndex: 99999
                                 }
                                 , closeOnClick: false
                                 , closeOnEsc: true
                                 , load: false
                              });
        att.$AddEmailButton.click(_.bind(this.addEmail, this));

        att.$Form.validate({
            rules: {
              'private_share_form_collaborators_addEmail': {'email': true, 'required': true}
            }
            , onsubmit: false
        });

        att.$ColaboratorsContainer.find('.icClose').click(_.bind(this.removeCollaborator, this));
        att.$SaveButton.click(_.bind(this.save, this));

        _.templateSettings = {
            interpolate : /\{\{(.+?)\}\}/g
        };

        var template = '<li id="{{id}}" class="email clearfix collaborator" data-email="{{email}}">' +
                            '<div class="img FL clearfix">' +
                                '<img src="{{image_url}}" title="{{email}}" class="FL" />' +
                            '</div>' +
                            '<p class="FL">{{nick}}</p>' +
                            '<a href="javascript:;" title="'+gettext('OVPRIV-REMOVEUSER-TEXT')+'" class="icClose FR">'+gettext('OVPRIV-REMOVEUSER-TEXT')+'</a>' +
                             '<select name="role" class="FR selectField">' +
                                '<option value="ao-viewer">'+gettext('OVPRIV-CANVIEW-TEXT')+'</option>' +
                                '<option value="ao-user">'+gettext('OVPRIV-CANUSE-TEXT')+'</option>' +
                            '</select>' +
                       '</li>';
        att.codeTemplate = _.template(template);
    }

    , display: function(pEvent) {
        this.beforeDisplay();
        this.attributes.$Container.data('overlay').load();
    }

    , close: function(pEvent) {
        this.attributes.$Container.data('overlay').close();
    }

    , addEmail: function(pEvent) {
        var att = this.attributes;
        var email = att.$AddEmailSelect.val();
        if (att.$Form.valid()) {
            this.addCollaborator(email);
        }
    }

    , addCollaborator: function (email) {
        var att = this.attributes;
        var $collaborator = att.$ColaboratorsContainer.find('#' + this.computeCollaboratorId(email));
        if ($collaborator.size() == 0) {
            $.ajax({
                url: '/auth/get_email_info/'
                , data: { email: email }
                , success: _.bind(function(response) {
                    var att = this.attributes;
                    response.id = this.computeCollaboratorId(response.email);
                    response.nick = att.$AddEmailSelect.find('option[value="'+response.email+'"]').html();
                    response.role = att.$AddRoleSelect.val();
                    var html = att.codeTemplate(response)
                    var $html = $(html);
                    $html.find('select option[value='+response.role+']').attr('selected', 'selected');
                    att.$AddEmailSelect.find('option[value="'+response.email+'"]').remove();
                    att.$ColaboratorsContainer.prepend($html);
                    att.$ColaboratorsContainer.animate({scrollTop:0}, 'fast');
                    // @XXX: live doesnt works with underscore, wtf!
                    att.$ColaboratorsContainer.find('.icClose').unbind('click').click(_.bind(this.removeCollaborator, this));
                }, this)
            });
        }
    }

    , computeCollaboratorId: function(email) {
        return email.replace(/[\.\@]/g, '_').toLowerCase();
    }

    , removeCollaborator: function (event) {
        $(event.target).parent('.collaborator').fadeOut(function(){ 
            var email = $(this).attr('data-email');
            var nick = $(this).find('p.FL').html();
            $(this).remove();
            var option = '<option value="'+email+'">'+nick+'</value>';
            $('#id_private_share_form_collaborators_addEmail').append(option);
        });
    }

    , save: function(event) {
        event.preventDefault();
        var att = this.attributes;
        att.$AddEmailButton.attr('disabled', 'disabled');
        att.$AddEmailSelect.attr('disabled', 'disabled');
        att.$AddRoleSelect.attr('disabled', 'disabled');
        var $collaborators = att.$ColaboratorsContainer.find('.collaborator');
        att.$Form.find('#id_private_share_form_collaborators-TOTAL_FORMS').val($collaborators.size());
        $collaborators.each(function(index){
            $(this).find('select').attr('disabled', 'disabled');
        });
        var data = att.$Form.serialize();

        $('.collaborator').each(function(index){
            var email = $(this).attr('data-email');
            collaborator = {};
            collaborator['private_share_form_collaborators-' + index + '-email'] = email;
            collaborator['private_share_form_collaborators-' + index + '-role'] = $(this).find('select').val();
            data += '&' + $.param(collaborator);
        });

        att.$AddEmailButton.removeAttr('disabled');
        att.$AddEmailSelect.removeAttr('disabled');
        att.$AddRoleSelect.removeAttr('disabled');
        $collaborators.each(function(index){
            $(this).find('select').removeAttr('disabled');
        });

        var url = att.$Form.attr('action');
        var method = att.$Form.attr('method');

        $.ajax({
            url: url
            , type: method
            , data: data
            , success: _.bind(function(response) {
                var att = this.attributes;
                $.TwitterMessage({message: response.pMessage, type: 'success'});
                this.close();
            }, this)
            , error: function(response) {
                response = JSON.parse(response.response);
                $.TwitterMessage({'message': response.pMessage, 'type': 'error'});
            }
        });
    }

    , beforeDisplay: function() {
    }

});
