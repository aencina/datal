var theme7Model = Backbone.Model.extend({
    defaults: {
        welcomeSectionImageUrl:'',
        welcomeSectionTitle:'',
        welcomeSectionDescription:'',
        welcomeSectionLinkLabel:'',
        welcomeSectionLink:'',
        welcomeSectionBackgroundColor:'',
        imageSliderSection:false,
        featuredSliderSectionBackgroundColor:'',
        prioritiesSliderSection:false,
        prioritiesSectionTitle:'',
        prioritiesSectionDescription:'',
        prioritiesSliderSectionBackgroundColor:'',
        buttonsSectionTitle:'',
        buttonsSectionDescription:'',
        buttonSection:false,
        buttonSectionBackgroundColor:'',
        leftBottomSectionImageUrl:'',
        leftBottomSectionTitle:'',
        leftBottomSectionLink:'',
        leftBottomSectionBackgroundColor:'',
        middleBottomSectionImageUrl:'',
        middleBottomSectionTitle:'',
        middleBottomSectionLink:'',
        middleBottomSectionBackgroundColor:'',
        rightBottomSectionImageUrl:'',
        rightBottomSectionTitle:'',
        rightBottomSectionLink:'',
        rightBottomSectionBackgroundColor:'',
        links:[],
    },
    initialize: function(attr){ 
        if (!_.isUndefined(attr)){
            var themeConfig = attr.config
            if (!_.isUndefined(themeConfig.welcomeSectionImageUrl)){
                this.set('welcomeSectionImageUrl', themeConfig.welcomeSectionImageUrl)
            }
            if (!_.isUndefined(themeConfig.welcomeSectionTitle)){
                this.set('welcomeSectionTitle', themeConfig.welcomeSectionTitle)
            } 
            if (!_.isUndefined(themeConfig.welcomeSectionDescription)){
                this.set('welcomeSectionDescription', themeConfig.welcomeSectionDescription)
            }                           
            if (!_.isUndefined(themeConfig.welcomeSectionLink)){
                this.set('welcomeSectionLink', themeConfig.welcomeSectionLink)
            }                           
            if (!_.isUndefined(themeConfig.welcomeSectionLinkLabel)){
                this.set('welcomeSectionLinkLabel', themeConfig.welcomeSectionLinkLabel)
            }                      
            if (!_.isUndefined(themeConfig.welcomeSectionBackgroundColor)){
                this.set('welcomeSectionBackgroundColor', themeConfig.welcomeSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.imageSliderSection)){
                this.set('imageSliderSection', themeConfig.imageSliderSection )
            }
            if (!_.isUndefined(themeConfig.featuredSliderSectionBackgroundColor)){
                this.set('featuredSliderSectionBackgroundColor', themeConfig.featuredSliderSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.prioritiesSliderSection)){
                this.set('prioritiesSliderSection', themeConfig.prioritiesSliderSection )
            }
            if (!_.isUndefined(themeConfig.prioritiesSectionTitle)){
                this.set('prioritiesSectionTitle', themeConfig.prioritiesSectionTitle)
            } 
            if (!_.isUndefined(themeConfig.prioritiesSectionDescription)){
                this.set('prioritiesSectionDescription', themeConfig.prioritiesSectionDescription)
            } 
            if (!_.isUndefined(themeConfig.prioritiesSliderSectionBackgroundColor)){
                this.set('prioritiesSliderSectionBackgroundColor', themeConfig.prioritiesSliderSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.buttonsSectionTitle)){
                this.set('buttonsSectionTitle', themeConfig.buttonsSectionTitle)
            } 
            if (!_.isUndefined(themeConfig.buttonsSectionDescription)){
                this.set('buttonsSectionDescription', themeConfig.buttonsSectionDescription)
            } 
            if (!_.isUndefined(themeConfig.buttonSection)){
                this.set('buttonSection', themeConfig.buttonSection )
            }
            if (!_.isUndefined(themeConfig.buttonSectionBackgroundColor)){
                this.set('buttonSectionBackgroundColor', themeConfig.buttonSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.leftBottomSectionImageUrl)){
                this.set('leftBottomSectionImageUrl', themeConfig.leftBottomSectionImageUrl)
            }
            if (!_.isUndefined(themeConfig.leftBottomSectionTitle)){
                this.set('leftBottomSectionTitle', themeConfig.leftBottomSectionTitle)
            }
            if (!_.isUndefined(themeConfig.leftBottomSectionLink)){
                this.set('leftBottomSectionLink', themeConfig.leftBottomSectionLink)
            }
            if (!_.isUndefined(themeConfig.leftBottomSectionBackgroundColor)){
                this.set('leftBottomSectionBackgroundColor', themeConfig.leftBottomSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.middleBottomSectionImageUrl)){
                this.set('middleBottomSectionImageUrl', themeConfig.middleBottomSectionImageUrl)
            }
            if (!_.isUndefined(themeConfig.middleBottomSectionTitle)){
                this.set('middleBottomSectionTitle', themeConfig.middleBottomSectionTitle)
            }
            if (!_.isUndefined(themeConfig.middleBottomSectionLink)){
                this.set('middleBottomSectionLink', themeConfig.middleBottomSectionLink)
            }
            if (!_.isUndefined(themeConfig.middleBottomSectionBackgroundColor)){
                this.set('middleBottomSectionBackgroundColor', themeConfig.middleBottomSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.rightBottomSectionImageUrl)){
                this.set('rightBottomSectionImageUrl', themeConfig.rightBottomSectionImageUrl)
            }
            if (!_.isUndefined(themeConfig.rightBottomSectionTitle)){
                this.set('rightBottomSectionTitle', themeConfig.rightBottomSectionTitle)
            }                           
            if (!_.isUndefined(themeConfig.rightBottomSectionLink)){
                this.set('rightBottomSectionLink', themeConfig.rightBottomSectionLink)
            }                       
            if (!_.isUndefined(themeConfig.rightBottomSectionBackgroundColor)){
                this.set('rightBottomSectionBackgroundColor', themeConfig.rightBottomSectionBackgroundColor)
            }
            if (!_.isUndefined(themeConfig.links)){
                this.set('links', themeConfig.links)
            }  
        }
        else{
            this.clear().set(this.defaults);
            this.set('buttonSection',[]);
            this.set('imageSliderSection',[]);
            this.set('prioritiesSliderSection',[]);
        }
    },

    toJSON: function() {
        return _.omit(this.attributes, 'config');
    }
});