var DatastreamEditItemView = Backbone.Epoxy.View.extend({
    el:"#id_editDataview",
    sources: null,
    tags: null,
    parentView: null,
    notesInstance: null,
    events: {
        "click #id_edit_cancel, .close": "closeOverlay",
        "click #id_edit_save": "onEditDataviewSave",
    },

    initialize: function(options) {
        var self = this;
        this.options = options;
        this.parentView = this.options.parentView;
        this.cleanUpForm();
        this.initSourceList();
        this.initTagList();
        this.initNotes();

        // Init Overlay
        this.$el.overlay({
            top: 'center',
            left: 'center',
            mask: {
                color: '#000',
                loadSpeed: 200,
                opacity: 0.5,
                zIndex: 99999
            }
        });

        // Render
        this.render();    

    },

    render: function(){
        var self = this;
        this.$el.data('overlay').load();

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
        $('#id_notes').val(this.model.get('notes'));
        this.notesInstance = new nicEditor({
            buttonList : ['bold','italic','underline','ul', 'ol', 'link', 'hr'], 
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

            // NOT WORKING. Need to be done with data and select what is sent to server.
            $.ajax({ 
                url: '/dataviews/edit/'+ this.model.get('datastream_revision_id'), 
                type:'POST', 
                data: data, 
                dataType: 'json',
                success: function(){

                    // Old way - Not good. Instead let's try a fetch and reset the grid.
                    // window.location.replace("/dataviews/");

                    // Reload Grid
                    self.parentView.listResources.fetch({
                        reset: true
                    });

                    $.gritter.add({
                        title : gettext('APP-CHANGES-SAVED-TEXT'),
                        text : gettext('APP-DATASTREAM-SAVESUCCESS-TEXT'),
                        image : '/static/workspace/images/common/ic_validationOk32.png',
                        sticky : false,
                        time : 3500
                    });
                    self.closeOverlay();

                },
                error: function(){
                    $.gritter.add({
                        title : gettext('APP-ERROR-TEXT'),
                        text : gettext('APP-REQUEST-ERROR'),
                        image : '/static/workspace/images/common/ic_validationError32.png',
                        sticky : true,
                        time : 3500
                    });
                    self.closeOverlay();
                }
            });      

        } 

    },

    closeOverlay: function(){
        this.notesInstance.removeInstance('id_notes');
        this.undelegateEvents();
        this.$el.data('overlay').close();
    },

    cleanUpForm: function(){
        this.$el.find('#sourceForm .sourcesContent').html('');
        this.$el.find('#tagForm .tagsContent').html('');
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