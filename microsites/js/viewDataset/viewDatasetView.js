var viewDatasetView = Backbone.View.extend({
	el: "body",

	theDataTable: null,
		
	events:{
		'click #id_openInfoButton, #id_openNotesButton': 'onOpenSidebarButtonClicked',
		'click #id_closeInfoButton, #id_closeNotesButton': 'onCloseSidebarButtonClicked',
		'click #id_permalink, #id_GUID': 'onInputClicked'
	},
	
	initialize: function() {
		
		// Preload JS Images
		this.preloadImages();

		// init Sidebars
		this.initInfoSidebar();
		this.initNotesSidebar();
		this.initResourcesList();

		// Set resources list height
		this.setResourcesListHeight();

	},
	
	render: function(){
		return this;
	},	
	
	onOpenSidebarButtonClicked: function(event){

		var button = event.currentTarget;

		if( $(button).hasClass('active') ){

			this.onCloseSidebarButtonClicked();

		}else{

			$('.tabs .sidebarIcon').removeClass('active');
			
			$(button).addClass('active');

    	$('.sidebar .box').hide(0 ,function(){
	    	$('#'+button.rel).show(0, function(){
	        $('#id_columns').addClass('showSidebar');
	      });
    	});

    }

	},
   
	onCloseSidebarButtonClicked: function(){	
	  $('.tabs .sidebarIcon').removeClass('active');
	  $('#id_columns').removeClass('showSidebar');
	},
	
	initInfoSidebar: function(){

		// Set Height
		this.setSidebarHeight();

		// Permalink
		this.permalinkHelper();

		// Hits
		// new dataStreamHitsView({model: new dataStreamHits(), dataStream: this.model});

	},

	initNotesSidebar: function(){
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
				- parseFloat( otherHeight	)
		    - parseFloat( $('.brandingHeader').height() )
		    - parseFloat( $('.content').css('padding-top').split('px')[0] )
		    - parseFloat( $('.content').css('padding-bottom').split('px')[0] )
		    // - parseFloat( $('.brandingFooter').height() )
		    - parseFloat( $('.miniFooterJunar').height() );

		  $(heightContainer).height(height);

  	}).resize();

	},

	setSidebarHeight: function(){

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

	setResourcesListHeight: function(){

		var self = this;

		$(document).ready(function(){

			var otherHeights =
				parseFloat( $('.section .box').css('border-top-width').split('px')[0] )
				+ parseFloat( $('.section .box').css('border-bottom-width').split('px')[0] )
				+ parseFloat( $('.section .border-box').css('border-bottom-width').split('px')[0] )
				+ parseFloat( $('.section .border-box').css('padding-top').split('px')[0] )
				+ parseFloat( $('.section .border-box').css('padding-bottom').split('px')[0] )
				+ parseFloat( $('.section .border-box').height() );
			  		
			self.setHeights( '.section .resources-list', otherHeights );

		});

	},

	permalinkHelper: function(){

		var permalink = this.model.attributes.permaLink,
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

	onInputClicked: function(event) {

    var input = event.currentTarget;
    $(input).select();

  },

  setWaitingMessage: function(event){

  	var button = event.currentTarget,
  		titleText;

  	if( $(button).attr('id') == "id_downloadLink" ){
  		titleText = gettext("VIEWDS-WAITMESSAGEDOWNLOAD-TITLE");
  	}else{
  		titleText = gettext("VIEWDS-WAITMESSAGEEXPORT-TITLE");
  	}

  	$.gritter.add({
      title: titleText,
      text: gettext("VIEWDS-WAITMESSAGEDOWNLOAD-TEXT"),
      image: '/static/microsites/images/microsites/ic_download.gif',
      sticky: false,
      time: ''
    });

  },

  preloadImages: function(){

  	$(document).ready(function(){

  		// Images Array
		  var JSImages = [
		    '/static/microsites/images/microsites/ic_download.gif',
		    '/static/core/styles/plugins/images/gritter.png',
		    '/static/core/styles/plugins/images/ie-spacer.gif'
		  ];

		  // Preload JS Images
		  new preLoader(JSImages);
  		
  	});

  },

  initResourcesList: function(){

  }

});
