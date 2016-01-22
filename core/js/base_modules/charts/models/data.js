var charts = charts || {
    models: {},
    views: {}
};

charts.models.ChartData = Backbone.Model.extend({
    type: 'line',
    idAttribute: 'visualization_revision_id',
    urlRoot: '/rest/charts/',
    defaults: {
        filters: {},
        type: 'line',
        fields: [
            // [fieldtype, fieldname]
        ],
        rows: [
            // [value, value, value, ...]
        ],
        //Map data
        points: [
            // "lat": "00.000000",
            // "long": "-00.000000",
            // "info": "<strong>Point text information</strong>"
        ],
        clusters: [
            // "lat": "00.000000",
            // "long": "-00.000000",
            // "info": "<strong>Point text information</strong>"
        ]
    },

    initialize: function () {
        this.on('change:filters', this.onFiltersChange, this);
    },

    /**
     * Se actualiza la data mediante el metodo fetch cada vez que se escucha un cambio en los filtros
     */
    onFiltersChange: function (model, value) {
        this.fetch();
    },

    /**
     * Se sobreescribe función fetch para detener cualquier request que esté pendiente
     * @return {[type]} [description]
     */
    fetch: function () {
        var self = this;
        this.trigger('fetch:start');

        if(this.fetchXhr && this.fetchXhr.readyState > 0 && this.fetchXhr.readyState < 4){
            this.fetchXhr.abort();
        }
        this.fetchXhr = Backbone.Model.prototype.fetch.apply(this, arguments);
        this.fetchXhr.then(function () {
            self.trigger('data_updated');
        });
        this.fetchXhr.always(function () {
            self.trigger('fetch:end');
        });
        return this.fetchXhr;
    },

    parse: function (response) {

        var response = response,
            columns = [],
            fields =[],
            filters = this.get('filters'),
            invertedAxis = filters.invertedAxis;

        // Si labels no viene en la respuesta, o viene vacio, procedo a crearlo vacío.
        if( 
            _.isUndefined( response.labels ) || 
            _.isEmpty(response.labels) || 
            response.labels == '' 
        ){

            response.labels = [];

            // Labels length = cantidad de filas
            var labelsLength = response.values[0].length;

            // Si viene invertedAxis, uso la cantidad de columnas como length
            if( !_.isUndefined( invertedAxis ) ){
                labelsLength = response.values.length;
            }

            for(var i=0;i<labelsLength;i++){
                response.labels.push(''); 
            }

        }

        // Si series no viene en la respuesta, o viene vacio, procedo a crearlo vacío.
        if( 
            _.isUndefined( response.series ) || 
            _.isEmpty(response.series) || 
            response.series == ''
        ){

            response.series = [];

            // Series length = cantidad de columnas
            var seriesLength = response.values.length;

            // Si viene invertedAxis, uso la cantidad de filas como length
            if( !_.isUndefined( invertedAxis ) ){
                seriesLength = response.values[0].length;
            }

            for(var i=0;i<seriesLength;i++){
                response.series.push({
                    'name': ''
                }); 
            }

        }

        var labels = response.labels;

        if (filters.type === 'mapchart') {
            return response;
        } else {

            //TODO: arreglar este hack para crear labels vacios
            if (labels && !labels.length) {
                labels = Array.apply(null, {length: response.values[0].length}).map(Number.call, Number);
                fields.push(['number', 'labels']);
            } else {
                //TODO: revisar el formato del lable
                fields.push(['string', 'labels']);
            }
            columns.push(labels);

            columns = columns.concat(response.values);
            fields = fields.concat(_.map(response.series, function (item) {
                return ['number', item.name];
            }));

            this.set('fields', fields);
            this.set('rows', _.clone(_.unzip(columns)));

        }
    },

    /**
     * Se arma la url para el fetch utilizando los attributos pasados al modelo y los filtros existentes
     */
    url: function () {
        var filters = this.get('filters'),
            id = this.get('id'), // ID existe cuando la visualizacion está siendo editada
            url,
            endpoint = 'charts/';

        if (filters.type === 'mapchart' || filters.type === 'trace' ) {
            endpoint = 'maps/';
        }

        if (_.isUndefined(id)) {
            url = '/rest/' + endpoint + 'sample.json' + '?' + $.param(filters);
        } else {
            filters = _.omit(filters, 'data')
            filters = _.omit(filters, 'headers')
            filters = _.omit(filters, 'labels')
            filters = _.omit(filters, 'nullValueAction')
            filters = _.omit(filters, 'nullValuePreset')
            filters = _.omit(filters, 'type')
            filters = _.omit(filters, 'invertedAxis')
            filters = _.omit(filters, 'revision_id')
            url = '/rest/' + endpoint + id + '/data.json' + '?' + $.param(filters);
        }

        return url;
    }
});
