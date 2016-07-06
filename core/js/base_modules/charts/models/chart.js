var charts = charts || {
    models: {},
    views: {}
};

charts.models.Chart = Backbone.Model.extend({
    urlRoot: '/api/charts/',
    defaults: {
        lib: 'google',
        showLegend: true,
        invertData: undefined,
        invertedAxis: undefined,
        chartTemplate: undefined,
        nullValueAction: 'exclude',
        nullValuePreset: undefined,

        //flag que indica si alguna vez abrió el modal de datos, es para validación
        select_data: false,

        //validation
        message: '',

        //metadata
        title: undefined,
        description: undefined,
        notes: undefined,
        datastream_category: undefined,
        datastream_sources: undefined,
        datastream_tags: undefined,
        parameters: undefined,

        //data selection
        range_headers: undefined,
        range_data: undefined,
        range_labels: undefined,

        // Map defaults
        joinIntersectedClusters: false,
        heatMap: undefined,
        onHeatMap: false,
        needToReloadData: false, //special case where I zoom on a heatMap
        mapType : 'ROADMAP',
        styles: {},
        options: {
            zoom: 2,
            center: {
                lat: 0,
                long: 0
            },
            bounds: [85,180,-85,-180]
        }

    },
    initialize: function (options) {

        //Se inicializa acá para prevenir error en embed
        if(window.gettext){
            this.set('message',gettext("APP-CUSTOMIZE-VISUALIZATION-SELECT-DATA-TEXT"));
        }

        this.data = new charts.models.ChartData({
            id: this.get('id'),
            type: this.get('type')
        });
        this.editMode = false;

        this.bindEvents();
    },

    bindEvents: function () {
        //Se actualizan los filtros de los datos cuando se cambian las options
        this.on('change', this.bindDataModel, this);
        this.listenTo(this.data, 'data_updated', this.handleDataUpdate);
    },

    parse: function (res) {

        var data = {
            datastream_revision_id: res.datastream_revision_id,
            datastream_tags:  res.datastream_tags,
            datastream_sources: res.datastream_sources,
            datastream_category: res.datastream_category
        };

        this.editMode = res.editMode || false;

        _.extend(data, _.pick(res, [
            'revision_id',
            'lib'
            ]));


        //edit
        if (res.revision_id) {
            data = _.extend(data,{
                type: res.format.type,

                data: res.data,
                
                select_data:true,
                notes: _.unescape(res.notes),
                title: res.title,
                description: res.description,

                //config
                showLegend: (res.format.showLegend == 'checked'),
                chartTemplate: res.format.chartTemplate,

                invertData: (res.format.invertData == 'checked'),
                invertedAxis: (res.format.invertedAxis == 'checked'),

                nullValueAction: res.format.nullValueAction,
                nullValuePreset: res.format.nullValuePreset,
            });
            if (data.type === 'mapchart') {
                data = _.extend(data,{
                    mapType: res.chart.mapType? res.chart.mapType.toUpperCase(): undefined,
                    geoType: res.chart.geoType,
                    options:{
                        zoom: res.chart.zoom,
                        bounds: res.chart.bounds? res.chart.bounds.split(';'): undefined,
                        center: res.chart.center? {lat: res.chart.center[0], long: res.chart.center[1]}: undefined                    }
                });
            };
        }

        //edit
        if (res.revision_id && this.editMode) {
            data = _.extend(data,{
                headerSelection: res.chart.headerSelection,
                labelSelection: res.chart.labelSelection,

                latitudSelection: res.chart.latitudSelection,
                longitudSelection: res.chart.longitudSelection

            });

            if (data.type === 'mapchart') {
                data = _.extend(data,{
                    latitudSelection: res.chart.latitudSelection,
                    longitudSelection: res.chart.longitudSelection,
                    traceSelection: res.chart.traceSelection,
                    mapType: res.chart.mapType? res.chart.mapType.toUpperCase(): undefined,
                    geoType: res.chart.geoType,
                    options:{
                        zoom: res.chart.zoom,
                        bounds: res.chart.bounds? res.chart.bounds.split(';'): undefined,
                        center: res.chart.center? {lat: res.chart.center[0], long: res.chart.center[1]}: undefined
                    }
                });
            };
        }
        var options = {
            silent: res.silent
        }

        this.set(data, options);

    },

    bindDataModel: function () {
        var self = this,
            filters = {};

        if (this.get('type') === 'mapchart' || this.get('type') === 'trace') {
            filters = this.getMapPreviewFilters();
        } else {
            filters = this.getChartPreviewFilters();
        }

        // Set de visualization_parameters al data model
        if( !_.isUndefined( this.get('parameters') ) ){
            this.data.set( 'parameters', this.get('parameters') );
        }

        this.data.set('filters', filters);
    },

    getChartPreviewFilters: function () {

        if(!this.isValid()){
            console.error('error en valid');
        }

        var filters = {
            data: this.get('data'),
            headers: this.get('headerSelection'),
            labels: this.get('labelSelection'),
            nullValueAction: this.get('nullValueAction'),
            nullValuePreset:  this.get('nullValuePreset') || '',
            type: this.get('type')
        };

        var revision_id = this.get('datastream_revision_id');
        if (!_.isUndefined(revision_id)) {
            filters['revision_id'] = revision_id
        }

        if(this.get('invertData')===true){
            filters['invertData'] = true;
        }

        if(this.get('invertedAxis')===true){
            filters['invertedAxis'] = true;
        }
        return filters;
    },

    getMapPreviewFilters: function () {
        var id = this.get('id');

        var filters = {
                zoom: this.get('options').zoom,
                bounds: (this.get('options').bounds)? this.get('options').bounds.join(';'): undefined,
                type: 'mapchart'
        };

        if(_.isUndefined(id)){
            filters = _.extend(filters,{
                nullValueAction: this.get('nullValueAction'),
                data: this.get('data'),
                lat: this.get('latitudSelection'),
                lon: this.get('longitudSelection'),
                traces: this.get('traceSelection')
            });
            var revision_id = this.get('datastream_revision_id');
            if (!_.isUndefined(revision_id)) {
                filters['revision_id'] = revision_id
            }
        } else {
            filters['revision_id'] = id
        }


        if (this.has('nullValuePreset')) {
            filters.nullValuePreset = this.get('nullValuePreset');
        }
        return filters;
    },

    /**
     * Handler para manejar las actualizaciones a los datos
     * @return {[type]} [description]
     */
    handleDataUpdate: function () {
        this.trigger('data_updated');
    },

    /**
     * Fetch data for the chart
     * @return {promise}
     */
    fetchData: function () {
        return this.data.fetch();
    },

    valid: function(){
        var valid = true;

        //Si alguna vez intentó seleccionar algo de data
        if(this.get('select_data')){

            if (this.get('type') === 'mapchart') {

                // example validation
                // valid = (this.data.get('clusters').length >0);
                valid = true;
                //console.log('valid',valid);

            } else if (this.get('type') === 'piechart') {

                // TODO: agregar validacion 
                // tenemos piechart que traen 'series' con unv alor y piecharts que no.
                valid = true;
                //console.log('valid',valid);
            
            } else {

                //General validation
                var lFields = this.data.get('fields').length;

                var check = _.reduce(this.data.get('rows'),
                    function(memo, ar){
                     return (ar.length==lFields)?memo:memo + 1;
                    }, 0);

                if (check!=0){
                    this.set("message",gettext("APP-CUSTOMIZE-VISUALIZATION-VALIDATE-HEADLINES")); //reemplazar por locale
                    valid = false;
                }

                if(valid){
                    //TODO specific validation for chart type
                    switch(this.get('type')){
                        case 'piechart':
                            //console.log('is pie chart');
                            //validar que no haya números negativos en la primer serie que se usa para el pie
                        break;
                    }
                }

            }



        }

        return valid;
    },

    validateMetadata: function(){
        var validTitle = !_.isEmpty(this.get('title')),
            validDescription = !_.isEmpty(this.get('description'));
            //validNotes = this.get('notes').length < 2048;

        return {
                //valid: (  validTitle &&  validDescription && validNotes ),
                valid: (  validTitle &&  validDescription ),
                fields:{
                    'title':  !validTitle,
                    'description':  !validDescription,
                    //'notes': !validNotes
                }
            };
    },

    paramsToURLString: function(parameters){
        var result = [];
        _.each(parameters, function(parameter){
            result.push('pArgument' + parameter.position + '=' + parameter.default);
        });
        return result.join('&');
    },

    getSettings: function(){
        var settings = {
            title: this.get('title'),
            description: this.get('description'),
            notes: this.get('notes'),

            parameters: this.paramsToURLString(this.get('parameters')),

            type: this.get('type'),
            lib: this.get('lib'),
            showLegend: this.get('showLegend'),
            chartTemplate: 'basicchart', // Muchachos, mando una para probar pero no se el criterio y es viernes por la noche. Las opciones son basicchart, piechart, mapchart, geochart
            nullValueAction: this.get('nullValueAction'),
            nullValuePreset: this.get('nullValuePreset'),
            invertData: this.get('invertData'),
            invertedAxis: this.get('invertedAxis'),

            //data selection
            headerSelection: this.get('headerSelection'),
            data: this.get('data'),
            labelSelection: this.get('labelSelection')

        };

        if (this.get('type') === 'mapchart') {
            settings = _.extend( settings, {
                latitudSelection: this.get('latitudSelection'),
                longitudSelection: this.get('longitudSelection'),
                traceSelection: this.get('traceSelection'),
                mapType: this.get('mapType').toLowerCase(),
                geoType: this.get('geoType'),
                zoom: this.get('options').zoom,
                bounds: this.get('options').bounds.join(';')
            });
        };

        settings = _.extend( settings,this.getChartAttributes() );

        return settings;
    },

    getChartAttributes: function(){
        var attr = {};
        var that = this;
        _.each(this.get('attributes'),function(e){
            attr[e] = that.get(e);
        });
        return attr;
    },

    validate: function (attrs, options) {
        var nullValuePreset = attrs.nullValuePreset;

        if (!_.isUndefined(attrs.nullValueAction) && attrs.nullValueAction === 'given') {

            if (!_.isUndefined(nullValuePreset) && isNaN(nullValuePreset)) {
                return 'invalid-value';
            }

        }
    },

    save: function (attrs, options) {
        var data = this.getSettings();

        return $.ajax({
            type:'POST',
            data: data,
            dataType: 'json'
        }).then(function (response) {
            if(response.status=='ok'){
                //console.log(response);
                return response;
            } else {
                console.error(response);
            }
        });
    },

    remove: function (options) {
        var opts = _.extend({url: '/visualizations/remove/' + this.id}, options || {});

        return Backbone.Model.prototype.destroy.call(this, opts);
    },

    remove_revision: function (options) {
        var opts = _.extend({url: '/visualizations/remove/revision/' + this.id}, options || {});

        return Backbone.Model.prototype.destroy.call(this, opts);
    },

    checkLegend: function(){
        var legend = this.get('showLegend');

        // Checkeo que no haya series vacia. Si las hay genere una propiedad showLegend = false en el response.
        if( this.get('type') !== 'mapchart' ){

            if( !_.isUndefined( this.data.get('response') ) ){

                var response = this.data.get('response');
                var showLegend = response.showLegend;

                if( !_.isUndefined( showLegend ) ){
                    legend = showLegend;
                }

            }
            
        }        

        return legend;
    }
});
