var datasetView = Backbone.Epoxy.View.extend({

	el: '.main-section',
	deleteListResources: null,

	template: null,

	events: {
		'click #id_delete': 'onDeleteButtonClicked',
		'click #id_approve, #id_reject, #id_publish, #id_sendToReview': 'changeStatus',
		'click #id_unpublish': 'onUnpublishButtonClicked'
	},

	initialize: function(){
		this.template = _.template( $("#context-menu-template").html() );
		this.listenTo(this.model, "change", this.render);
		this.onTabActive();
		this.render();
	},

	render: function() {
		this.$el.find('.context-menu').html( this.template( this.model.toJSON() ) );
		return this;
	},

	onTabActive:function() {
		var $dataTabs;
	    $dataTabs = $(".detail").hashTabs({
	      smoothScroll: {
	        enabled: true,
	        initialTabId: "smooth-scroller"
	      }
	    });
	},

	onDeleteButtonClicked: function(){
		this.deleteListResources = new Array();
		this.deleteListResources.push(this.model);
		var deleteItemView = new DeleteItemView({
				models: this.deleteListResources,
				type: "datastreams"
		});
	},

	onUnpublishButtonClicked: function(){
		this.unpublishListResources = new Array();
		this.unpublishListResources.push(this.model);
		var unpublishView = new UnpublishView({
				models: this.unpublishListResources,
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
			url = '/datasets/change_status/'+lastPublishRevisionId+'/';
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
					response.onClose = function(){ window.location.reload(true)}; 
					datalEvents.trigger('datal:application-error', response);
				}

			},
			error:function(response){

				datalEvents.trigger('datal:application-error', response);

			},
			complete:function(response){
				// Hide Loading
				$("#ajax_loading_overlay").hide();
			}
		});

	},


});
