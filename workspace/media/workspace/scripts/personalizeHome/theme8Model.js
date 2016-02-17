var theme8Model = Backbone.Epoxy.Model.extend({
	defaults: {
		mainTitle:'',
		mainSection:'',
		sliderSection:[],
		buttonsSectionTitle:'',
	    buttonsSectionDescription:'',
	    buttonsPerRow:'4',
	    buttonsPerRowWidth:'25',
	    buttonSection:[],
	    buttonStartingCategory:'',
	},

	initialize: function(attr){		
		if (!_.isUndefined(attr)){
			var themeConfig = attr.config
			if (!_.isUndefined(themeConfig.mainTitle)){
				this.set('mainTitle', themeConfig.mainTitle)
			}
			if (!_.isUndefined(themeConfig.mainSection)){
				this.set('mainSection', themeConfig.mainSection )
			}
			if (!_.isUndefined(themeConfig.sliderSection)){
				this.set('sliderSection', themeConfig.sliderSection )
			}
            if (!_.isUndefined(themeConfig.buttonStartingCategory)){
				this.set('buttonStartingCategory', themeConfig.buttonStartingCategory )
			}
			if (!_.isUndefined(themeConfig.buttonsSectionTitle)){
			  	this.set('buttonsSectionTitle', themeConfig.buttonsSectionTitle)
			} 
			if (!_.isUndefined(themeConfig.buttonsSectionDescription)){
			  	this.set('buttonsSectionDescription', themeConfig.buttonsSectionDescription)
			} 
			if (!_.isUndefined(themeConfig.buttonsPerRow)){
			  	this.set('buttonsPerRow', themeConfig.buttonsPerRow)
			}
			if (!_.isUndefined(themeConfig.buttonSection)){
			  	this.set('buttonSection', themeConfig.buttonSection )
			}
			}else{
				this.clear().set(this.defaults);
				//this.set('buttonSection',[]);
			}
		
	},

	toJSON: function() {
		return _.omit(this.attributes, 'config');
	},
});