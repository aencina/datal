var SelectedCellRangeView = Backbone.View.extend({

	events: {
		'focusin input[type="text"]': 'onFocusInput',
		'focusout input[type="text"]': 'onFocusOutInput',
		'keyup input[type="text"]': 'onKeyupInput'
	},

	initialize: function (options) {
        this.listenTo(this.collection, 'change:excelRange', this.onChangeExcelRange, this);
        this.listenTo(this.model, 'change:type', this.render, this);
	},

	render: function  () {
        var type = this.model.get('type'),
            geoType = this.model.get('geoType'),
            inputs = [];

        if (type === 'mapchart') {
            if (geoType === 'points') {
                inputs = ['latitudSelection', 'longitudSelection', 'data'];
            } else if (geoType === 'traces') {
                inputs = ['traceSelection', 'data'];
            }
        } else {
            inputs = ['data', 'labelSelection', 'headerSelection'];
        }

		this.$('.input-row').addClass('hidden');
		_.each(inputs, function (name) {
			this.$('[data-name="' + name + '"].input-row ').removeClass('hidden');
		});
		this.$('.input-row:not(.hidden) input[type="text"]').first().focus();
	},
	focus: function () {
	},
	clear: function () {
		this.$('input[type="text"]').val('');
	},

	onFocusInput: function (event) {
		var $target = $(event.currentTarget),
			name = $target.attr('name');
		this.$('input[type="text"]').removeClass('active');
		$target.addClass('active');
		this.selectedInput = $target;
		this.trigger('focus-input', name);
	},

	onFocusOutInput: function (event) {
		var $target = $(event.currentTarget),
			name = $target.attr('name');
		this.trigger('focusout', name);
	},

	onKeyupInput: function (event) {
		var $target = $(event.currentTarget),
			name = $target.attr('name'),
			value = $target.val(),
			model = this.collection.find(function (model) {
				return model.get('name') === name;
			});

		if (value === '') {
			model.unset('excelRange');
		} else {
			model.set('excelRange', value? value.split(','): []);
		}
		this.validate(model);
	},

	onChangeExcelRange: function (model, value) {
		this.$('input[name="' + model.get('name') + '"]').val(value);
		this.validate(model);
	},

	validate: function (model) {
		var $input = this.$('input[name="' + model.get('name') + '"]'),
			hasRangeError, hasInvalidError;

		model.isValid();
		hasRangeError = (model.get('notEmpty') && !model.hasRange());
		hasInvalidError = (model.validationError === 'invalid-range');

		$input.siblings('p.validation-not-empty').toggleClass('hidden', !hasRangeError);
		$input.siblings('p.validation-invalid-range').toggleClass('hidden', !hasInvalidError);
		$input.toggleClass('has-error', hasInvalidError || hasRangeError);
	}
});
