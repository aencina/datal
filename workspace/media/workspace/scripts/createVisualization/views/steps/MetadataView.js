var MetadataView = StepViewSPA.extend({

	initialize: function(){
		MetadataView.__super__.initialize.apply(this, arguments);

		this.$el.find('.validate-msg').hide();
		this.addEvents({
			'click a.backButton': 'onPreviousButtonClicked',
			'click a.nextButton': 'onNextButtonClicked'
		});
		this.initNotes();
	},

	bindings: {
		"input.title": 			"value:title,		events:['keyup']",
		"input.description": 	"value:description,events:['keyup']",
		"select.category": 		"value:datastream_category,	events:['change']"
	},

	onPreviousButtonClicked: function(e){
		this.previous();
	},

	onNextButtonClicked: function(){
		this.$el.find('input').removeClass('has-error');
		this.$el.find('.validate-msg').hide();

		//hago set aquí porque Epoxy no se banca nicedit
		var notes = '';
		if($('.nicEdit-main').length > 0
				&& $('.nicEdit-main').html() != '<br>' // When notes initialice empty, nicEdit initialice with <br>, so we check if that is the case
		){
			notes = $.trim( this.notesInstance.instanceById('id_notes').getContent() );
		}

		this.model.set('notes', notes);

		var validation = this.model.validateMetadata();
		if( validation.valid ){
			this.next();
		}else{
			var that = this;
			_.each(validation.fields, function(invalid, field){
				if(invalid){
					that.$el.find('input.'+field).addClass('has-error');
					that.$el.find('input.'+field).siblings('.validate-msg').show();
				}
				if (field === 'notes' && invalid) {
					that.$el.find('.notes-field .validate-msg').show();
				}
			});
		};
	},

	initNotes: function(){
        
        this.notesInstance = new nicEditor({
            buttonList : ['bold','italic','underline','ul', 'ol', 'link', 'hr','xhtml'], 
            iconsPath: '/js_core/plugins/nicEdit/nicEditorIcons-2014.gif'
        }).panelInstance('id_notes');

		if(this.model.get('notes')){
			this.notesInstance.instanceById('id_notes').setContent(this.model.get('notes'));
		}

    },


});
