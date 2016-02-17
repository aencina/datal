var SourceModel = Backbone.Model.extend({
	defaults: {
		source__name: undefined,
		source__url: undefined
	},

  validation: {
    source__name: [
      {
        required: true,
        msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
      },{
        maxLength: 40,
        msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 40 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
      }
    ],
    source__url: [
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
});