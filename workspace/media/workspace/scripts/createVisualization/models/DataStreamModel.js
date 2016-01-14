var DataStreamModel = Backbone.Model.extend({
    idAttribute: 'datastream_revision_id',

    url: function () {
        return ['/rest/datastreams/',
            this.get('datastream_revision_id'),
            '/data.json?limit=50&page=0'].join('');
    },

    initialize: function () {
        this.data = new Backbone.Model();
    },

    parse: function (response) {
        var columns = _.first(response.fArray, response.fCols),
            rows = _.map(_.range(0, response.fRows), function (i) {
              var row = response.fArray.slice(i*response.fCols, (i+1)*response.fCols);
              return _.pluck(row, 'fStr');
            });

        this.data.set('columns', columns);
        this.data.set('rows', rows);
    },

})