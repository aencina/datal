var ColumnModel = Backbone.Epoxy.Model.extend({
    idAttribute: "column",

    defaults: {
        column: undefined,
        type: 'TEXT',

        inputPattern: undefined,
        inputCustomPattern: undefined,

        inputLocale: undefined,
        separatorType: 'symbol',
        thousandSeparator: undefined,
        decimalSeparator: undefined,

        outputPattern: undefined,
        outputCustomPattern: undefined,
        numberDisplayLocale: undefined,
        dateDisplayLocale: undefined,
    },

    validation: {
        column: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],
        inputPattern: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],

        outputPattern: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            }
        ],

        inputCustomPattern: function(value, attr) {
            if (this.get('inputPattern') === 'custom') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        outputCustomPattern: function(value, attr) {
            if (this.get('outputPattern') === 'custom') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        thousandSeparator: function(value, attr) {
            if (this.get('type') === 'NUMBER' && this.get('separatorType') === 'symbol') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        decimalSeparator: function(value, attr) {
            if (this.get('type') === 'NUMBER' && this.get('separatorType') === 'symbol') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        inputLocale: function(value, attr) {
            if (this.get('separatorType') === 'locale') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        numberDisplayLocale: function(value, attr) {
            if (this.get('type') === 'NUMBER') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        },

        dateDisplayLocale: function(value, attr) {
            if (this.get('type') === 'DATE') {
                if(_.isUndefined(value) || value === '') {
                    return gettext('VALIDATE-REQUIREDFIELD-TEXT');
                }
            }
        }
    },

    reset: function () {
        var keep = this.pick(['column', 'excelCol']);
        this.clear().set(keep);
    }
});