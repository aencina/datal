var FiltersOptionsView = Backbone.Epoxy.View.extend({

    events: {
        'click button.btn-clear': 'onClickClear',
        'click a.btn-back': 'onClickBack',
        'click button.btn-ok': 'onClickOk',

        'change input[name="default"]': 'onChangeInput'
    },

    bindings: {
        "select.select-column": "value:column, events:['change']",
        "select.select-operator": "value:operator, events:['change']",
        "select.select-value-type": "value:type, events:['change']",
        'input[name="name"]': "value:name, events:['keyup']",
        'textarea[name="description"]': "value:description, events:['keyup']",
    },

    initialize: function (options) {
        this.template = _.template( $('#filters_options_template').html() );
        this.stateModel = options.stateModel;
        this.totalCols = options.totalCols;

        this.listenTo(this.model, 'change:column', this.onChangeColumn, this);
        this.listenTo(this.model, 'change:operator', this.onChangeOperator, this);
        this.listenTo(this.model, 'change:type', this.onChangeValueType, this);
    },

    render: function () {
        var existingColumns = this.collection.map(function (model) {
            return Number(model.get('column'));
        });
        var editingCol = this.model.get('column');
        if (!_.isUndefined(editingCol)) {
            existingColumns.splice(existingColumns.indexOf(Number(editingCol)), 1);
        }

        var availableCols = _.difference(_.range(0, this.totalCols), existingColumns);
        var columns = _.map(availableCols, function (number) {
                return {
                    label: DataTableUtils.intToExcelCol(number + 1),
                    index: number
                };
            });

        this.$el.html(this.template({
            columns: columns,
            column: this.model.toJSON(),
            state: this.stateModel.toJSON()
        }));
        this.applyBindings();

        this.setInitialState();
    },

    setInitialState: function () {
        // Set initial values
        var column = this.model.get('column');
        var operator = this.model.get('operator');
        var type = this.model.get('type');
        var defaultParam = this.model.get('default');

        this.onChangeColumn(null, _.isUndefined(column)? '': column);
        this.onChangeOperator(null, _.isUndefined(operator)? '': operator);
        this.onChangeValueType(null, _.isUndefined(type)? '': type);

        this.$('input[name="default"]').val(defaultParam);
    },

    onClickBack: function () {
        this.stateModel.set('mode', 'data');
    },

    onClickClear: function () {
        this.model.reset();
        this.setInitialState();
    },

    onClickOk: function () {
        this.collection.add(this.model);
        this.stateModel.set('mode', 'data');
    },

    onChangeColumn: function (model, value) {
        if (value !== '') {
            this.model.set('excelCol', DataTableUtils.intToExcelCol(Number(value) + 1));
            this.$('.row-operator').removeClass('hidden');
        } else {
            this.model.unset('excelCol');
            this.$('.row-operator').addClass('hidden')
            this.$('.row-fixed-value').addClass('hidden');
            this.$('.row-parameter').addClass('hidden');
        }
    },

    onChangeOperator: function (model, value) {
        if (value !== '') {
            this.$('.row-value-type').removeClass('hidden');
        } else {
            this.$('.row-value-type').addClass('hidden');
            this.$('.row-fixed-value').addClass('hidden');
            this.$('.row-parameter').addClass('hidden');
        }
    },

    onChangeValueType: function (model, value) {
        if (value === '') {
            this.$('.row-fixed-value').addClass('hidden');
            this.$('.row-parameter').addClass('hidden');
        } else if (value === 'fixed') {
            this.$('.row-fixed-value').removeClass('hidden');
            this.$('.row-parameter').addClass('hidden');
        } else if (value === 'parameter') {
            this.$('.row-fixed-value').addClass('hidden');
            this.$('.row-parameter').removeClass('hidden');
        }
    },

    onChangeInput: function (e) {
        var $target = $(e.currentTarget),
            name = $target.attr('name'),
            value = $target.val();
        if (value !== '') {
            this.model.set(name, value);
        } else {
            this.model.unset(name);
        }
    },

    show: function () {
        this.$el.removeClass('hidden');
    },

    hide: function () {
        this.$el.addClass('hidden');
    },
});
