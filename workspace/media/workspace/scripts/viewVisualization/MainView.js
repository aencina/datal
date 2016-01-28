var MainView = Backbone.View.extend({

	el : ".main-section",

	events: {
		'click #id_delete': 'onDeleteButtonClicked',
		'click #id_unpublish': 'onUnpublishButtonClicked',
		'click #id_approve, #id_reject, #id_publish, #id_sendToReview': 'changeStatus',
	},

	chartContainer: "#id_visualizationResult",

	initialize : function() {

		this.template = _.template( $("#context-menu-template").html() );

		this.$('.visualizationContainer .loading').removeClass('hidden');

		this.listenTo(this.model, "change", this.render);

		this.chartView = new ChartView({
			el: '#id_visualizationResult',
			model: this.model
		});
		this.setChartContainerSize();
		this.render();
        this.listenTo(this.model.data, 'fetch:start', this.onFetchStart, this);
        this.listenTo(this.model.data, 'fetch:end', this.onFetchEnd, this);
        this.chartView.render();
	},

	render: function () {
		this.$el.find('.context-menu').html( this.template( this.model.toJSON() ) );
		return this;
	},

	setLoading: function () {
		
		var height = this.$el.find('#id_visualizationResult').height();

		this.$el.find('#id_visualizationResult .loading').height(height);

	},

	setChartContainerSize:function(){
		var chartInstance = this.chartView.chartInstance,
			container = $(this.chartContainer),
			$window = $(window),
			$mainHeader = $('header.header'),
			$title = $('.main-section .section-title'),
			$chartHeader = $('header.header'),
			self = this;

		var handleResizeEnd = function () {
			//Calcula el alto de los headers
			var otherHeights = $mainHeader.outerHeight(true) 
							 + $title.outerHeight(true)
							 + $chartHeader.outerHeight(true);
			//Calucla el alto que deberá tener el contenedor del chart
			var minHeight = $window.height() - otherHeights - 30;
			container.css({
				height: minHeight + 'px'
			});
			//chartInstance.render();
			self.setLoading();
		}

		//Calcula el tamaño inicial
		handleResizeEnd();

		//Asigna listener al resize de la ventana para ajustar tamaño del chart
		$window.on('resize', function () {
			if(this.resizeTo) clearTimeout(this.resizeTo);
			this.resizeTO = setTimeout(function() {
				handleResizeEnd();
			}, 500);
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
			url = 'change_status/'+lastPublishRevisionId+'/';
			data.killemall = killemall;
		}

		var self = this;

		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			dataType: 'json',
			beforeSend: function(xhr, settings){
				// Prevent override of global beforeSend
				$.ajaxSettings.beforeSend(xhr, settings);
				// Show Loading
				self.$('.visualizationContainer .loading').removeClass('hidden');
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
						time: 2500
					});

				}else{
					response.onClose = function(){ window.location.reload(true)}; 
					datalEvents.trigger('datal:application-error', response);
				}

			},
			error:function(response){
				datalEvents.trigger('datal:application-error', response);
				self.$('.visualizationContainer .loading').addClass('hidden');
			},
			complete:function(response){
				// Hide Loading
				self.$('.visualizationContainer .loading').addClass('hidden');
			}
		}).fail(function () {
			self.$('.visualizationContainer .loading').addClass('hidden');
		});

	},

	onDeleteButtonClicked: function(){
		this.deleteListResources = new Array();
		this.deleteListResources.push(this.model);
		var deleteItemView = new DeleteItemView({
			models: this.deleteListResources
		});
	},

	onUnpublishButtonClicked: function(){
		this.unpublishListResources = new Array();
		this.unpublishListResources.push(this.model);
		var unpublishView = new UnpublishView({
			models: this.unpublishListResources,
			parentView: this
		});
	},

    onFetchStart: function () {
        this.$('.visualizationContainer .loading').removeClass('hidden');
    },

    onFetchEnd: function () {
        this.$('.visualizationContainer .loading').addClass('hidden');
    }
});