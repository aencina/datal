var EditArgumentOverlayView = Backbone.View.extend({

	events:{
		'click a.btn-accept': 'onClickAccept',
		'click a.btn-cancel': 'onClickCancel',
	},

	initialize: function() {
		this.template = _.template( $('#edit_arguments_overlay_template').html() );

		this.listenTo(this.model, "invalid", this.onValidationErrors);

		this.$el.overlay({
			top: 'center',
			left: 'center',
			mask: {
				color: '#000',
				loadSpeed: 200,
				opacity: 0.5,
				zIndex: 99999
			}
		});
	},

	render: function() {
		this.$el.find('#id_editParamsForm').html(
			this.template({
				arg: this.model.toJSON()
			})
		);
			
		this.$el.data('overlay').load();
	},

	onValidationErrors: function(){

	},

	onClickAccept:function(){
		var value = this.$el.find('#id_editParamsForm input[name=param]').val();
		this.model.set('value', value);

		if (this.model.isValid()) {
			this.$el.data('overlay').close();
		};
	},

	onClickCancel:function(){
		this.$el.data('overlay').close();
	}

});