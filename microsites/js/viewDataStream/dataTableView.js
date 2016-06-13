var dataTableView = function(options) {
	this.inheritedEvents = [];

	Backbone.View.call(this, options);
}

_.extend(dataTableView.prototype, Backbone.View.prototype, {

	// Extend functions

	baseEvents: {

		// Add Data Table events as Base Events
		'click #id_refreshButton, #id_retryButton': 'onRefreshButtonClicked',
		'click a[id^="id_changeParam"]': 'onChangeParamButtonClicked',

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
	
	// Data Table functions

	el: '#id_wrapper',	 
	
	template: null,

	$parameters: null,
	
	initialize: function() {

		this.parentView = this.options.parentView;
		this.dataStream = this.options.dataStream;

		$parameters = this.$el.find('a[id^="id_changeParam"]');
		this.template = _.template( $("#id_dataTableTemplate").html() );
		
		this.listenTo(this.model, "change:result", this.render);
	  
	  //When page, rows or dataStream's arguments change then invoke
	  var i=0;
		while(i < $parameters.size()){
			var name = 'parameter' + i;
			this.listenTo(this.dataStream, "change:"+name, this.invoke);
			i++;
		} 
	  
	  this.invoke();
	},
	
	render: function() {

		if (this.model.attributes.result.fType == 'LOADING') {
			this.setLoading()
		} else {
			var dataStream = this.dataStream.attributes;

			// Set Template
			var $result = this.$el.find('#id_datastreamResult > div')
			$result.html(this.template(this.model.attributes));

			// Set Max Width for Title
			this.setTitleMaxWidth();

			// If Array, Init Flexigrid
			if(this.model.attributes.result.fType == 'ARRAY'){

				// Trigger init on flexigrid to listenTo on plugins
				this.trigger('flexigrid-init', this.model.attributes.result);

				// Init flexigrid
				this.initFlexigrid(this.model.attributes.result);

			} else {
				this.setTableHeight();
			}
		}
	    return this;

	},

	setTitleMaxWidth: function(){

		$(document).ready(function(){

			$(window).resize(function(){

				var paramsWidth = 0;

				if( $parameters.length > 0 ){
					paramsWidth = 
						parseFloat( $('.dataTable header h1 .parameters').width() )
			    	- parseFloat( $('.dataTable header h1 .parameters').css('padding-left').split('px')[0] )
			    	+ 20;// Fix to perfection
				}

				var maxWidth = 
					parseFloat( $('.dataTable header h1').width() )
			    - paramsWidth;
			    
			  $('.dataTable header h1 strong').css('max-width',maxWidth+'px');

	  	}).resize();

		});

	},
	
	onChangeParamButtonClicked: function(event){

		var button = event.currentTarget;

		// If not disabled
		if( !$(button).parents('.parameters').hasClass('isDisabled') ){
			new changeDataStreamParametersView({model: new changeDataStreamParameters(), dataStream: this.dataStream});
		}
		
	},

	onRefreshButtonClicked: function(event){

		var button = event.currentTarget;

		// If not disabled
		if( !$(button).hasClass('isDisabled') ){
			this.dataStream.set('filter', '');
			this.invoke();
		}

	},

	updateParametersButtonsValues: function(){

		var dataStream = this.dataStream;

		var i=0;
		while(i < $parameters.size()){
			var name = 'parameter' + i;
			if(dataStream.hasChanged(name)){
				$parameters.eq(i).html(dataStream.get(name).value);
			}
			i++;
		}

	},

	invoke: function(){

		var params = [];
		
		// Add DataStream ID, Limit, Page
		params.push({
			name: 'limit',
			value: this.model.get("rows")
		},{
			name: 'page',
			value: this.model.get("page")
		});

		// Set flexigrid search to ''
		$('.flexigrid input[name=q]').val('');

		// Add the rest of the params
		$.merge( params, this.setPOSTParams() );
			
		var ajax = $.ajax({
			url: '/rest/datastreams/' + this.dataStream.get('datastream_revision_id') + '/data.json/', 
		  type:'GET', 
		  data: params, 
		  dataType: 'json', 
		  beforeSend: _.bind(this.onInvokeBeforeSend, this),
		  success: _.bind(this.onInvokeSuccess, this), 
		  error: _.bind(this.onInvokeError, this)
		});

	},

	onInvokeBeforeSend: function(){
	    this.updateParametersButtonsValues();
	    this.model.set('result', { fType: 'LOADING'})
	},
	
	onInvokeSuccess: function(response){
		this.model.set('result', response);
		if( !_.isUndefined( response.fTimestamp ) ){
			this.dataStream.set('timestamp', response.fTimestamp);
		}
	},
	
	onInvokeError: function(){

	},

	setLoading: function(){

		// Loading Template
		this.$el.find('#id_datastreamResult').html('<div class="result"><div class="loading">'+ gettext( 'APP-LOADING-TEXT' ) + '</div></div>');

		// Set Loading Height
		var self = this;

		$(document).ready(function(){
			
			var otherHeights = 
				parseFloat( $('.dataTable header').height() )
		    	+ parseFloat( $('.dataTable header').css('padding-top').split('px')[0] )
		    	+ parseFloat( $('.dataTable header').css('padding-bottom').split('px')[0] )
		    	+ parseFloat( $('.dataTable header').css('border-bottom-width').split('px')[0] )
		    	+ parseFloat( $('.dataTable .data').css('padding-top').split('px')[0] )
				+ parseFloat( $('.dataTable .data').css('padding-bottom').split('px')[0] )
				+ parseFloat( $('.dataTable #id_datastreamResult').css('border-top-width').split('px')[0] )
				+ parseFloat( $('.dataTable #id_datastreamResult').css('border-bottom-width').split('px')[0] );
				//+ 14;// Fix to perfection;

			self.parentView.setHeights('#id_datastreamResult .loading', otherHeights);

	  });

	},

	setTableHeight:function(){

		// Set Flexigrid Height
		var self = this;

	  $(document).ready(function(){

	  	var otherHeights = 
	  		parseFloat( $('.dataTable header').height() )
	    	+ parseFloat( $('.dataTable header').css('padding-top').split('px')[0] )
	    	+ parseFloat( $('.dataTable header').css('padding-bottom').split('px')[0] )
	    	+ parseFloat( $('.dataTable header').css('border-bottom-width').split('px')[0] )
	    	+ parseFloat( $('.dataTable .data').css('padding-top').split('px')[0] )
			+ parseFloat( $('.dataTable .data').css('padding-bottom').split('px')[0] )
			+ parseFloat( $('.dataTable #id_datastreamResult').css('border-top-width').split('px')[0] )
			+ parseFloat( $('.dataTable #id_datastreamResult').css('border-bottom-width').split('px')[0] );
			//+ 14;// Fix to perfection;

		  self.parentView.setHeights( '#id_datastreamResult .result table', otherHeights );

		});	

	},

	setFlexigridHeight: function(){
		
		var self = this;

		$(document).ready(function(){

			var otherHeights =
				parseFloat( $('.dataTable header').height() )
				+ parseFloat( $('.dataTable header').css('padding-top').split('px')[0] )
				+ parseFloat( $('.dataTable header').css('padding-bottom').split('px')[0] )
				+ parseFloat( $('.dataTable .data').css('padding-top').split('px')[0] )
				+ parseFloat( $('.dataTable .data').css('padding-bottom').split('px')[0] )
				+ parseFloat( $('.dataTable header').css('border-bottom-width').split('px')[0] )
				+ parseFloat( $('.flexigrid .hDiv').height() )
				+ parseFloat( $('.flexigrid .pDiv').height() )
				+ parseFloat( $('.flexigrid .pDiv').css('border-top-width').split('px')[0] )
				+ parseFloat( $('.flexigrid .pDiv').css('border-bottom-width').split('px')[0] )
				+ parseFloat( $('.dataTable #id_datastreamResult').css('border-top-width').split('px')[0] )
				+ parseFloat( $('.dataTable #id_datastreamResult').css('border-bottom-width').split('px')[0] );
				//+ 14;// Fix to perfection;

			self.parentView.setHeights( '.flexigrid div.bDiv', otherHeights );

		});	
		
	},

	initFlexigrid: function(result){

		var dataStream = this.dataStream.attributes,
			tableWidth = $('#id_datastreamResult > div').width(),
	    cellWidth = 150,
	    colModel = [],
	    searchArray = [],
	    self = this;

	  // Set cells width 
	  if( tableWidth / result.fCols > cellWidth ){
	  	if( !$.client.os == "Mac"){
	  		var scrollbar = 27; // 27 is the size of the scrollbar in windows XP, test with other browsers and OS
	  		tableWidth = tableWidth - scrollbar;
	  	} 	
	    cellWidth = tableWidth / result.fCols;
	  }

	  // Create Flexigrid colModel
		if(result.headerCells.length > 0){
			for (var j = 0; j < result.fCols; j++) {
				var col = {};
				col.display = result.headerCells[j];
				col.name = 'column'+j;
				col.width = cellWidth;
				col.sortable = true;
				col.align = 'center';
				colModel.push(col);
			}
		}else{
			var charCode 	= 65;
			for (var j = 0; j < result.fCols; j++) {
				var col = {};
				col.display = String.fromCharCode(charCode + j);
				col.name = 'column'+j;
				col.width = cellWidth;
				col.sortable = true;
				col.align = 'center';
				colModel.push(col);
			}
		}

		// Create Flexigrid search Items
		if(result.headerCells.length > 0){
			for (var j = 0; j < result.fCols; j++) {
				var col = {};
				if( j == 0 ){
					col.isdefault = true;
				}
				col.display = result.headerCells[j];
				col.name = 'column'+j;
				searchArray.push(col);
			}
		}else{
			var charCode 	= 65;
			for (var j = 0; j < result.fCols; j++) {
				var col = {};
				if( j == 0 ){
					col.isdefault = true;
				}
				col.display = String.fromCharCode(charCode + j);
				col.name = 'column'+j;
				searchArray.push(col);
			}
		}

		// Init Flexigrid
		$('.dataTable .data .result').flexigrid({
			url: '/rest/datastreams/' + dataStream.datastream_revision_id + '/data.grid/',
			dataType: 'json',
			colModel: colModel,
			searchitems : searchArray,
			autoload: false,
			sortname: "",
			sortorder: "asc",
			width: 'auto',
			//height: 'auto', // al dejarlo en auto se pisa con el seteo de altura que le hago segun la ventana.
			minheight: 400,
			usepager: true,
			useRp: true,
			rp: self.model.get('rows'),
			page: self.model.get('page') + 1,
			singleSelect: true,
			resizable: true,
			total: result.fLength,
			pages: Math.ceil( result.fLength / 50), //In the future, 50 should come from a Configuration
			method: 'GET',
			blockOpacity: 1,
			errormsg: gettext('VIEWDS-FLEXIGRID-ERRORMSG'),
			pagestat: gettext('VIEWDS-FLEXIGRID-PAGESTAT-1') + ' {from} ' 
					+ gettext('VIEWDS-FLEXIGRID-PAGESTAT-2') + ' {to} ' 
					+ gettext('VIEWDS-FLEXIGRID-PAGESTAT-3') + ' {total} ' + gettext('VIEWDS-FLEXIGRID-PAGESTAT-4'),
			pagetext: gettext('VIEWDS-FLEXIGRID-PAGETEXT'),
			outof: gettext('VIEWDS-FLEXIGRID-OUTOF'),
			findtext: gettext('VIEWDS-FLEXIGRID-FINDTEXT'),
			procmsg: gettext('VIEWDS-FLEXIGRID-PROCMSG'),
			nomsg: gettext('VIEWDS-FLEXIGRID-NOMSG'),
			onBeforeSend: function(settings){

				self.trigger('flexigrid-beforeSend', result);
				
				self.setFilterParams(settings);
				
				// Fix page
				settings.url = settings.url.replace(/(page=).*?(&)/, '$1' + (this.newp - 1).toString() + '$2')
				
				// Fix sort
				sortname = settings.url.match(/sortname=\d+/)
				sortorder = settings.url.match(/sortorder=\w+/)
				if (!_.isEmpty(sortname) && !_.isEmpty(sortorder) && sortname.length == 1 && sortorder.length == 1) {
					order_list = _.map(settings.url.match(/(orderBy\d+)/g), function(x){return parseInt(x.replace("orderBy", ""))})
					order = _.isEmpty(order_list)? 0: _.max(order_list) + 1
					settings.url += "&orderBy" + order + "=column" + sortname[0].split('=')[1] + "[" + sortorder[0].split('=')[1][0].toUpperCase() + "]"
				}

				// Fix query
				filter_column = settings.url.match(/qtype=\w+/)
				filter_text = settings.url.match(/query=\w+/)
				if (!_.isEmpty(filter_column) && !_.isEmpty(filter_text) && filter_column.length == 1 && filter_text.length == 1) {
					filter_order_list = _.map(settings.url.match(/(filter\d+)/g), function(x){return parseInt(x.replace("filter", ""))})
					filter_order = _.isEmpty(filter_order_list)? 0: _.max(filter_order_list) + 1
					if (filter_order == 0) {
						settings.url += "&filter" + filter_order + "=" + filter_column[0].split('=')[1] + "[contains]" + filter_text[0].split('=')[1]
					}
				}
				return true;

			},
			onSubmit: function(settings){

				self.trigger('flexigrid-submit', result);
			
				var params = [];

				// Add the rest of the params
				$.merge( params, self.setPOSTParams() );

				// Set Flex options
				$('.dataTable .data .result').flexOptions({
					params: params
				});	

				return true;

			},
			onSuccess: function(flexigridResponse, result){
				self.trigger('flexigrid-success', result);
			},
			onError: function(result){
				self.trigger('flexigrid-error', result);
			}
		});
	
		// Set Flexigrid Height
		//self.setTableHeight();
		this.setFlexigridHeight();

	},

	setPOSTParams: function(){	

		var params = [],	
			n = 0;

		// Add DataStream pArguments
		while(!_.isUndefined(this.dataStream.attributes['parameter'+n])){
			params.push({
				name: 'pArgument'+n,
				value: this.dataStream.attributes['parameter'+n].value
			});
			n++;					
		}

		return params;

	},

	setFilterParams: function(settings){

		var url = '';

		// Just flexigrid filter
		if( !_.isUndefined( settings ) ){
			var hash = settings.url.split('&'),
			obj = {};

			for(var i = 0; i < hash.length; i++){
				var kv = hash[i].split('=');
				obj[kv[0]] = kv[1];
			}

			if( obj.query != "" ){
				url = 'filter0='+encodeURIComponent(obj.qtype)+'[contains]'+encodeURIComponent(obj.query);
			}

		}

		if( url != ''){
			if( $parameters.length > 0 ){
				url = '&' + url;
			}else{
				url = '?' + url;
			}
		}

		this.dataStream.set('filter', url);

	},

});

dataTableView.extend = Backbone.View.extend;