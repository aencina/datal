var SelectDataView = Backbone.View.extend({

    events: {
        'change select.select-table': 'onChangeTable',
        'click a.edit-arg': 'onClickEditArg'
    },

    _selectionEnabled: true,

    initialize: function (options) {

        this.dataviewModel = options.dataviewModel;
        this.datasetModel = options.datasetModel;
        this.internalState = new Backbone.Model({
            mode: 'data'
        });

        this.template = _.template( $('#select_data_template').html() );

        this.listenTo(this.internalState, 'change:mode', this.onChangeMode, this);
        this.listenTo(this.dataviewModel.dataset, 'change:tables', this.render, this);
    },

    render: function () {
        var tableId = tableId = this.dataviewModel.get('tableId');

        var editableArgs = this.datasetModel.args.where({editable: true}).map(function (m) {
            return m.toJSON()
        });

        this.$el.html(this.template({
            tables: this.datasetModel.getTables(),
            args: editableArgs
        }));
        this.$('.select-table').val(tableId);

        this.attachChildrenViews();
    },

    attachChildrenViews: function () {
        var tableId = this.dataviewModel.get('tableId');
        var rows = this.datasetModel.get('tables')[tableId];

        if (this.dataTableView) {
            this.dataTableView.$('.table-view').empty();
        }

        this.dataTableView = new DataTableView({
            el: this.$('.data-table-view'),
            collection: this.dataviewModel.selection,
            dataview: {
                rows: rows
            },
            enableFulllRowSelection: true
        });
        this.listenTo(this.dataTableView, 'afterSelectionEnd', function () {
            this.addSelection();
        }, this);
        this.dataTableView.render();

        if (this.selectionView) {
            this.selectionView.remove();
            delete this.selectionView;
        }
        this.selectionView = new SelectionView({
            collection: this.dataviewModel.selection,
            dataviewModel: this.dataviewModel,
            model: this.internalState
        });
        this.selectionView.render();
        this.$('.selection-view').append(this.selectionView.$el);

        if (this.headersOptionsView) {
            this.headersOptionsView.remove();
            delete this.headersOptionsView;
        }
        this.headersOptionsView = new HeadersOptionsView({
            model: this.internalState,
            collection: this.dataviewModel.selection
        });
        this.headersOptionsView.render();
        this.headersOptionsView.hide();
        this.$('.headers-options-view').append(this.headersOptionsView.$el);
    },

    attachFiltersView: function () {
        this.destroyFiltersView();

        this.filtersOptionsView = new FiltersOptionsView({
            stateModel: this.internalState,
            collection: this.dataviewModel.filters,
            totalCols: this.dataviewModel.get('totalCols'),
            model: new FilterModel()
        });
        this.filtersOptionsView.render();
        this.$('.headers-options-view').append(this.filtersOptionsView.$el);
    },

    destroyFiltersView: function () {
        if (this.filtersOptionsView) {
            this.filtersOptionsView.remove();
            delete this.filtersOptionsView;
        }
    },

    attachFormatsView: function () {
        this.destroyFormatsView();

        this.formatsView = new FormatsView({
            stateModel: this.internalState,
            collection: this.dataviewModel.formats,
            totalCols: this.dataviewModel.get('totalCols'),
            model: new ColumnModel()
        });
        this.formatsView.render();
        this.$('.headers-options-view').append(this.formatsView.$el);
    },

    destroyFormatsView: function () {
        if (this.formatsView) {
            this.formatsView.remove();
            delete this.formatsView;
        }
    },

    canSelectMode: function (mode) {
        var collection = this.dataviewModel.selection,
            hasCells = collection.hasItemsByMode('cell'),
            hasTable = collection.hasItemsByMode('table'),
            hasRows = collection.hasItemsByMode('row'),
            hasCols = collection.hasItemsByMode('col');

        if (mode === 'col' || mode === 'row') {
            return !(hasCells || hasTable);
        } else if (mode === 'table'){
            return !(hasCols || hasRows || hasCells);
        } else if (mode === 'cell'){
            return !(hasCols || hasRows || hasTable);
        } else {
            return true;
        }
    },

    disableSelection: function () {
        this._selectionEnabled = false;
    },

    enableSelection: function () {
        this._selectionEnabled = true;
    },

    addSelection: function () {
        var selection = this.dataTableView.getSelection(),
            model;

        if (!this._selectionEnabled) {
            return;
        }

        if (this.internalState.get('mode') === 'data') {

            if (selection.mode === 'cell' && this.canSelectMode('cell')) {
                model = new DataTableSelectionModel({classname: 'cell'});
            } else if (selection.mode === 'col' && this.canSelectMode('col')) {
                model = new DataTableSelectionModel({classname: 'col'});
            } else if (selection.mode === 'row' && this.canSelectMode('row')) {
                model = new DataTableSelectionModel({classname: 'row'});
            } else if (selection.mode === 'table' && this.canSelectMode('table')) {
                model = new DataTableSelectionModel({classname: 'table'});
            } else {
                return;
            }

        } else if (this.internalState.get('mode') === 'headers') {

            // Solo seleccionar filas en el modo headers
            if (selection.mode === 'row') {
                model = new DataTableSelectionModel({classname: 'header'});
                selection.mode = 'header';
            } else {
                return;
            }

        };

        model.set(selection);

        // TODO: Esta funcionalidad deberia estar encapsulada en collection.toggleModel()
        var existing = this.checkExisting(model);
        if (existing) {
            this.dataviewModel.selection.remove(existing);
        } else {
            this.dataviewModel.selection.add(model);
        }
    },

    checkExisting: function (model) {
        var items = this.dataviewModel.selection.filter(function (item) {
            return item.get('mode') === model.get('mode');
        });
        var existing = _.find(items, function (item) {
            return model.get('excelRange') === item.get('excelRange');
        });
        return existing;
    },

    onChangeTable: function (e) {
        var $target = $(e.currentTarget),
            tableId = $target.val();

        this.dataviewModel.set('tableId', tableId);
        var table = this.datasetModel.get('tables')[tableId];
        this.dataviewModel.set('totalCols', table[0].length);
        this.attachChildrenViews();
    },

    onClickEditArg: function (e) {
        var argName = $(e.currentTarget).data('name'),
            model = this.datasetModel.args.get(argName);
        e.preventDefault();

        this.editArgumentsOverlayView = new EditArgumentOverlayView({
            el: '#overlay',
            model: model
        });
        this.editArgumentsOverlayView.render();
    },

    onChangeMode: function (model, value) {
        if (value === 'headers') {
            this.selectionView.hide();
            this.headersOptionsView.show();
        } else if (value === 'add-filter') {
            this.disableSelection();
            this.selectionView.hide();
            this.attachFiltersView();
        } else if (value === 'set-formats') {
            this.disableSelection();
            this.selectionView.hide();
            this.attachFormatsView();
        } else {
            this.enableSelection();
            this.destroyFiltersView();
            this.destroyFormatsView();
            this.headersOptionsView.hide();
            this.selectionView.show();
        }
    },

    isValid: function () {
        return true;
    }
});