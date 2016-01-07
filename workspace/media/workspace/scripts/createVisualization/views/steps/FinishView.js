var FinishView = StepViewSPA.extend({

	initialize: function(){
		FinishView.__super__.initialize.apply(this, arguments);

		this.addEvents({
			'click a.backButton': 'onPreviousButtonClicked',
			'click button.editMetadata': 'onPreviousButtonClicked',
			'click button.editChart': 'onEditChartButtonClicked',
			'click a.finishButton': 'onFinishButtonClicked'
		});

		this.chartsFactory = new charts.ChartsFactory(); // create ChartsFactory

		this.chartContent = this.$el.find('.chartContentFinish');
		this.finishBtn = this.$el.find('a.finishButton');

	}, 

	bindingHandlers: {
		listTags: function( $element, value ) {
			if(value && value.length > 0){
			
				$element.parent().show();
				
				var htmlTemplate =	'<div class="tag"><span class="tagInner clearfix"><span class="tagTxt">[[tag]]</span></span></div>';
			    var html = [];
			    _.each(value,function(t){
			    	html.push(htmlTemplate.replace('[[tag]]',t.name));
			    });

			    $element.html( html.join('') );
			    
			};
		},
		listSources: function( $element, value ) {
			if(value && value.length > 0){
			
				$element.parent().show();

				var htmlTemplate =	'<p><a href="[[url]]" target="_blank">[[name]]</a></p>';
			    var html = [];
			    _.each(value,function(t){
			    	html.push(htmlTemplate.replace('[[url]]',t.url).replace('[[name]]',t.name));
			    });

			    $element.html( html.join('') );

			};
		},
		showField: function( $element, value){
			if(value != '<br>' && value != undefined && value != ''){
				$element.parent().show();
				$element.html( value );
			}else{
				$element.parent().hide();
			};
		}
	},

	onEditChartButtonClicked: function(){
		this.goTo(1);
	},

	onPreviousButtonClicked: function(){
		this.previous();
	},

	onFinishButtonClicked: function(e){
		if(!this.finishBtn.hasClass('saving')){
			$("#ajax_loading_overlay").show();
			this.finishBtn.addClass('saving');
			var self=this;
			var data = this.model.save().then(function (response) {
				window.location = '/visualizations/'+response.revision_id;
			}).fail(function (rejection) {
				self.finishBtn.removeClass('saving');
				$("#ajax_loading_overlay").hide();
				console.error(rejection);
			});
		}

	},

	start: function(){
		this.constructor.__super__.start.apply(this);
		this.finishBtn.removeClass('saving');
		this.setupChart();
		this.renderChart();

	},

	finish: function(){
		this.constructor.__super__.finish.apply(this);
		if(this.chartInstance){
			this.chartInstance.destroy();
		}
	},

	setupChart: function(){

		var chartSettings = this.chartsFactory.create(this.model.get('type'),this.model.get('lib'));

		if(chartSettings){

			//Set list of custom attributes for my model
			this.model.set('attributes',chartSettings.attributes);

			this.ChartViewClass = chartSettings.Class;

		} else {
			delete this.ChartViewClass;
			console.log('There are not class for this');
		}

	},

	renderChart: function () {
	
		if (this.ChartViewClass) {

			if(this.chartInstance){
				this.chartInstance.destroy();
			}

			this.chartInstance = new this.ChartViewClass({
				el: this.chartContent,
				model: this.model,
				mapOptions: {
                    disableDefaultUI: true,
                    disableDoubleClickZoom: true,
                    scrollwheel: false,
                    draggable: false
                }
			});
			
			if(this.model.valid()){
				this.chartInstance.render();
			};
		}
	},

});