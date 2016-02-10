var charts = charts || {
    models: {},
    views: {}
};


charts.views.Chart = Backbone.View.extend({
    initialize: function(){
        if (this.model.get('type') === null) {
            console.error('Chart models must define a type property');
        }
        this.bindEvents();
    },

    bindEvents: function () {
        // this.model.on('change', this.render, this);
        this.model.on('data_updated', this.handleDataUpdated, this);
    },

    handleDataUpdated: function () {
        this.render();
    },

    formatData: function () {
    	// reads data from model and returns formated data for the specific
    	// subclass
    },

    render: function () {
    	// implements rendering of data received from :formatData: for the 
    	// specific chart library
    },

    destroy: function(){
        if (this.model.get('isMap')) {
            //No se puede destruir oficialmente una instancia de googleMaps - https://code.google.com/p/gmaps-api-issues/issues/detail?id=3803
            if(this.mapInstance){
                this.$el.attr('style','');
                this.$el.empty();
                google.maps.event.clearInstanceListeners(window);
                google.maps.event.clearInstanceListeners(document);
                google.maps.event.clearInstanceListeners(this.el);
                delete this.mapInstance;
                delete this.heatMapLayer;
            }

        }else{
            if(this.chart && this.chart.destroy){ //c3
                this.chart.destroy();
            }
            if(this.chart && this.chart.clearChart){ //google
                this.chart.clearChart();
            }            
        }
        this.stopListening();
    }
});
