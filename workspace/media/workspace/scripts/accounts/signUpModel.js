var SignUpModel = Backbone.Model.extend({

	validation: {

		account_name: {
			required: true,
			pattern: /^[a-zA-Z0-9\-]+$/,
			msg: gettext('APP-ACCOUNT-NAME-NOT-VALID')
		},

		admin_url: [{
			required: true,
			msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
		},{
			pattern: /^[a-zA-Z0-9\-]+$/,
			msg: gettext( 'VALIDATE-REGEX' )
		},{
			maxLength: 30,
			msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 30 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
		}],

		nick: [{
			required: true,
			msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
		},{
			pattern: /^[a-zA-Z0-9\_\.\-]+$/,
			msg: gettext( 'VALIDATE-REGEX' )
		},{
			maxLength: 30,
			msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 30 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
		}],

		name: [{
			required: true,
			msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
		},{
			maxLength: 30,
			msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 30 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
		}],

		password: {
			required: true,
			msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
		},

		password_again: {
			equalTo: 'password',
			msg: gettext('VALIDATE-PASSWORDMATCH-TEXT')
		},

		email: [{
			required: true,
			msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
		},{
			pattern: 'email',
			msg: gettext('VALIDATE-EMAILNOTVALID-TEXT')
		},{
			maxLength: 75,
			msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 75 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
		}]

	},

	ifAdminUrlExists: function() {
		var url = '/accounts/check_admin_url/';
		var msg = false;
		var data = { csrfmiddlewaretoken: csrfmiddlewaretoken }
		data['admin_url'] = this.get('admin_url');
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			dataType: 'json',
			async: false,
			success: function(response){
				if( !response ){
					msg = gettext( 'VALIDATE-ADMIN-URL' );
				}
			}
		});
		return msg;
	},

	ifNickExists: function() {
		var url = '/admin/check_username/';
		var msg = false;
		var data = { csrfmiddlewaretoken: csrfmiddlewaretoken }
		data['nick'] = this.get('nick');
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			dataType: 'json',
			async: false,
			success: function(response){
				if( !response ){
					msg = gettext( 'VALIDATE-USERNAME' );
				}
			}
		});
		return msg;
	},

	ifEmailExists: function() {
		var url = '/admin/check_email/';
		var msg = false;
		var data = { csrfmiddlewaretoken: csrfmiddlewaretoken }
		data['email'] = this.get('email');
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			dataType: 'json',
			async: false,
			success: function(response){
				if( !response){
					msg = gettext( 'VALIDATE-EMAIL' );
				}
			}
		});
		return msg;
	}

});
