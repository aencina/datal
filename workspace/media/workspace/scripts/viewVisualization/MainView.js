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
		
		// Render context menu
		this.render();
        
        this.listenTo(this.model.data, 'fetch:start', this.onFetchStart, this);
        this.listenTo(this.model.data, 'fetch:end', this.onFetchEnd, this);
        
        // Render visualiztion
        this.renderVisualization();

        // Handle Visualization Resize
		this.bindVisualizationResize();
		this.handleVisualizationResize();

	},

	bindVisualizationResize: function () {

		var self = this;
		this.$window = $(window);

		this.$window.on('resize', function () {
			if(this.resizeTo) clearTimeout(this.resizeTo);
			this.resizeTo = setTimeout(function() {
				self.handleVisualizationResize.call(self);
			}, 500);
		});

	},

	render: function () {
		this.$el.find('.context-menu').html( this.template( this.model.toJSON() ) );
		return this;
	},

	renderVisualization: function(){
		this.setLoading();
        this.chartView.render();
	},

	setLoading: function () {
		
		if( this.chartView.model.get('type') === 'mapchart' ){

			// Set mini loading

		}else{

			var height = this.$el.find('#id_visualizationResult').height();

			this.$el.find('#id_visualizationResult .loading').height(height);

		}

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
    },

    handleVisualizationResize: function() {
		var $mainHeader = $('header.header'),
			$sectionTitle = $('.main-section .section-title'),
			$sectionContent = $('.main-section .section-content'),
			$detail = $('.section-content > .detail');

		//Calcula el alto de los headers
		var otherHeights = 
			$mainHeader.outerHeight(true) + 
			$sectionTitle.outerHeight(true) +
			parseFloat( $sectionContent.css('padding-top').split('px')[0] ) +
			parseFloat( $sectionContent.css('padding-bottom').split('px')[0] ) +
			parseFloat( $detail.css('padding-top').split('px')[0] ) +
			parseFloat( $detail.css('padding-bottom').split('px')[0] ) + 
			15; // 15 redondea el espacio que quiero mantener abajo

		//Calcula el alto que deberá tener el contenedor del chart
		var height = this.$window.height() - otherHeights;

		// Aplico nueva altura al contenedor de la visualizacion
		this.chartView.$el.css({
			height: height + 'px',
			maxHeight: height + 'px',
			minHeight: height + 'px',
			overflowX: 'hidden',
			overflowY: 'hidden'
		});

		// Rendereo la visualizacion a la nueva altura
		this.renderVisualization();
	}

});