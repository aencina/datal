var CollectFileView = StepView.extend({

	name: null,
	template: null,
	templateHTML: null,

	initialize: function(){

		this.templateHTML = $("#id_collectFileTemplate").html();
		this.template = _.template( this.templateHTML );
		this.name = this.model.get('name');

		// Overriding el and $el
		this.el = '.step[data-step='+this.name+']',
		this.$el = $(this.el);

		// Right way to extend events without overriding the parent ones
		var eventsObject = {}
		eventsObject['click .backButton'] = 'onPreviousButtonClicked';
		eventsObject['click .nextButton'] = 'onNextButtonClicked';
		eventsObject['change #id_license_url'] = 'onSelectChange';
		eventsObject['change #id_frequency'] = 'onSelectChange';
		eventsObject['change #id_file_data'] = 'onInputFileChange';
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

		// Set template
		this.$el.find('.formContent').html( this.template( this.model.toJSON() ) );	

		// Init file upload
		this.initFileUpload();

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
		
		var filename = "",
			files = this.model.get('files');

		// Create
		if(!_.isUndefined(files[0]) ){
			filename = files[0].name;

		// Edit
		}else{
			filename = this.model.get('file_data');
			
		}

		if(this.model.isValid(true)){
			this.model.set('impl_type',this.model.checkExtension(filename));
			this.model.setOutput();
			this.next();
		}

	},

	isOtherValue: function(field){

		var value = this.model.get(field),
			valuesToCheck = [];
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

	onInputFileChange: function(event){

		var element = event.currentTarget,
			value = $(element).val(),
			otherElement = $(element).attr('data-other'),
			otherRow = this.$el.find(otherElement);

		// Erase C:\Fakepath\ from string (comes in chrome)
		try {
		  if( !_.isUndefined( value ) ){
				var checkValue = value.split('\\');
				if( typeof checkValue !== 'string' ){
					value = checkValue[ (checkValue.length-1) ];
				}
			}
		}
		catch(error) {
			// Do nothing
		}

		otherRow.val(value);
		
	},

	setIndividualError: function(element, name, error){

		// If license_url, use error in license_url_other
		if(name == 'license_url'){
			element = $('#id_license_url_other')
		}

		// If frequency, use error in frequency_other
		if(name == 'frequency'){
			element = $('#id_frequency_other')
		}

		if(name == 'file_data'){
			element = $('.step[data-step='+this.name+'] .input-file');
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

	initFileUpload: function(){
		
		$( this.model.get('inputFileId') ).fileupload({
			url: '/datasets/upload/',
			acceptFileTypes: '/(\.|\/)(doc|docx|docm|dotx|dotm|xls|xlsx|xlsm|xltx|xltm|xlsb|xlam|xll|odt|ods|csv|txt|pdf|html|htm|xml|kml|kmz)$/i',
			autoUpload: false,
			maxNumberOfFiles: 1,
			replaceFileInput: false,
			singleFileUploads: true,
			add: _.bind(this.onFileUploadAdd, this),
			fail: _.bind(this.onFileUploadFail, this),
			start: function(){
				$("#ajax_loading_overlay").show();
			}
		});

	},

	onFileUploadAdd: function(event, data) {
	  this.model.set('files',data.files);
	},

	onFileUploadFail:function(event, data){
        // Hide Loadings
        $("#ajax_loading_overlay").hide();
        datalEvents.trigger('datal:application-error', data);
	},

});