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
            filters = this.get('filters');

        if (filters.type !== 'mapchart') {

            // Si series no viene en la respuesta, o viene vacio, procedo a crearlo vacío.
            if( 
                _.isUndefined( response.series ) || 
                _.isEmpty(response.series) || 
                response.series == ''
            ){

                response.series = [];
                var values = [];

                for(var i=0;i<response.values.length;i++){

                    // Solo uso los valores que no son vacios
                    if( response.values[i].length > 0 ){
                        response.series.push({
                            'name': ''
                        }); 
                        values.push( response.values[i] );
                    }

                }

                response.values = values;

            // Si el length de series == 1 y el length de values es > 1, concateno los values.
            }else if(
                response.series.length == 1 &&
                response.values.length > 1 
            ){
                var values = _.flatten(response.values);
                response.values = [];
                response.values.push(values);
            
            // Si values tiene un array vacio lo remuevo y lo remuevo de series tambien.
            }else if( 
                response.series.length == response.values.length 
            ){

                var series = [],
                    values = [];

                for(var i=0;i<response.values.length;i++){
                    if( response.values[i].length > 0 ){
                        series.push( response.series[i] ); 
                        values.push( response.values[i] );
                    }
                }

                response.series = series;
                response.values = values;                

            }

            // Si labels no viene en la respuesta, o viene vacio, procedo a crearlo vacío.
            if( 
                _.isUndefined( response.labels ) || 
                _.isEmpty(response.labels) || 
                response.labels == '' 
            ){

                response.labels = [];

                for(var i=0;i<response.values[0].length;i++){
                    response.labels.push(''); 
                }

            }

        }

        var labels = response.labels,
            columns = [],
            fields =[];

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
