var TagsModel = Backbone.Model.extend({
    defaults: {
        tag__name: undefined
    },

    validation: {
        tag__name: {
                maxLength: 40,
                msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 40 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
            }
    }
});