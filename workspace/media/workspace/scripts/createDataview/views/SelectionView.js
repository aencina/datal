var SelectionView = Backbone.View.extend({
    events: {
        'click a.btn-clear': 'onClickClear',
        'click a.btn-edit': 'onClickEdit',
        'click a.btn-headers': 'onClickHeaders',
        'click a.btn-filters': 'onClickFilters',
        'click a.btn-formats': 'onClickFormats'
    },

    initialize: function (options) {
        this.dataviewModel = options.dataviewModel;

        this.template = _.template( $('#selection_template').html() );
        this.listenTo(this.dataviewModel.selection, 'add change remove reset', this.render, this);
        this.listenTo(this.dataviewModel.filters, 'add change remove reset', this.render, this);
        this.listenTo(this.dataviewModel.formats, 'add change remove reset', this.render, this);
        this.listenTo(this.dataviewModel.args, 'add change remove reset', this.render, this);
        this.listenTo(this.model, 'change', this.render, this);
    },

    render: function () {
        var columns = this.filter('col'),
            rows = this.filter('row'),
            cells = this.filter('cell'),
            tables = this.filter('table'),
            headers = this.filter('header'),
            total = this.dataviewModel.selection.length;

        this.$el.html(this.template({
            columns: columns,
            rows: rows,
            cells: cells,
            tables: tables,
            headers: headers,
            total: total,
            filters: this.dataviewModel.filters.toJSON(),
            formats: this.dataviewModel.formats.toJSON(),
            state: this.model.toJSON()
        }));
    },

    onClickClear: function (e) {
        var mode = $(e.currentTarget).data('mode'),
            col = $(e.currentTarget).data('col');

        if (mode === 'filter') {
            this.dataviewModel.filters.remove(col);
        } else if (mode === 'format') {
            this.dataviewModel.formats.remove(col);
        } else {
            this.clearByMode(this.dataviewModel.selection, mode);
        }
    },

    onClickEdit: function (e) {
        var mode = $(e.currentTarget).data('mode'),
            model,
            col = $(e.currentTarget).data('col');

        if (mode === 'filter') {
            model = this.dataviewModel.filters.get(col);
            this.model.set('currently-editing-model', model);
            this.model.set('mode', 'add-filter');
        } else if (mode === 'format') {
            model = this.dataviewModel.formats.get(col);
            this.model.set('currently-editing-model', model);
            this.model.set('mode', 'set-formats');
        } else {
            this.clearByMode(this.dataviewModel.selection, mode);
        }
    },

    onClickHeaders: function () {
        this.model.set('mode', 'headers');
    },

    onClickFilters: function () {
        this.model.set('mode', 'add-filter');
    },

    onClickFormats: function () {
        this.model.set('mode', 'set-formats');
    },

    show: function () {
        this.$el.removeClass('hidden');
    },

    hide: function () {
        this.$el.addClass('hidden');
    },

    filter: function (mode) {
        return this.dataviewModel.selection.filterByMode(mode).map(function (model) {
            return model.toJSON();
        });
    },

    clearByMode: function (collection, mode) {
        collection.remove(collection.filterByMode(mode));
    }

});
