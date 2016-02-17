var DataTableSelectedCollection = Backbone.Collection.extend({
    model: DataTableSelectionModel,

    setCache: function () {
        this._cache = this.reduce(function (memo, m) {
            memo[m.get('name')] = m.get('excelRange');
            return memo;
        }, {});
        return this._cache;
    },

    revert: function () {
        _.each(this._cache, function (value, key) {
            var m = this.find(function (model) {
                return model.get('name') === key;
            }).set('excelRange', value);
        }, this);
    },

    setMaxCols: function (maxCols) {
        this.maxCols = maxCols;
    },

    setMaxRows: function (maxRows) {
        this.maxRows = maxRows;
    },

    getItemsByMode: function (mode) {
        return this.filter(function (model) {
            return model.get('mode') === mode;
        });
    },

    hasItemsByMode: function (mode) {
        return this.getItemsByMode(mode).length !== 0;
    },

    removeItemsByMode: function (mode) {
        return this.remove(this.getItemsByMode(mode));
    },

    filterByMode: function (mode) {
        return this.filter(function (model) {
            return model.get('mode') === mode;
        });
    }
});
