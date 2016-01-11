var FormatsView = Backbone.Epoxy.View.extend({
    events: {
        'click button.btn-clear': 'onClickClear',
        'click a.btn-back': 'onClickBack',
        'click button.btn-ok': 'onClickOk',
        'change input[name="separator"]': 'onChangeSeparatorType'
    },

    bindings: {
        "select.select-column": "value:column, events:['change']",
        "select.select-data-type": "value:type, events:['change']",
        'input[name="inputCustomPattern"]': "value:inputCustomPattern, events:['keyup']",
        'input[name="outputCustomPattern"]': "value:outputCustomPattern, events:['keyup']",
        "select.decimal-separator": "value:decimalSeparator, events:['change']",
        "select.thousand-separator": "value:thousandSeparator, events:['change']",
        "select[name=inputLocale]": "value:inputLocale, events:['change']",
        "select[name=numberDisplayLocale]": "value:numberDisplayLocale, events:['change']",
        "select[name=dateDisplayLocale]": "value:dateDisplayLocale, events:['change']"
    },

    initialize: function (options) {
        this.template = _.template( $('#formats_template').html() );
        this.stateModel = options.stateModel;
        this.totalCols = options.totalCols;

        this.listenTo(this.model, 'change:column', this.onChangeColumn, this);
        this.listenTo(this.model, 'change:type', this.onChangeType, this);
        this.listenTo(this.model, 'change:inputPattern', this.onChangeInputPattern, this);
        this.listenTo(this.model, 'change:outputPattern', this.onChangeOutputPattern, this);
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
            column: this.model.toJSON()
        }));
        this.$(".tabs").hashTabs();
        this.attachPatternViews(this.model.get('type'));
        this.applyBindings();

        // Set Initial Values
        var separatorType = this.model.get('separatorType');
        var type = this.model.get('type');
        if (type === 'NUMBER' && !_.isUndefined(separatorType)) {
            this.$('.separators').toggleClass('hidden', separatorType === 'locale');
            this.$('input:radio[name="separator"][value="' + separatorType + '"]').prop('checked', true);
        }
        if (type === 'NUMBER' && separatorType === 'locale' || type === 'DATE') {
            this.$('.input-locale').removeClass('hidden');
        } else {
            this.$('.input-locale').addClass('hidden');
        };
        this.onChangeInputPattern(null, this.model.get('inputPattern'));
        this.onChangeOutputPattern(null, this.model.get('outputPattern'));

        Backbone.Validation.bind(this, {
            valid: function (view, attr, selector) {
                view.setIndividualError(view.$('[name=' + attr + ']'), attr, '');
            },
            invalid: function (view, attr, error, selector) {
                view.setIndividualError(view.$('[name=' + attr + ']'), attr, error);
            },
        });
    },

    attachPatternViews: function (type) {
        this.destroyChildView('inputPatternView');
        this.inputPatternView = new PatternView({
            el: this.$('.input-pattern-view'),
            type: type,
            subtype: 'input'
        });
        this.inputPatternView.on('change', function (value) {
            this.model.set('inputPattern', value);
        }, this);

        this.destroyChildView('displayPatternView');

        this.displayPatternView = new PatternView({
            el: this.$('.display-pattern-view'),
            type: type,
            subtype: 'output'
        });
        this.displayPatternView.on('change', function (value) {
            this.model.set('outputPattern', value);
        }, this);
        this.displayPatternView.render();
        this.inputPatternView.render();

        // Set Initial states
        this.displayPatternView.setValue(this.model.get('outputPattern'));
        this.inputPatternView.setValue(this.model.get('inputPattern'));
    },

    destroyChildView: function (childViewName) {
        if (this[childViewName]) {
            this[childViewName].$el.empty();
            delete this[childViewName];
        }
    },

    onClickBack: function () {
        this.stateModel.set('mode', 'data');
    },

    onClickClear: function () {
        this.model.reset();
        this.model.set('type', 'NUMBER');
    },

    onClickOk: function () {
        if (this.model.isValid(true)) {
            this.collection.add(this.model);
            this.stateModel.set('mode', 'data');
        }
    },

    onChangeColumn: function (model, value) {
        this.$('.row-data-type').toggleClass('hidden', value === '');
        if (value !== '') {
            this.model.set('excelCol', DataTableUtils.intToExcelCol(Number(value) + 1));
            this.model.set('type', 'NUMBER');
        } else {
            this.model.set('type', 'TEXT');
            this.model.unset('excelCol');
        }
    },

    onChangeType: function (model, value) {
        this.$('.input-output-view').toggleClass('hidden', value === 'TEXT');
        this.$('.number-display-locale').toggleClass('hidden', value !== 'NUMBER');
        this.$('.date-display-locale').toggleClass('hidden', value !== 'DATE');
        this.$('.separators').toggleClass('hidden', value !== 'NUMBER');
        this.$('.symbols-locale-option').toggleClass('hidden', value !== 'NUMBER');

        this.model.set('outputPattern', '');
        this.model.set('inputPattern', '');
        if (value === 'NUMBER' || value === 'DATE') {
            this.attachPatternViews(value);
        }
        if (value === 'NUMBER' && this.model.get('separatorType') === 'locale' || value === 'DATE') {
            this.$('.input-locale').removeClass('hidden');
        } else {
            this.$('.input-locale').addClass('hidden');
        };
    },

    onChangeInputPattern: function (model, value) {
        this.$('.custom-origin-pattern').toggleClass('hidden', value !== 'custom');
    },

    onChangeOutputPattern: function (model, value) {
        this.$('.custom-display-pattern').toggleClass('hidden', value !== 'custom');
    },

    onChangeSeparatorType: function (e) {
        var value = $(e.currentTarget).val();
        this.model.set('separatorType', value);
        this.$('.input-locale').toggleClass('hidden', value === 'symbol');
        this.$('.separators').toggleClass('hidden', value === 'locale');
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

    setIndividualError: function(element, name, error){
        if( error !== ''){
            element.addClass('has-error');
            element.next('p.has-error').remove();
            element.after('<p class="has-error">'+error+'</p>');
        } else {
            element.removeClass('has-error');
            element.next('p.has-error').remove();
        }
    },
});
