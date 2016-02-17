var viewEmbedChartView = Backbone.View.extend({

    el : "body",
    chartContainer: "#id_visualizationResult",

    initialize : function() {

        // Init Visualization
        this.chartView = new ChartView({
            el: this.chartContainer,
            model: this.model
        });

        // Bind Resize
        this.bindVisualizationResize();

        // Set Heights
        this.handleVisualizationResize();

    },

    render : function() {

        this.chartView.render();

        return this;
    },

    bindVisualizationResize: function () {

        var self = this;

        this.$window = $(window);

        this.$window.on('resize', function () {
            if(this.resizeTo) clearTimeout(this.resizeTo);
            this.resizeTo = setTimeout(function() {
                self.handleVisualizationResize.call(self);
            }, 500);
        });

    },

    handleVisualizationResize: function(){
        var overflowX =  'hidden',
            overflowY =  'hidden',
            $header = this.$el.find('.chartTitle');

        //Calcula el alto que deberá tener el contenedor del chart
        var height = this.$window.height() - $header.outerHeight(true);

        this.chartView.$el.css({
            height: height + 'px',
            maxHeight: height + 'px',
            minHeight: height + 'px',
            overflowX: overflowX,
            overflowY: overflowY
        });

        this.render();

    }

});