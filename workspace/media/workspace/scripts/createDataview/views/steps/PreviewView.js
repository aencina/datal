var PreviewView = Backbone.View.extend({

    initialize: function () {
        this.template = _.template( $('#preview_dataview_template').html() );
        this.model.data.clear();
        this.model.fetch();
        this.listenTo(this.model.data, 'change:rowsRaw change:headers', this.render, this);
    },

    render: function () {
        var container = this.$('.table-container').get(0),
            rowsRaw = this.model.data.get('rowsRaw'),
            headers = this.model.data.get('headers');

        this.$el.html(this.template({
          rows: this.formatRows(rowsRaw),
          headers: _.map(headers, this.formatCell.bind(this)),
          dataview: this.model.toJSON(),
          tags: this.model.tags.toJSON(),
          sources: this.model.sources.toJSON()
        }));

    },

    // TODO: Código portado de un template, necesita mejoras
    formatRows: function (rows) {
        var self = this;
        var result = _.map(rows, function (cells) {
            return _.map(cells, function (cell) {
                return self.formatCell(cell);
            });
        });
        return result;
    },

    // TODO: Código portado de un template, necesita mejoras
    formatCell: function (cell) {
        var value;

        if (cell.fType === 'TEXT') {
            value = this.formatTEXT(cell);
        } else if (cell.fType === 'DATE') {
            value = this.formatDATE(cell);
        } else if (cell.fType === 'NUMBER') {
            value = this.formatNUMBER(cell);
        } else if (cell.fType === 'LINK') {
            value = this.formatLINK(cell);
        }

        return value;
    },

    // TODO: Código portado de un template, necesita mejoras
    formatTEXT: function (cell) {
        var value;
        value = (cell.fStr.length !== 1)? cell.fStr: cell.fStr.replace('-', '&nbsp;');
        value = value.replace(/(<([^>]+)>)/ig," "); // remove html tags from string
        return value;
    },

    // TODO: Código portado de un template, necesita mejoras
    formatDATE: function (cell) {
        var value;
        var format = cell.fDisplayFormat;
        var timestamp = cell.fNum;
        if (! _.isUndefined(format)) {
            // sometimes are seconds, sometimes miliseconds
            if (timestamp < 100000000000) {
                timestamp = timestamp * 1000;
            }
            var locale = format.fLocale;
            //One must use "" for "en"
            if (undefined === locale || locale === "en" || locale.indexOf("en_")) {
                locale = "";
            }
            if (locale.indexOf("es_")) {
                locale = "es";
            }

            value = $.datepicker.formatDate(format.fPattern, new Date(timestamp), {
                dayNamesShort: $.datepicker.regional[locale].dayNamesShort,
                dayNames: $.datepicker.regional[locale].dayNames,
                monthNamesShort: $.datepicker.regional[locale].monthNamesShort,
                monthNames: $.datepicker.regional[locale].monthNames
            });
        } else {
            value = String(timestamp);
        }
        return value;
    },

    // TODO: Código portado de un template, necesita mejoras
    formatNUMBER: function (cell) {
        var format = cell.fDisplayFormat,
            number = ( _.isUndefined(format) ) ? cell.fNum : $.formatNumber( cell.fNum, {format:format.fPattern, locale:format.fLocale} );
        return String(number);
    },

    // TODO: Código portado de un template, necesita mejoras
    formatLINK: function (cell) {
        var value = '<a target="_blank" href="' + cell.fUri + '" rel="nofollow" title="' + cell.fStr + '">' + cell.fStr + '</a>';
        return value;        
    }
});
