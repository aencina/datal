var AddSourceModel = Backbone.Model.extend({

	defaults: {
		name: "",
		url: ""
	},

	validation: {
		name: [
			{
				required: true,
				msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
			},{
				maxLength: 40,
				msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 40 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
			}
		],
		url: [
			{
				required: true,
				msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
			},{
				pattern: /^(?:(ht|f|sf)tp(s?)\:\/\/)/,
				msg: gettext('VALIDATE-PROTOCOLNOTALLOWED-TEXT')
			},{
				pattern: 'url',
				msg: gettext('VALIDATE-URLNOTVALID-TEXT')
			}
		]
	},

	validateSourceNameAlreadyExist: function() {
		var url = '/rest/sources.json/',
			data = {},
			msg = false;
		data['name'] = this.get('name');
		$.ajax({
			url: url,
			type: 'GET',
			data: data,
			dataType: 'json',
			async: false,
			success: function(response){
				if( response.length > 0){
					msg = gettext( 'VALIDATE-SOURCENAMEALREADYEXIST-TEXT' );	
				}
			}
		});
		return msg;
	},

	validateSourceUrlAlreadyExist: function() {
		var url = '/rest/sources.json/',
			data = {},
			msg = false;
		data['url'] = this.get('url');
		$.ajax({
			url: url,
			type: 'GET',
			data: data,
			dataType: 'json',
			async: false,
			success: function(response){
				if( response.length > 0){
					msg =  gettext( 'VALIDATE-SOURCEALREADYEXIST-TEXT1' ) + response[0] + gettext( 'VALIDATE-SOURCEALREADYEXIST-TEXT2' );	
				}
			}
		});
		return msg;
	}

});
