var DatastreamEditItemView = Backbone.Epoxy.View.extend({
    el:"body",
    sources: null,
    tags: null,
    sourceUrl: null,
    tagUrl: null,
    parentView: null,
    notesInstance: null,
    loadSpeed: 200,
    template: null,
    events: {
        "click #id_editDataview #id_edit_cancel, #id_editDataview .close, #exposeMask": "closeOverlay",
        "click #id_editDataview #id_edit_save": "onEditDataviewSave",
    },

    initialize: function(options) {
        var self = this;

        this.parentView = options.parentView;
        this.template = _.template( $("#id_editTemplate").html() );

        this.sourceUrl = options.sourceUrl;
        this.tagUrl = options.tagUrl;

        // Init Overlay
        this.$el.find('#id_editDataview').overlay({
            top: 'center',
            left: 'center',
            mask: {
                color: '#000',
                loadSpeed: this.loadSpeed,
                opacity: 0.5,
                zIndex: 99999
            }
        });

        // Render
        this.render();    

    },

    render: function(){
        var self = this;

        this.$el.find('#id_editDataview .formContent').html( this.template( this.model.toJSON() ) ); 

        this.cleanUpForm();
        this.initSourceList();
        this.initTagList();
        this.initNotes();

        this.$el.find('#id_editDataview').data('overlay').load();

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

    initSourceList: function(){
        var sourceModel = new SourceModel();
            this.sources = new Sources(this.model.get('sources'));
        new SourcesView({collection: this.sources, parentView:this, model: sourceModel, parentModel: this.model});
    },

    initTagList: function(){
        var tagModel = new TagModel();
        this.tags = new Tags(this.model.get('tags'));
        new TagsView({collection: this.tags, parentView:this, model: tagModel, parentModel: this.model});
    },

    initNotes: function(){
        this.notesInstance = new nicEditor({
             buttonList : ['bold','italic','underline','ul', 'ol', 'link', 'hr','xhtml'], 
             iconsPath: '/js_core/plugins/nicEdit/nicEditorIcons-2014.gif'
        }).panelInstance('id_notes');
    },

    onEditDataviewSave: function(){

        if(this.model.isValid(true)){

            // Set sources and tags
            this.model.set('sources', this.sources.toJSON());
            this.model.set('tags', this.tags.toJSON());
            this.model.setData();

            var self = this,
                data = this.model.get('data');

            $.ajax({ 
                url: this.model.get('editUrl'), 
                type:'POST', 
                data: data, 
                dataType: 'json',
                beforeSend: function(xhr, settings){
                    // Prevent override of global beforeSend
                    $.ajaxSettings.beforeSend(xhr, settings);
                    // Show Loading
                    $("#ajax_loading_overlay").show();
                },
                success: function(response){
                    $.gritter.add({
                        title : gettext('APP-CHANGES-SAVED-TEXT'),
                        text : gettext('APP-REDIRECTING-TEXT'),
                        image : '/static/workspace/images/common/ic_validationOk32.png',
                        sticky : false,
                        time : 3500
                    });
                    self.closeOverlay();

                    var newRevisionID = response['datastream_revision_id'],
                        setURL = "/dataviews/" + newRevisionID + '/';

                    setTimeout(function () {
                           window.location = setURL;
                    }, 2000);
                },
                error: function(response){
                    // Hide Loading
                    $("#ajax_loading_overlay").hide();
                    datalEvents.trigger('datal:application-error', response);
                    self.closeOverlay();
                }
            });

        } 

    },

    closeOverlay: function(){
        this.undelegateEvents();
        this.$el.find('#id_editDataview').data('overlay').close();
        
        var self = this;
        setTimeout(function(){
            self.notesInstance.removeInstance('id_notes')
        }, this.loadSpeed);
    },

    cleanUpForm: function(){
        this.$el.find('#id_editDataview #sourceForm .sourcesContent').html('');
        this.$el.find('#id_editDataview #tagForm .tagsContent').html('');
        $('.nicEdit-main').html('');
    },

    setIndividualError: function(element, name, error){

        // If not valid
        if( error != ''){
            element.addClass('has-error');
            element.next('span').next().remove();
            element.next().after('<p class="has-error">'+error+'</p>');

        // If valid
        }else{
            element.removeClass('has-error');
            element.next('span').next().remove();
        }

    },

});
