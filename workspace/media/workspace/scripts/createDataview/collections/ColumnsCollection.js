var ColumnsCollection = Backbone.Collection.extend({
    model: ColumnModel,
    comparator: function(obj) {
        return parseInt(obj.get('column'))
    }
});