var dataTableView = Backbone.View.extend({

	el: '.detail',	 
	
	template: null,
	parentView: null,
	
	events:{
		'click a[id^="id_changeParam"]': 'onChangeParamButtonClicked',
	},

	$parameters: null,
	
	initialize: function(options) {

		this.parentView = options.parentView;
		this.dataStream = options.dataStream;

		$parameters = this.$el.find('a[id^="id_changeParam"]');
		this.template = _.template( $("#id_dataTableTemplate").html() );
		this.listenTo(this.model, "change:result", this.render);
	  
	  //When page, rows or dataStream's arguments change then invoke
	  this.listenTo(this.model, "change:page", this.invoke); 
	  this.listenTo(this.model, "change:rows", this.invoke);		
	  var i=0;
		while(i < $parameters.size()){
			var name = 'parameter' + i;
			this.listenTo(this.dataStream, "change:"+name, this.invoke);
			i++;
		} 
	  
	  this.invoke();
	},
	
	render: function() {

		var dataStream = this.dataStream.attributes;

		// Set Template
		this.$el.find('#id_datastreamResult > div').html(this.template(this.model.attributes));

		// If Array, Init Flexigrid
		if(this.model.attributes.result.fType == 'ARRAY'){
			this.initFlexigrid(this.model.attributes.result);
		}else{
			this.setTableHeight();
		}

    return this;

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

		var dataStream = this.dataStream.attributes;

	  var data = "&limit=" + this.model.get("rows") + "&page=" + this.model.get("page");

	  // Add DataStream pArguments
	  var params = [],
			n = 0;

		while( dataStream['parameter' + n ] != undefined ){
			params.push('&pArgument' + n + '=' + dataStream['parameter'+n].value);
			n++;					
		}

		if(params.length > 0){
			data += params.join('');
		}
	    
	  var ajax = $.ajax({ 
			url: '/rest/datastreams/' + dataStream.id + '/data.json', 
		  type:'GET', 
		  data: data, 
		  dataType: 'json', 
		  beforeSend: _.bind(this.onInvokeBeforeSend, this),
		  success: _.bind(this.onInvokeSuccess, this), 
		  error: _.bind(this.onInvokeError, this)
	  });

	},

	onInvokeBeforeSend: function(xhr, settings){

		// Prevent override of global beforeSend
		$.ajaxSettings.beforeSend(xhr, settings);

    this.updateParametersButtonsValues();
    this.setLoading();
	},
	
	onInvokeSuccess: function(response){
		//HERE IS SET THE DATA
		this.model.set('result', response);
	},
	
	onInvokeError: function(){

	},

	setLoading: function(){

		// Loading Template
		this.$el.find('#id_datastreamResult').html('<div class="result"><div class="loading">'+ gettext( 'APP-LOADING-TEXT' ) + '</div></div>');

		// Set Loading Height
		this.setLoadingHeight();

	},

	setLoadingHeight: function(){
		var self = this;

		$(document).ready(function(){
			
			var otherHeights = 0;

			self.parentView.setHeights('#id_datastreamResult .loading', otherHeights);

		});
	},

	setTableHeight:function(){

		// Set Flexigrid Height
		var self = this;

	  $(document).ready(function(){

	  	var otherHeights = 0;

		  self.parentView.setHeights( '#id_datastreamResult .result table', otherHeights );

		});	

	},

	initFlexigrid: function(result){

		var dataStream = this.dataStream.attributes,
			tableWidth = $('#id_datastreamResult > div').width(),
	    cellWidth = 100,
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

	  // TODO: CHECK PROBLEM WHEN SIDEBAR IS OPENED
	  // Remove Horizontal Scroll if not needed
	  //if( cellWidth * result.fCols <= tableWidth ){
	    //$('.dataTable .data').addClass('noHorizontalScroll');
	  //} 

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
			url: '/rest/datastreams/' + dataStream.lastPublishRevisionId + '/data.grid',
			dataType: 'json',
			colModel: colModel,
			searchitems : searchArray,
			autoload: false,
			sortname: "",
			sortorder: "asc",
			width: 'auto',
			height: 'auto',
			minheight: 400,
			usepager: true,
			useRp: true,
			page: self.model.get('page') + 1,
			rp: self.model.get('rows'),
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
				
				self.setFilterParams(settings);
				settings.url = settings.url.replace(/(page=).*?(&)/, '$1' + (this.newp - 1).toString() + '$2')
				sortname = settings.url.match(/sortname=\d+/)
				sortorder = settings.url.match(/sortorder=\w+/)
				if (!_.isEmpty(sortname) && !_.isEmpty(sortorder) && sortname.length == 1 && sortorder.length == 1) {
					order_list = _.map(settings.url.match(/(orderBy\d+)/g), function(x){return parseInt(x.replace("orderBy", ""))})
					order = _.isEmpty(order_list)? 0: _.max(order_list) + 1
					settings.url += "&orderBy" + order + "=column" + sortname[0].split('=')[1] + "[" + sortorder[0].split('=')[1][0].toUpperCase() + "]"
				}
				return true;

			},
			onSubmit: function(){
				
				var params = [];
				var n = 0;
				// Add DataStream pArguments
				while(!_.isUndefined(dataStream['parameter'+n])){
					params.push({
						name: 'pArgument'+n,
						value: dataStream['parameter'+n].value
					});
					n++;					
				}

				// Set Flex options
				$('.dataTable .data .result').flexOptions({
					params: params
				});	

				return true;

			},
			onSuccess: function(result){
			    console.log('OK');
			    console.log(result);
			},
			onError: function(result){				
    			console.log('ERROR');
    			console.log(result);
			}
		});
	
		// Set Flexigrid Height
	  $(document).ready(function(){

	  	var otherHeights = 
	  		+ parseFloat( $('.section-content').css('padding-top').split('px')[0] )
	  		+ parseFloat( $('.flexigrid .hDiv').height() )
		    + parseFloat( $('.flexigrid .pDiv').height() )
		    + parseFloat( $('.flexigrid .pDiv').css('border-top-width').split('px')[0] )
		    + parseFloat( $('.flexigrid .pDiv').css('border-bottom-width').split('px')[0] );

		  self.parentView.setHeights( '.flexigrid div.bDiv', otherHeights );

		});	

	},

	setFilterParams: function(settings){

		var hash = settings.url.split('?')[1],
			split = hash.split('&'),
			obj = {};

		for(var i = 0; i < split.length; i++){
			var kv = split[i].split('=');
			obj[kv[0]] = kv[1];
		}

		var url = '';

		if( obj.query != "" ){

			url = 'pFilter0='+encodeURIComponent(obj.qtype)+'[contains]'+encodeURIComponent(obj.query);

			if( $parameters.length > 0 ){
				url = '&' + url;
			}else{
				url = '?' + url;
			}

		}

		this.dataStream.set('filter', url);


	},

});