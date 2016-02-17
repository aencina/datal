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
			},
			{
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
	}

});

