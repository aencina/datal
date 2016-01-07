var Theme8View = Backbone.Epoxy.View.extend({

	el: '.theme8',

	events:{
		"click .buttons-grid li": "onButtonClicked",
		"click a.back": "onBackClicked"
	},

	initialize: function(options){
		this.initButtons();
		this.render();
	},

	render: function(){
		return this;
	},

	initButtons: function(){

	    this.$el.find('.buttons .caption').css({
	        position: "absolute",
	        top: "50%",
	        width: "100%",
	        marginTop: "-" + $('.buttons .caption').height() / 2 + "px"
	    });

	},

	onButtonClicked: function(event){

		var titleUpgradeable = $(event.currentTarget).attr('data-button-title');
		this.model.set('titleUpgradeable', titleUpgradeable);

		this.$el.find('.section-title h3').fadeOut();
		this.$el.find('.buttons a.back').css('opacity','1');
		this.$el.find('.resources-table').fadeIn();
		this.$el.find('.buttons-grid').fadeOut();
	},

	onBackClicked: function(event){

		var titleOriginal = this.model.get('titleOriginal');
		this.model.set('titleUpgradeable', titleOriginal);

		this.$el.find('.section-title h3').fadeIn();
		this.$el.find('.buttons a.back').css('opacity','0');
		this.$el.find('.resources-table').fadeOut();
		this.$el.find('.buttons-grid').fadeIn();
		// desmarcar las categorias elegidas
		window.datatableHomeFilterManager.cleanCategories();	

	}

});