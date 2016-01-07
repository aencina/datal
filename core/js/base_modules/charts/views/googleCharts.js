var charts = charts || {
    models: {},
    views: {}
};

charts.views.GoogleLineChart = charts.views.LineChart.extend({
    initialize: function (options) {
        this.constructor.__super__.initialize.apply(this, arguments);
    },

    formatData: function (data) {
        var dataTable = new google.visualization.DataTable();
        if (data.fields.length === 0) {
            return;
        }
        _.each(data.fields, function (field) {
            dataTable.addColumn(field[0], field[1]);
        });
        dataTable.addRows(data.rows);
        return dataTable;
    },

    render: function () {
        var dataTable = this.formatData(this.model.data.toJSON());
        if (_.isUndefined(dataTable)) {
            return;
        }
        var options = this.model.get('options');

        this.chart = new google.visualization.LineChart(this.el);

        this.chart.draw(dataTable, options);

        return this;
    }
});

charts.views.GoogleAreaChart = charts.views.AreaChart.extend({
    initialize: function (options) {
        this.constructor.__super__.initialize.apply(this, arguments);
    },

    formatData: function (data) {
        var dataTable = new google.visualization.DataTable();
        if (data.fields.length === 0) {
            return;
        }
        _.each(data.fields, function (field) {
            dataTable.addColumn(field[0], field[1]);
        });
        dataTable.addRows(data.rows);
        return dataTable;
    },

    render: function () {
        var dataTable = this.formatData(this.model.data.toJSON());
        if (_.isUndefined(dataTable)) {
            return;
        }
        var options = this.model.get('options');

        options.isStacked = true;

        this.chart = new google.visualization.AreaChart(this.el);

        this.chart.draw(dataTable, options);

        return this;
    }
});


charts.views.GoogleBarChart = charts.views.BarChart.extend({
    initialize: function (options) {
        this.constructor.__super__.initialize.apply(this, arguments);
    },

    formatData: function (data) {
        var dataTable = new google.visualization.DataTable();
        if (data.fields.length === 0) {
            return;
        }
        _.each(data.fields, function (field) {
            dataTable.addColumn(field[0], field[1]);
        });
        dataTable.addRows(data.rows);
        return dataTable;
    },

    render: function () {
        var dataTable = this.formatData(this.model.data.toJSON());
        if (_.isUndefined(dataTable)) {
            return;
        }
        var options = this.model.get('options');

        options.isStacked = false;

        this.chart = new google.visualization.BarChart(this.el);

        this.chart.draw(dataTable, options);

        return this;
    }

});

charts.views.GoogleColumnChart = charts.views.ColumnChart.extend({
    initialize: function (options) {
        this.constructor.__super__.initialize.apply(this, arguments);
    },

    formatData: function (data) {
        var dataTable = new google.visualization.DataTable();
        if (data.fields.length === 0) {
            return;
        }
        _.each(data.fields, function (field) {
            dataTable.addColumn(field[0], field[1]);
        });
        dataTable.addRows(data.rows);
        return dataTable;
    },

    render: function () {
        var dataTable = this.formatData(this.model.data.toJSON());
        if (_.isUndefined(dataTable)) {
            return;
        }
        var options = this.model.get('options');

        options.isStacked = false;

        this.chart = new google.visualization.ColumnChart(this.el);

        this.chart.draw(dataTable, options);

        return this;
    }

});

charts.views.GooglePieChart = charts.views.PieChart.extend({
    initialize: function (options) {
        this.constructor.__super__.initialize.apply(this, arguments);
    },

    formatData: function (data) {
        var dataTable = new google.visualization.DataTable();

        var graphData = [];

        _.each(data.rows,function(e,i){
            graphData.push([e[0],e[1]]);
        });

        dataTable.addColumn('string', 'Label');
        dataTable.addColumn('number', 'Data');

        dataTable.addRows(graphData);

        return dataTable;
    },

    render: function () {
        var dataTable = this.formatData(this.model.data.toJSON());

        var options = this.model.get('options');

        this.chart = new google.visualization.PieChart(this.el);

        this.chart.draw(dataTable, options);

        return this;
    }

});
