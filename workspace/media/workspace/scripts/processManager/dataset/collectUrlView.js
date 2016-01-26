var CollectUrlView = StepView.extend({

	name: null,
	template: null,
	templateHTML: null,

	initialize: function(){

		this.templateHTML = $("#id_collectUrlTemplate").html();
		this.template = _.template( this.templateHTML );
		this.name = this.model.get('name');

		// Overriding el and $el
		this.el = '.step[data-step='+this.name+']',
		this.$el = $(this.el);

		// Right way to extend events without overriding the parent ones
		var eventsObject = {}
		eventsObject['click .backButton'] = 'onPreviousButtonClicked';
		eventsObject['click .nextButton'] = 'onNextButtonClicked';
		eventsObject['change #id_license_url, #id_frequency'] = 'onSelectChange';
		this.addEvents(eventsObject);

		// Bind model validation to view
		Backbone.Validation.bind(this);

		this.render();

	}, 

	render: function(){

		var self = this;

		// Check if is the value is "other", and set that in the model.
		this.isOtherValue('frequency');
		this.isOtherValue('license_url');

		this.$el.find('.formContent').html( this.template( this.model.toJSON() ) );	

		// Bind custom model validation callbacks
		Backbone.Validation.bind(this, {
			valid: function (view, attr, selector) {
				self.setIndividualError(view.$('[name=' + attr + ']'), attr, '');
			},
			invalid: function (view, attr, error, selector) {
				self.setIndividualError(view.$('[name=' + attr + ']'), attr, error);
			}
		});

		return this;
	},

	onPreviousButtonClicked: function(){
		this.previous();
	},

	onNextButtonClicked: function(){

		var end_point = $.trim( this.model.get('end_point') );
		this.model.set('end_point', end_point);

		if(this.model.isValid(true)){

			var self = this,
				ajaxUrl  = '/datasets/check_endpoint_url/',
				ajaxData = "url="+ encodeURI(this.model.get('end_point'));

			$.when(
				$.ajax({ 
					url: ajaxUrl,
					data: ajaxData,
					dataType: 'json',
					beforeSend: function(xhr, settings){
						// Prevent override of global beforeSend
						$.ajaxSettings.beforeSend(xhr, settings);
						// Show Loading
						$("#ajax_loading_overlay").show();
					},
					success: function(response){
						// Set impl_type in model
						var impl_type = self.model.setImplementationTypeByMimeType(response.mimetype);
						self.model.set('impl_type', impl_type);
					},
					error: function(response){
						datalEvents.trigger('datal:application-error', response);
					},
					complete: function(){
						// Hide Loading
						$("#ajax_loading_overlay").hide();
					}
				})
			).then(function(){
				// If impl_type was not setted, do not proceed
				if( self.model.get('impl_type') !== '' ){
					self.model.setOutput();
					self.next();
				}else{
					$.gritter.add({
						title: 'Error',
						text: gettext('ERROR-TRY-ANOTHER-DATASET'),
						image: '/static/workspace/images/common/ic_validationError32.png',
						sticky: true,
						time: ''
					});
				}
			});
			
		}
	},

	isOtherValue: function(field){

		var value = this.model.get(field),
			valuesToCheck = [],
			htmlString = this.parseHTML(this.templateHTML),
			values = htmlString.find('[name='+field+'] option');

		for(i=0;i<values.length;i++){
			valuesToCheck.push( values.eq(i).val() );
		}

		if( $.inArray(value, valuesToCheck) == -1 ){
			this.model.set(field, 'other');
			this.model.set(field+'_other', value);
		}

	},

	parseHTML:function(htmlString){
		var fakeEl = $( '<div></div>' );
		fakeEl.html( htmlString );
		return $(fakeEl);
	},

	onSelectChange: function(event){

		var element = event.currentTarget,
			value = $(element).val(),
			otherElement = $(element).attr('data-other'),
			otherRow = this.$el.find(otherElement);

		if(value == 'other'){
			otherRow.show();
		}else{
			otherRow.hide();
		}

	},

	setIndividualError: function(element, name, error){

		// If license_url, use error in license_url_other
		if( name == 'license_url'){
			element = $('#id_license_url_other')
		}

		// If frequency, use error in frequency_other
		if( name == 'frequency'){
			element = $('#id_frequency_other')
		}

		// If not valid
		if( error != ''){
			element.addClass('has-error');
			element.next('p.has-error').remove();
			element.after('<p class="has-error">'+error+'</p>');

		// If valid
		}else{
			element.removeClass('has-error');
			element.next('p.has-error').remove();
		}

	},

});
