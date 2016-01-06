var viewVisualizationView = function(options) {
	this.inheritedEvents = [];

	Backbone.View.call(this, options);
}

_.extend(viewVisualizationView.prototype, Backbone.View.prototype, {
		
	// Extend functions

	baseEvents: {

		// Add View Visualization events as Base Events
		'click #id_embedButton' : 'onEmbedButtonClicked',
		'click #id_openInfoButton, #id_openAPIButton, #id_openNotesButton' : 'onOpenSidebarButtonClicked',
		'click #id_openNotesLink': 'onViewMoreDescriptionLinkClicked',
		'click #id_closeInfoButton, #id_closeAPIButton, #id_closeNotesButton': 'onCloseSidebarButtonClicked',
		'click #id_exportToXLSButton, #id_exportToCSVButton, #id_exportButton' : 'onExportButtonClicked',
		'click #id_permalink, #id_GUID' : 'onInputClicked',
		'click #id_downloadLink, #id_exportToXLSButton, #id_exportToCSVButton' : 'setWaitingMessage',
		'click #id_refreshButton, #id_retryButton' : 'onRefreshButtonClicked',

	},

	events: function() {
		var e = _.extend({}, this.baseEvents);

		_.each(this.inheritedEvents, function(events) {
			e = _.extend(e, events);
		});

		return e;
	},

	addEvents: function(eventObj) {
		this.inheritedEvents.push(eventObj);
		this.delegateEvents();
	},

	// viewVisualizationView functions

	el: "body",
	chartContainer: "#id_visualizationResult",

	initialize : function() {
		
		// Preload JS Images
		this.preloadImages();

		this.listenTo(this.model, "change:filter", this.updateExportsURL);

		// Init Visualization
		this.chartView = new ChartView({
			el: this.chartContainer,
			model: this.model
		});

		// Init Sidebars
		this.initSidebars();

		// Render
		this.render();

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

	loadDatatable: function(){
		this.theDataTable = new dataTableView({model: new dataTable(), dataStream: this.model, parentView: this});
	},

	setLoading : function() {
		var otherHeights =
			parseFloat( $('.dataTable header').height() )
			+ parseFloat( $('.dataTable header').css('padding-top').split('px')[0] )
			+ parseFloat( $('.dataTable header').css('padding-bottom').split('px')[0] )
			+ parseFloat( $('.dataTable header').css('border-bottom-width').split('px')[0] )
			+ 2;// Fix to perfection;

			this.setHeights(this.chartContainer + ' .loading', otherHeights);
			$(this.chartContainer).html('<div class="result"><div class="loading">'+ gettext('APP-LOADING-TEXT') + '</div></div>');
	},

	// setMiniLoading: function(){
	// 	$("#id_miniLoading").show();
	// },

	// unsetLoading: function(){
	// 	$("#id_miniLoading").hide();
	// },

	render : function() {
		this.chartView.render();
		//this.setChartContainerHeight();
		return this;
	},

	onEmbedButtonClicked : function() {

		new embedChartView({
			model : new embedChart({
				title: this.model.get("title"),
				url: this.model.get("embedUrl"),
			}, {
				validate : true
			})
		});
	},

	onViewMoreDescriptionLinkClicked: function(event){
		this.onOpenSidebarButtonClicked(event);
		this.toggleDescriptionLink();
	},

	toggleDescriptionLink: function(){
		var button = $('.dataTable header h2 .link'),
			tab = $('.tabs .sidebarIcon.notes'),
			viewMore = button.find('.viewMore'),
			viewLess = button.find('.viewLess');

		if( button.hasClass('active') ){
			tab.addClass('active');
			viewLess.show();
			viewMore.hide();
		}else{
			tab.removeClass('active');
			viewLess.hide();
			viewMore.show();
		}
	},

	onOpenSidebarButtonClicked : function(event) {

		var button = event.currentTarget;

		// If not disabled
		if( !$(button).hasClass('isDisabled') ){

			if( $(button).hasClass('active') ){

				this.onCloseSidebarButtonClicked(event);

			}else{

				$('.tabs .sidebarIcon').removeClass('active');
				
				$(button).addClass('active');

				// For preferences.account_description_enhancement
				if( $(button).attr('id') == 'id_openNotesButton' || $(button).attr('id') == 'id_openNotesLink' ){
					$('.dataTable header h2 .link').addClass('active');
					this.toggleDescriptionLink();
				}else{
					$('.dataTable header h2 .link').removeClass('active');
					this.toggleDescriptionLink();
				}

				// Hide all sidebars and show necesary one
				$('.sidebar .box').hide(0 ,function(){
					$('#'+button.rel).show(0, function(){
						$('#id_columns').addClass('showSidebar');
					});
				});

				this.trigger('open-sidebar', button);

			}

		}

	},

	onCloseSidebarButtonClicked : function(event) {

		var button = event.currentTarget;

		$('.tabs .sidebarIcon').removeClass('active');
		$('#id_columns').removeClass('showSidebar');

		// For preferences.account_description_enhancement
		$('.dataTable header h2 .link').removeClass('active');
		this.toggleDescriptionLink();

		this.trigger('close-sidebar', button);

	},

	onExportButtonClicked : function(event) {

		var button = event.currentTarget,
			itemHeight = parseInt( $('#'+button.rel).find('li a').height() ),
			itemLength = parseInt( $('#'+button.rel).find('li').length ),
			containerPaddingTop = parseInt( $('#'+button.rel).css('padding-top').split('px')[0] ),
			containerPaddingBottom = parseInt( $('#'+button.rel).css('padding-bottom').split('px')[0] ),
			marginTop = - ( ( ( itemHeight * itemLength ) + ( containerPaddingTop + containerPaddingBottom ) ) / 2 ) + 'px';

		// Set middle position of tooltip
		$('#'+button.rel).css('margin-top', marginTop );

		// Toggle Fade
		$('#'+button.rel).fadeToggle(375);

		// Toggle Active class
		$('#id_exportButton').toggleClass('active');

	},

	initSidebars: function(){

		var self = this;

		this.$('#id_columns .sidebar').on('transitionend webkitTransitionEnd', function (e) {
			self.handleVisualizationResize.call(self);
		});

		// init Sidebars
		this.initInfoSidebar();
		this.initAPISidebar();
		this.initNotesSidebar();

	},

	initInfoSidebar : function() {

		// Set Height
		this.setSidebarHeight();

		// Permalink
		this.permalinkHelper();

		// Hits
		new visualizationHitsView({model: new visualizationHits(), visualization: this.model});

	},

	initAPISidebar : function() {
		this.setSidebarHeight();
	},

	initNotesSidebar : function() {
		this.setSidebarHeight();
	},

	setHeights: function(theContainer, theHeight){

		if(typeof theHeight == 'undefined'){
			theHeight = 0;
		}

		var heightContainer = String(theContainer),
			tabsHeight = parseFloat( $('.tabs').height() ),
			otherHeight = theHeight,
			minHeight = tabsHeight - otherHeight;

		$(heightContainer).css('min-height', minHeight+ 'px');

		$(window).resize(function(){

			var height =
				parseFloat( $(window).height() )
				- parseFloat( otherHeight )
				- parseFloat( $('.brandingHeader').height() )
				- parseFloat( $('.content').css('padding-top').split('px')[0] )
				- parseFloat( $('.content').css('padding-bottom').split('px')[0] )
				// - parseFloat( $('.brandingFooter').height() )
				- parseFloat( $('.miniFooterJunar').height() );

			$(heightContainer).height(height);

		}).resize();

	},

	setSidebarHeight : function() {

		var self = this;

		$(document).ready(function(){

			var otherHeights =
				parseFloat( $('.sidebar .box').css('border-top-width').split('px')[0] )
				+ parseFloat( $('.sidebar .box').css('border-bottom-width').split('px')[0] )
				+ parseFloat( $('.sidebar .box .title').height() )
				+ parseFloat( $('.sidebar .box .title').css('border-bottom-width').split('px')[0] );
						
			self.setHeights( '.sidebar .boxContent', otherHeights );

		});

	},

	permalinkHelper: function(){
		var permalink = this.model.attributes.publicUrl,
		self = this;
		$('#id_permalink').val(permalink);

		if (typeof(BitlyClient) != 'undefined') {
			BitlyClient.shorten( permalink, function(pData){

				var response,
				  shortUrl;

				for(var r in pData.results) {
				response = pData.results[r];
				break;
				}

				shortUrl = response['shortUrl'];

				if(shortUrl){
				  self.model.attributes.shortUrl = shortUrl;
				  $('#id_permalink').val(shortUrl);
				}
		
			});
		}
	},

	onInputClicked : function(event) {
		var input = event.currentTarget;
		$(input).select();
	},

	setWaitingMessage : function(event) {

		var button = event.currentTarget, titleText;

		if ($(button).attr('id') == "id_downloadLink") {
			titleText = gettext("VIEWDS-WAITMESSAGEDOWNLOAD-TITLE");
		} else {
			titleText = gettext("VIEWDS-WAITMESSAGEEXPORT-TITLE");
		}

		$.gritter.add({
			title : titleText,
			text : gettext("VIEWDS-WAITMESSAGEDOWNLOAD-TEXT"),
			image : '/static/microsites/images/microsites/ic_download.gif',
			sticky : false,
			time : ''
		});

	},

	preloadImages : function() {

		$(document).ready(function(){

			// Images Array
			var JSImages = [
			'/static/microsites/images/microsites/ic_download.gif',
			'/static/core/styles/plugins/images/gritter.png',
			'/static/core/styles/plugins/images/ie-spacer.gif',
			'/static/microsites/images/microsites/im_miniLoading.gif'
			];

			// Preload JS Images
			new preLoader(JSImages);

		});

	},
			
	onRefreshButtonClicked : function() {
		this.render();
		// // by now only maps has an ajax function activated.
		// var chType = this.model.attributes.chart_type;
		// if (chType != "mapchart")
		// 	window.location.reload();
		// else {
		// 	this.setMiniLoading();
		// 	this.refreshData(true);
		// }
	},

	updateExportsURL: function(){

		var params = [],
			paramsQuery = '',
			filter = this.model.get('filter'),
			CSV = this.model.get('exportCSVURL'),
			XLS = this.model.get('exportXLSURL')

		if(params.length > 0){
			paramsQuery = params.join('');
		}

		// Update Export href Values
		$('#id_exportToCSVButton').attr('href',CSV+paramsQuery+filter);
		$('#id_exportToXLSButton').attr('href',XLS+paramsQuery+filter);

	},

	handleVisualizationResize: function () {
		var chartInstance = this.chartInstance,
			overflowX =  'hidden',
			overflowY =  'hidden',
			$mainHeader = $('.brandingHeader'),
			$chartHeader = $('.dataTable header');

		//Calcula el alto de los headers
		var otherHeights = $mainHeader.outerHeight(true) + $chartHeader.outerHeight(true);

		//Ajusta overflow si se está mostrando el sidebar		
		if( $('#id_columns').hasClass('showSidebar') ){
				overflowX = 'auto';
		}

		//Calcula el alto que deberá tener el contenedor del chart
		var height = this.$window.height() - otherHeights - 65, // fix. 65 ajusta el alto del chart
			tabsHeight = this.$el.find('#id_wrapper .tabs').height() - $chartHeader.outerHeight(true);

		// Min height para que no sea mas chico que las tabs
		if( height < tabsHeight ){
			height = tabsHeight;
		}

		this.chartView.$el.css({
			height: height + 'px',
			maxHeight: height + 'px',
			minHeight: height + 'px',
			overflowX: overflowX,
			overflowY: overflowY
		});
		this.render();
	},

});

viewVisualizationView.extend = Backbone.View.extend;
