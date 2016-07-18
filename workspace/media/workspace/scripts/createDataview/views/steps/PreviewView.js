var test;

var PreviewView = Backbone.View.extend({

    events: {
        'click a.go-to': 'onGoTo'
    },

    initialize: function (options) {
        this.setLoading();
        this.template = _.template( $('#preview_dataview_template').html() );
        this.categories = options.categories;
        this.stateModel = options.stateModel;

        this.model.data.clear();
        this.model.fetch();
        
        // Esta linea no entra en el response. La cambio por la que sigue.
        //this.listenTo(this.model.data, 'change:rowsRaw change:headers', this.render, this);
        this.listenTo(this.model.data, 'change:response', this.render, this);
    },

    setLoading: function(){
        this.$el.html('<div class="loading light" style="height: 300px"></div>');
        this.setLoadingHeight();
    },

    setLoadingHeight: function(){
        var self = this;

        $(window).resize(function(){

            var windowHeight = $(window).height(),
                sectionTitleHeight = $('.main-section .section-title').height();

            var sectionContentHeight =
                windowHeight
                - $('.global-navigation').height()
                - sectionTitleHeight;

            self.$('.loading.preview-loading').css({
                'height': sectionContentHeight+'px'
            });

        }).resize();

    },

    render: function () {

        var container = this.$('.table-container').get(0),
            rowsRaw = this.model.data.get('rowsRaw'),
            headers = this.model.data.get('headers'),
            categoryId = Number(this.model.get('category')),
            category = _.find(this.categories, function (category) {
                return category[0] === categoryId;
            }),
            response,
            rows = [],
            fType, 
            className;

        if( !_.isUndefined( this.model.data.get('response') ) ){

            response = this.model.data.get('response');

            // a veces cuando elijo 1 celda el preview la devuelve como ARRAY. No queremos eso.
            if( 
                response.fType == 'ARRAY' && 
                response.fCols == 1 && 
                response.fLength == 1 && 
                response.fRows == 1 
            ){  
                // Fusiono response con el valor de la celda y limpio lo perteneciente a array.
                _.extend(response, response.fArray[0]);
                response = _.omit(response, 'fArray');
                response = _.omit(response, 'fCols');
                response = _.omit(response, 'fRows');
            }

            fType = response.fType;

            // Formateo de datos
            if( fType == 'ARRAY' ){
                // Formateo filas para la tabla
                rows = this.formatRows(rowsRaw);
            }else if( fType != 'ERROR' ){
                // Formateo la celda de tipo numero, texto, link o fecha.
                rows = this.formatCell( response );
            }else{
                // Nada para formatear si es error
            }

            // Configuro class Name
            switch(fType){
                case "ARRAY":
                    className = "array";
                    break;  
                case "TEXT":
                case "LINK":
                    className = "text";
                    break;
                case "DATE":
                case "NUMBER":
                    className = "number";
                    break;
                case "ERROR":
                    className = "error";
                    break;
            }

        }


        this.$el.html(this.template({
           rows: rows,
           headers: _.map(headers, this.formatCell.bind(this)),
           dataview: this.model.toJSON(),
           tags: this.model.tags.toJSON(),
           sources: this.model.sources.toJSON(),
           category: category,
           fType: fType,
           className: className
        }));

    },

    onGoTo: function (e) {
        var step = $(e.currentTarget).data('step');
        this.stateModel.set({step: step});
    },

    formatRows: function (rows) {
        var self = this;
        var result = _.map(rows, function (cells) {
            return _.map(cells, function (cell) {
                return self.formatCell(cell);
            });
        });
        return result;
    },

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

    formatTEXT: function (cell) {
        var value;
        value = (cell.fStr.length !== 1)? cell.fStr: cell.fStr.replace('-', '&nbsp;');
        value = value.replace(/(<([^>]+)>)/ig," "); // remove html tags from string
        return value;
    },

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

            var dt = new Date(timestamp);
            dt.setTime( dt.getTime() + dt.getTimezoneOffset()*60*1000 );

            value = $.datepicker.formatDate(format.fPattern, dt, {
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

    formatNUMBER: function (cell) {
        var format = cell.fDisplayFormat,
            number = ( _.isUndefined(format) ) ? cell.fNum : $.formatNumber( cell.fNum, {format:format.fPattern, locale:format.fLocale} );
        return String(number);
    },

    formatLINK: function (cell) {
        var value = '<a target="_blank" href="' + cell.fUri + '" rel="nofollow" title="' + cell.fStr + '">' + cell.fStr + '</a>';
        return value;
    }
});
