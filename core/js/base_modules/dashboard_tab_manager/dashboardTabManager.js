var dashboardTabManager = Backbone.Model.extend({
	defaults : {
		$Tabs : null,
		container : null,
		isDragging : false,
		currentSelectedId : 0,
		startingIndex: 0,
		disable : false,
		dashboardId : ''
	},
	initialize : function(){
		var _self 	= this;
		var att		= _self.attributes;
		var hash 	= window.location.hash;
		
		att.container = $('#id_dashboard_container');
		att.$Tabs = $('#sortable');
		
		att.$Tabs.click(_.bind(this.onTabClicked, this));
		
		_self.initializeDashboard();
		
		if(hash.indexOf("dashboardid") != -1){
			_self.initializeHashTag(hash.split("=")[1]);
		}else if(att.dashboardId != ''){
			this.setSelectedTab(null, att.dashboardId);
			this.loadTab(att.dashboardId);
		}else{
			if($('#sortable li').size() == 0){
	            $('#id_comment_container').hide();
				this.loadNewTab();
	        }else{
				var $Tab = att.$Tabs.find('li').eq(0);
				this.setSelectedTab($Tab, $Tab.data("dashboard_id"));
				this.loadTab($Tab.data("dashboard_id"));
			}
		}
	}, 
	initializeHashTag : function(pDashboardId){
		this.setSelectedTab(null, pDashboardId);
		this.loadTab(pDashboardId);
	},
	initializeDashboard : function(){
		var att = this.attributes;
		
		$('#id_editFavouriteDashboardsButton').click( _.bind(this.onNewTabClicked, this));
		
		if(att.disable){
			$('#id_editFavouriteDashboardsButton').remove();
			$('[id*=id_removeFavouriteDashboardButton_]').remove()
		}
		
		if(!att.disable){
			att.$Tabs.sortable({
				handle: '.handle',
				forcePlaceholderSize: true,
				revert: false,
				tolerance: 'intersect',
				placeholder: "ui-state-highlight",
				cancel: '.no-selector',
				update: _.bind(this.onTabDropped, this),
				start: function(pEvent, pUI){
					att.isDragging = true;
					att.startingIndex = $(pUI.item).data('index');
					$(pUI.item).find('.icClose').css({
							position: 'absolute',
							top: 0,
							right: 0
					});
					eWidth = $(pUI.item).width();
					$(pUI.item).parent().find('.ui-state-highlight').width(eWidth+4);
				},
				stop: function(pEvent, pUI){
					$(pUI.item).find('.icClose').css({
							position: 'relative',
							top: 'auto',
							right: 'auto'
					});
					setTimeout(function(){
						att.isDragging = false;
					}, '1');
				}
			});
		}	
		
		att.$Tabs.disableSelection();
	},
	onTabClicked : function(pEvent){
	    pEvent.preventDefault();
		var _self 			= this;
		var $Target 		= $(pEvent.target);
		var lDashboardId 	= '';
		var lFavouriteId 	= '';
		var lTab 			= null;
		
		if($Target.is('a')){
			lTab = $Target.parent().parent();
			lDashboardId = lTab.data("dashboard_id");
			lFavouriteId = lTab.data("favourite_dashboard_id");
			fUserNick = lTab.data("user_nick");
		}
		if ($Target.hasClass('handle')) {
			if(!_self.attributes.isDragging && lDashboardId != _self.attributes.currentSelectedId){
				ajaxManager.killAll();
				_self.setSelectedTab(lTab, lDashboardId);
				_self.loadTab(lDashboardId);
			}
		}
		if ($Target.hasClass('icClose')) {
			_self.removeTab(lFavouriteId, lTab);
		}
	},
	onNewTabClicked : function(pEvent){
		this.loadNewTab();
	},
	loadNewTab : function(){
		var $lButton     = $('#id_editFavouriteDashboardsButton');
	    var lUrl         = Configuration.baseUri + "/portal/DashboardsManager/actionAddTab/";
	
	    $fEditFavouriteDashboardsContainer.show();
	    $fEditDashboardDataServicesContainer.hide();
	    startWaitMessage($fEditFavouriteDashboardsContainer);
		
		this.setSelectedTab($lButton.parent().parent(), 0);
		
	    $.ajax({ url: lUrl
	            , type:'GET'
	            , dataType: 'html'
	            , success: function(pData){
                    $fEditFavouriteDashboardsContainer.html(pData);
                    var createDB = new CreateDashboard({'$Container' : $('#id_dashboard_container')});
                    initEditPanel();
					$( '[id*=id_followThatDashboard_]' ).click( onFollowThatDashboardButtonClicked );
                }
	    });
	
	    ajaxManager.killAll();
	},
	loadTab : function(pDashboardId){
		fDashboardId = pDashboardId;
        var lUrl 	= '/portal/DashboardsManager/actionSwitchDashboard/';
        var lData 	= "dashboard_id=" + pDashboardId;
		var $Container = this.attributes.container;
		
		$fEditFavouriteDashboardsContainer.hide();
	    $fEditDashboardDataServicesContainer.show();
				
        $Container.html('');
        startWaitMessage($Container);

        var lajaxCall = $.ajax({ url: lUrl
                                , type:'GET'
                                , data: lData
                                , dataType: 'html'
                                , success: _.bind(this.onSuccessTabLoaded,this)
                                , error: _.bind(this.onErrorTabLoaded, this)
                                }
                        );

        ajaxManager.register( pDashboardId, lajaxCall );
	},
	onSuccessTabLoaded : function(pResponse){
		this.attributes.container.html(pResponse);
        $('#id_editFavouriteDashboardsPanelHideButton:visible').trigger('click');
		
        $fPersonalizeDashboardContainer = $("#id_personalize_dashboard_container");
        $fPersonalizeDashboardContainer.hide();

        $('#id_editFavouriteDashboardsPanelHideButton:visible').trigger('click');

        $fEditDashboardCommentsContainer = $('#id_edit_dashboard_comments_container');
		
        initDashboardPanel();
	},
	onErrorTabLoaded : function(pResponse){
		var lMessage = pResponse.status + ':' + pResponse.statusText;
	},
	onTabDropped : function(pEvent, pUI){
		var new_position    = pUI.item.index();
        var lDraggable      = $( pUI.item )[0];
        var lDraggableId    = lDraggable.id;
		
        var lDashboardContainerId    = $( '#'+lDraggableId ).attr( "rel" );
        var lDashboardContainer      = $( lDashboardContainerId )[0];

        var lIndex = pUI.item.index();

        var lId     = jQuery.data( lDraggable, "favourite_dashboard_id");
        var lFrom   = jQuery.data( lDraggable, "order");
        var lTo;

        if( this.attributes.startingIndex > lIndex ){
            lTo = parseInt(lFrom) - ( parseInt(this.attributes.startingIndex) - lIndex );
        }

        if( this.attributes.startingIndex < lIndex ){
            lTo = parseInt(lFrom) + ( parseInt(lIndex) - this.attributes.startingIndex );
        }

        if( this.attributes.startingIndex == lIndex ){
            lTo = parseInt(lIndex);
        }

        this.updateTabPosition(lId, lFrom, lTo);
	},
	updateTabPosition : function(pId, pFrom, pTo){
		var lUrl 	= Configuration.baseUri + '/portal/DashboardsManager/actionMoveFavouriteDashboard/';
        var lData 	= "id=" + pId
                        + "&from=" + pFrom
                        + "&to=" + pTo;

        $.ajax({ url: lUrl
                , type:'GET'
                , data: lData
                , dataType: 'json'
                , error: _.bind(this.onTabUpdateError, this)
		});
	},
	onTabUpdateError : function(pResponse){
		// callback in case updating tab method fails
	},
	removeTab : function(pFavouriteId, pTab){
		var lUrl 	= Configuration.baseUri + '/portal/DashboardsManager/actionRemoveFavouriteDashboard/';
        var lData 	= "favourite_dashboard_id=" + pFavouriteId;
		
        $.ajax({ url: lUrl
                , type:'GET'
                , data: lData
                , dataType: 'json'
                , success: _.bind(this.onSuccessTabRemoved, this)
                , error: _.bind(this.onErrorTabRemoved, this)
                }
        );
		
		var oldDashboardId = pTab.data("dashboard_id");
		pTab.remove();
		
		if(this.attributes.currentSelectedId == oldDashboardId){
			ajaxManager.killAll();
			var $Tabs = this.attributes.$Tabs.find('li')
			if($Tabs.size() != 0){
				var $Tab = $Tabs.eq(0);
				var dashboardId = $Tab.data("dashboard_id");
				this.setSelectedTab($Tab, dashboardId);
				this.loadTab(dashboardId);
			}else{
				this.loadNewTab();
			}
		}
	},
	onSuccessTabRemoved : function(pResponse){
		//what to do here?
	},
	onErrorTabRemoved : function(pResponse){
		//review error message display
	},
	setSelectedTab : function(pTab, pDashboardId){
		var lTab = null;
		if(pTab == null){
			var lTabs = $('#sortable li');
			for (var i = 0; i < lTabs.size(); i++){
				if(pDashboardId == lTabs.eq(i).data("dashboard_id")){
					lTab = lTabs.eq(i);
					break;
				}
			};	
		}else{
			lTab = pTab;
		}
		
		if(lTab == null){
			this.setDefaultTab();
		}else{
			$('.tab-selected').removeClass('tab-selected');
			lTab.addClass('tab-selected');
			this.attributes.currentSelectedId = pDashboardId;
		}
	},
	setDefaultTab : function(){
		var _self = this;
		var $Tabs = _self.attributes.$Tabs.find('li');
		if($Tabs.size() > 0){
			var $Tab = $Tabs.eq(0);
			var lDashboardId = $Tab.data("dashboard_id");
			//_self.setSelectedTab($Tab, lDashboardId);
			_self.loadTab(lDashboardId);
		}else{
			_self.loadNewTab();
		}
	},
	resetTabs : function(){
		var lUrl  = Configuration.baseUri + "/portal/DashboardsManager/actionSearchFavouriteDashboard/";
	
	    $.ajax({ url: lUrl
	            , type:'GET'
	            , dataType: 'html'
	            , success: _.bind(this.onSuccessTabReset ,this)
	            }
	    );
	},
	onSuccessTabReset :  function(pResponse){
		$('#sortable').html(pResponse);
		this.setSelectedTab(null, this.attributes.currentSelectedId);
	},
	addTab : function(pDashboardId){
		var lUrl 	= Configuration.baseUri + '/portal/DashboardsManager/actionAddDashboard/';
		var lIndex 	= this.attributes.$Tabs.size();
	    var lData 	= 'dashboard_id=' + pDashboardId + '&index=' + lIndex;
	
	    $.ajax({ url: lUrl
	            , type:'GET'
	            , data: lData
	            , dataType: 'json'
	            , success: _.bind(this.onAddTabSuccess, this) 
	            , error: _.bind(this.onAddTabError, this)
	            }
	    );
	},
	onAddTabSuccess : function(pResponse){
		if (_gaq) {
	        _gaq.push(['_trackPageview', '/dashboard/add']);
	    }

	    var lIndex 		= pResponse.pIndex;
		var lOrder		= lIndex;
	    var lDashboardId = pResponse.pDashboardId;
		var lDashboardName = pResponse.pDashboardName;
		var lFavouriteId = pResponse.pFavouriteId.toString();
		var lUserNick	= pResponse.pUserNick;
		var lPermalink = pResponse.pDashboardPermalink;
		
		//create HTML template add it to the end of the list and set it as selected DB and load it
	    var newTab = ' <li class="tab FL myDashboardTab" rel="#id_favourite_dashboard_container_'+lIndex+'" id="id_favourite_dashboard_container_'+lIndex+'">' +
						   '<div class="clearfix">' +
						       '<a class="handle" title="' + gettext( "DBMAN-DBTAB-TIP" ) + '" id="id_maximizeFavouriteDashboardButton_'+lIndex+'" href="'+lPermalink+'">' +
						        lDashboardName +
						    	'</a>' +
						    	'<a class="icClose" title="' + gettext( "DBMAN-DBTAB-CLOSETIP" )+ '" id="id_removeFavouriteDashboardButton_'+lIndex+'" href="javascript:;"><span class="DN">' + gettext( "APP-CLOSE-TEXT" )+ '</span></a>' +
							'</div>' +
						'</li>';
						
		this.attributes.$Tabs.append(newTab);
		var $newTab = this.attributes.$Tabs.find('li:last-child');
		$newTab.data("index", lIndex);
		$newTab.data("order", lOrder);
		$newTab.data("dashboard_id", lDashboardId);
		$newTab.data("favourite_dashboard_id", lFavouriteId);
		$newTab.data("dashboard_name", lDashboardName);
		$newTab.data("user_nick", lUserNick);
		$newTab.data("dashboard_permalink", lPermalink);
		fUserNick = lUserNick;
		
		this.setSelectedTab($newTab, lDashboardId);
		this.loadTab(lDashboardId);
	},
	onAddTabError : function(pResponse){
		//review what to do here
	}
});


var dashboardDetailTabManager = dashboardTabManager.extend({
	defaults : {
		
	},
	initialize : function(){
		dashboardTabManager.prototype.initialize.call(this);
		_.defaults(this.attributes, dashboardTabManager.prototype.defaults);
		
	}, 
	onTabClicked : function(pEvent){
	},

	loadNewTab : function(){
	},

	loadTab : function(pDashboardId){
	    initDashboardPanel();
	},
	onTabDropped : function(pEvent, pUI){

	},
	updateTabPosition : function(pId, pFrom, pTo){

	},
	onTabUpdateError : function(pResponse){

	},
	removeTab : function(pFavouriteId, pTab){

	},
	onSuccessTabRemoved : function(pResponse){

	},
	onErrorTabRemoved : function(pResponse){

	},
	addTab : function(pDashboardId){

	},
	onAddTabSuccess : function(pResponse){
	
	}
});
