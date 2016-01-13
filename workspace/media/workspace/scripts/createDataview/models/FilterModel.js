var FilterModel = Backbone.Epoxy.Model.extend({
    idAttribute: "column",

    defaults: {
        column: undefined,
        operator: undefined,
        type: undefined,
        name: undefined,
        description: undefined,
        'default': undefined
    },

    validation: {
        column: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],
        operator: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],

        type: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],

        name: function(value, attr) {
            if (this.get('type') === 'parameter') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        'default': [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],

    },

    reset: function () {
        var keep = this.pick(['column', 'excelCol']);
        this.set(this.defaults).set(keep);
    }
});