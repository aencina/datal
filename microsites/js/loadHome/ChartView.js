var ChartView = Backbone.View.extend({

    initialize: function(){
        this.chartsFactory = new charts.ChartsFactory();
        this.setupChart();
    }, 

    setupChart: function(){

        var chartSettings = this.chartsFactory.create(this.model.get('type'),this.model.get('lib'));

        if(chartSettings){

            //Set list of custom attributes for my model
            this.model.set('attributes',chartSettings.attributes);

            this.ChartViewClass = chartSettings.Class;

        } else {
            delete this.ChartViewClass;
        }

    },

    render: function () {
    
        if (this.ChartViewClass) {

            if(this.chartInstance){
                this.chartInstance.destroy();
            }

            this.chartInstance = new this.ChartViewClass({
                el: this.$el,
                model: this.model
            });

            if(this.model.valid()){
                var height = this.chartInstance.$el.parent().height();
                this.chartInstance.$el.height( height );
                this.chartInstance.render();
            };
        }
    },

});
