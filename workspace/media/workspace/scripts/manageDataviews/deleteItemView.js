var DeleteItemView = Backbone.View.extend({
	
	el: '#id_deleteDataview',

	parentView: null,
	bulkActions: null,
	
	events: {
		"click #id_deleteResource": "deleteDataview",
		"click #id_deleteRevision": "deleteRevision"
	},

	initialize: function(options) {

		this.parentView = options.parentView;
        this.options=options;

		this.itemCollection = options.itemCollection;
		this.models = options.models;
		this.type = options.type;

        this.cant = this.models[0].attributes.cant;

		// Check if is a Bulk Actions Overlay
		if( _.isUndefined( options.bulkActions ) ){
			this.bulkActions = false;
		}else{
			this.bulkActions = options.bulkActions;
		}

		// Then, if is a Bulk Actions Overlay, change the el and $el
		if( this.bulkActions ){
			this.el = '#id_bulkDeleteDataview';
			this.$el = $( this.el );
		}

		// init Overlay
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
		
		// Render
		this.render();

	},

	render: function(){

        // oculta el boton de eliminar revisión actual
        if ( this.cant > 1 )
            $("#id_deleteRevision",this.$el).show();
        else
            $("#id_deleteRevision",this.$el).hide();

		this.$el.data('overlay').load();
	},

	deleteDataview: function() {
		var affectedResourcesCollection = new AffectedResourcesCollection();
		var affectedResourcesCollectionView = new AffectedResourcesCollectionView({
			collection: affectedResourcesCollection,
			itemCollection: this.itemCollection,
			models: this.models,
			type: this.type
		});
		this.parentView.resetBulkActions();
		this.closeOverlay();
		this.undelegateEvents();
	},

	deleteRevision: function() {
		self = this;
		_.each(this.models, function(model) {

			var resource = model.get('title');

			model.remove_revision({

				success: function(response, data) {
					$.gritter.add({
						title: gettext('APP-OVERLAY-DELETE-DATASTREAM-CONFIRM-TITLE'),
						text: resource + ": " + data.messages[0],
						image: '/static/workspace/images/common/ic_validationOk32.png',
						sticky: false,
						time: 3500
					});
					self.closeOverlay();
					self.undelegateEvents();
					self.itemCollection.fetch({
						reset: true
					});
				},

				error: function() {
					$.gritter.add({
						title: gettext('APP-DELETE-DATAVIEW-TEXT'),
						text: resource + ": " + gettext('APP-DELETE-DATASTREAM-ACTION-ERROR-TEXT'),
						image: '/static/workspace/images/common/ic_validationError32.png',
						sticky: true,
						time: 2500
					});
					self.closeOverlay();
					self.undelegateEvents();
				}

			});
			self.parentView.resetBulkActions();

		});

	},

	closeOverlay: function() {
		$("#ajax_loading_overlay").hide();
		this.$el.data('overlay').close();
	}
});
