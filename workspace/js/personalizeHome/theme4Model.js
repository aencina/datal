var theme4Model = Backbone.Model.extend({
	defaults: {
		mainTitle:'',
		mainSection:'',
		coverUrl:'',
		sliderSection:[],
		linkSection:[],
		resourcesTable:true,
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
			
			if (!_.isUndefined(themeConfig.coverUrl)){
				this.set('coverUrl', themeConfig.coverUrl)
			}

			if (!_.isUndefined(themeConfig.linkSection)){
				this.set('linkSection', themeConfig.linkSection)
			}		

			if (!_.isUndefined(themeConfig.resourcesTable)){
				this.set('resourcesTable', themeConfig.resourcesTable)
			}
		}
	},

	toJSON: function() {
		return _.omit(this.attributes, 'config');
	}
});