var ViewDataStreamView = Backbone.Epoxy.View.extend({

	el: '.main-section',

	theDataTable: null,
	listResources: null,
	sourceUrl: null,
	tagUrl: null,
	datastreamEditItemModel: null,

	events: {
		'click #id_delete': 'onDeleteButtonClicked',
		'click #id_unpublish': 'onUnpublishButtonClicked',
		'click #id_approve, #id_reject, #id_publish, #id_sendToReview': 'changeStatus',
		'click #id_publish_all': 'onPublishAllClicked',
		"click #id_edit": "onEditButtonClicked",
	},

	initialize: function(options){
		this.template = _.template( $("#context-menu-template").html() );
		this.listenTo(this.model, "change", this.render);
		this.theDataTable = new dataTableView({model: new dataTable(), dataStream: this.model, parentView: this});
		this.render();

		this.sourceUrl = options.sourceUrl;
		this.tagUrl = options.tagUrl;
		this.datastreamEditItemModel = options.datastreamEditItemModel;

		// Init Filters
		this.initFilters();
	},

	render: function(){
		this.$el.find('.context-menu').html( this.template( this.model.toJSON() ) );
		return this;
	},

	setHeights: function(theContainer, theHeight){

		if(typeof theHeight == 'undefined'){
			theHeight = 0;
		}

		var heightContainer = String(theContainer),
			otherHeight = theHeight;

		$(window).resize(function(){

			var windowHeight;
			if( $(window).height() < 600){
				// Set window height minimum value to 600
				windowHeight = 600;
			}else{
				windowHeight = $(window).height();
		 	}

			var sectionContentHeight =
				windowHeight
				- parseFloat( otherHeight	)
				- $('.global-navigation').height()
				- $('.main-section .section-title').height()
				- parseFloat( $('.main-section .section-content').css('padding-top').split('px')[0] );
				- parseInt($('.main-section .section-content .detail').css('padding-top').split('px')[0])
				- parseInt($('.main-section .section-content .detail').css('padding-bottom').split('px')[0])
				- 20; // to set some space at the bottom

			$(heightContainer).css('height', sectionContentHeight+'px');

		}).resize();

	},  

	onPublishAllClicked: function(event){
       	this.publishChildResources = new Array();
       	this.publishChildResources.push(this.model);
       	var affectedResourcesCollection = new AffectedResourcesCollection();
        var affectedResourcesCollectionPublishView = new AffectedResourcesCollectionPublishItemView({
            collection: affectedResourcesCollection,
            models: this.publishChildResources,
            type: "datastreams",
            parentView: this
        });
    },

	changeStatus: function(event, killemall){

		if( _.isUndefined( killemall ) ){
			var killemall = false;
		}else{
			var killemall = killemall;
		}

		var action = $(event.currentTarget).attr('data-action'),
			data = {'action': action},
			url = this.model.get('changeStatusUrl'),
			self = this;

		if(action == 'unpublish'){
			var lastPublishRevisionId = this.model.get('lastPublishRevisionId');
			url = '/dataviews/change_status/'+lastPublishRevisionId+'/';
			data.killemall = killemall;
		}

		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			dataType: 'json',
			beforeSend: function(xhr, settings){
				// Prevent override of global beforeSend
				$.ajaxSettings.beforeSend(xhr, settings);
				// Show Loading
				$("#ajax_loading_overlay").show();
			},
			success: function(response){

				if(response.status == 'ok'){

					// Update some model attributes
					self.model.set({
						'status_str': STATUS_CHOICES( response.result.status ),
						'status': response.result.status,
						'lastPublishRevisionId': response.result.last_published_revision_id,
						'lastPublishDate': response.result.last_published_date,
						'publicUrl': response.result.public_url,
						'modifiedAt': response.result.modified_at,
					});

                    self.datastreamEditItemModel.set({
                        'status': response.result.status,
                    });

					// Set OK Message
					$.gritter.add({
						title: response.messages.title,
						text: response.messages.description,
						image: '/static/workspace/images/common/ic_validationOk32.png',
						sticky: false,
						time: 2500,
						after_close: function () {
							window.location.reload();
						}
					});

				}else{

					datalEvents.trigger('datal:application-error', response);

				}

			},
			error:function(response){
				response.onClose = function(){ window.location.reload(true)}; 
				datalEvents.trigger('datal:application-error', response);
				$("#ajax_loading_overlay").hide();
			}
		});

	},

	updateHeights: function(){
			
		// Update Sidebar Height
		this.setSidebarHeight();

		// Update Table Height
		if(this.theDataTable.model.attributes.result.fType == 'ARRAY'){
			if( $('.flexigrid').length == 0 ){
				var self = this;
				setTimeout(function(){
					self.updateHeights();
				}, 1000);
			}else{
				this.theDataTable.setFlexigridHeight();
			}
		}else{
			this.theDataTable.setTableHeight();
		}

		// Update Loading Height
		this.theDataTable.setLoadingHeight();

	},

	initFilters: function(){

		// Init Backbone PageableCollection
		this.listResources = new ListResources({
			filters: this.filters
		});

	},

	onDeleteButtonClicked: function(){
		self = this;
		this.deleteListResources = new Array();
		this.deleteListResources.push(this.model);
		var deleteItemView = new DeleteItemView({
			models: this.deleteListResources,
			type: "visualizations"
		});
	},

	onUnpublishButtonClicked: function(){
		this.unpublishListResources = new Array();
		this.unpublishListResources.push(this.model);
		var unpublishView = new UnpublishView({
				models: this.unpublishListResources,
				type: "visualizations",
				parentView: this
		});
	},

	onEditButtonClicked: function(event){
		new DatastreamEditItemView({
			model: this.datastreamEditItemModel,
			parentView: this
		});
	},

});
