var personalizeView = Backbone.View.extend({
	
	//el: '#id_personalizeHome',
	el: '.main-section',
	pivotView: null,
	themeToSet : null,
	themeModel : null,
	events:{
		'click #id_save, #id_save_top, #id_preview, #id_preview_top': 'save',
		'click #id_noThemeButton, #id_theme0Button, #id_theme1Button, #id_theme2Button, #id_theme3Button, #id_theme4Button, #id_theme5Button, #id_theme6Button, #id_theme7Button, #id_theme8Button': 'onSwitchThemeButtonClicked',
	},

	initialize: function(){

		themeToSet = this.model.get('themeID');
		this.render();

	},

	render: function(){  	
	
		that = this;
		if(this.pivotView){
			this.pivotView.undelegateEvents();		
		}
	
		switch(themeToSet){  			
			case '0':
				this.selectTheme0();
				break;
			case '1':
				this.selectTheme1();
				break;
			case '2':
				this.selectTheme2();
				break;
			case '3':
				this.selectTheme3();
				break;
			case '4':
				this.selectTheme4();
				break;
			case '5':
				this.selectTheme5();
				break;
			case '6':
				this.selectTheme6();
				break;
			case '7':
				this.selectTheme7();
				break;
			case '8':
				this.selectTheme8();
				break;
			default:
				this.noThemeSelected();
		}

		return this;

	},

	onSwitchThemeButtonClicked: function(event){

		themeToSet = $(event.currentTarget).attr('rel');
		themeModel = null;
		this.render();
		
	},

	selectTheme0: function(){		
		this.selectTab('id_theme0Button');
		this.setThemeDescriptions(0);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme0Model( {config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme0Model();
		}	
		this.pivotView = new theme0View({
			model: themeModel , currentModel: this.model, currentView: this
		});

	},

	selectTheme1: function(){
		this.selectTab('id_theme1Button');
		this.setThemeDescriptions(1);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme1Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme1Model();
		}	
		this.pivotView = new theme1View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});

	},

	selectTheme2: function(){
		this.selectTab('id_theme2Button');
		this.setThemeDescriptions(2);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme2Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme2Model();
		}	
		this.pivotView = new theme2View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});

	},

	selectTheme3: function(){
		this.selectTab('id_theme3Button');
		this.setThemeDescriptions(3);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme3Model( {config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme3Model();			
		}	
		this.pivotView = new theme3View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});		
	},

	selectTheme4: function(){
		this.selectTab('id_theme4Button');
		this.setThemeDescriptions(4);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme4Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme4Model();
		}	
		this.pivotView = new theme4View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});
	},

	selectTheme5: function(){
		this.selectTab('id_theme5Button');
		this.setThemeDescriptions(5);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme5Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme5Model();
		}	
		this.pivotView = new theme5View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});
	},

	selectTheme6: function(){
		this.selectTab('id_theme6Button');
		this.setThemeDescriptions(6);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview, #id_preview_top').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme6Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme6Model();
		}	
		this.pivotView = new theme6View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});
	},

	selectTheme7: function(){
		this.selectTab('id_theme7Button');
		this.setThemeDescriptions(7);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme7Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme7Model();
		}	
		this.pivotView = new theme7View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});
	},

	selectTheme8: function(){
		this.selectTab('id_theme8Button');
		this.setThemeDescriptions(8);
		$('#id_themeConfigs').show().removeClass('noThemeSelected');
		$('#id_preview').show();
		if(themeToSet == this.model.get('themeID'))
		{
			themeModel= new theme8Model({config: this.model.get('config')});
		}
		else
		{
			themeModel = new theme8Model();
		}	
		this.pivotView = new theme8View({ 
			model: themeModel, currentModel: this.model, currentView: this
		});
	},

	noThemeSelected: function(){		
		this.selectTab('id_noThemeButton');
		this.setThemeDescriptions(null);
		$('#id_themeConfigs').show().addClass('noThemeSelected');
		$('#id_preview, #id_preview_top').hide();
		$('#id_themeForm').html();
		this.pivotView = null;
	},

	selectTab: function(tab){
		$('.themeTabs li').removeClass('active');
		$('#'+tab).parent().addClass('active');
	},

	setThemeDescriptions: function(themeID){
		var description;

		if( _.isUndefined(themeID) || themeID == null ){
			description = gettext('ADMIN-HOME-DESCRIPTION-NOTHEME');
		}else{
			description = gettext('ADMIN-HOME-DESCRIPTION-THEME'+themeID);
		}

		$('#id_description').html(description);

	},
	
	save: function(event){
		
		if( _.isUndefined(this.pivotView) || this.pivotView == null ){
			
			var ob={};
			this.model.set('config', null);
			this.model.set('themeID', null);
			ob['config'] = this.model.get('config');
			ob['theme'] = this.model.get('themeID');
			ob['type']= 'save';

			$.ajax({
				type: 'POST',
				data: {'jsonString': saferStringify(ob)}, 
				dataType: 'json',
				beforeSend: function(xhr, settings){

					// call global beforeSend func
					$.ajaxSettings.beforeSend(xhr, settings);

					$("#ajax_loading_overlay").show();
				},
				success: function(response) {
					$("#ajax_loading_overlay").hide();
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-SUCCESS-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-SUCCESS-TEXT'),
						image : '/static/workspace/images/common/ic_validationOk32.png',
						sticky : false,
						time : 3500
					});
				},
				error: function(response) {
					$("#ajax_loading_overlay").hide();
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : true,
						time : ''
					});
				},
				url: '/personalizeHome/save/'
			});			

		}else{			
		 	this.pivotView.save(event);
		}
			
	},

	helpAndTips: function(action){
		if(action == 'show'){
			$('.helpBox').show();
		}else{
			$('.helpBox').hide();
		}
	}

});