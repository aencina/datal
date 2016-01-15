var MetadataView = Backbone.Epoxy.View.extend({
    events:  {
        'click a.add-source': 'onAddSource'
    },

    bindings: {
        "input.title":          "value:title, events:['keyup']",
        "input.description":    "value:description, events:['keyup']",
        "select.category":      "value:category, events:['change']"
    },

    initialize: function (options) {
        this.template = _.template( $('#metadata_view_template').html() );
        this.categories = options.categories;
    },

    render: function () {
        var self = this;
        this.$el.html(this.template({
            categories: this.categories
        }));
        this.applyBindings();

        var default_category = _.find(this.categories, function (category) {
            return category[2];
        });

        if (_.isUndefined(default_category)) {
            default_category = this.categories[0];
        }

        if (!this.model.has('category')) {
            this.model.set('category', default_category[0]);
        };

        Backbone.Validation.bind(this, {
            attributes: function(view) {
                return ['title', 'description'];
            },
            valid: function (view, attr, selector) {
                self.setIndividualError(view.$('[name=' + attr + ']'), attr, '');
            },
            invalid: function (view, attr, error, selector) {
                self.setIndividualError(view.$('[name=' + attr + ']'), attr, error);
            },
        });
        this.sourcesView = new SourcesView({
            el: this.$('.sources-view'),
            collection: this.model.sources
        });
        this.sourcesView.render();

        this.tagsView = new TagsView({
            el: this.$('.tags-view'),
            collection: this.model.tags
        });
        this.tagsView.render();

        this.paramsView = new ParamsView({
            el: this.$('.params-view'),
            collection: this.model.dataset.args
        });
        this.paramsView.render();

        this.initNotes();
        this.$('.input-source').autocomplete({
          source: '/rest/sources.json',
          minLength: 3,
          select: function (e, ui) {
            e.preventDefault();
            self.model.set({
                source__name: ui.item.value,
                source__url: ''
            });
            if(self.model.isValid(true)){
              self.model.sources.add(self.model.toJSON());
              $(e.target).val('');
            }
          }
        });
    },

    initNotes: function(){

        this.notesInstance = new nicEditor({
            buttonList : ['bold','italic','underline','ul', 'ol', 'link', 'hr'],
            iconsPath: '/js_core/plugins/nicEdit/nicEditorIcons-2014.gif'
        }).panelInstance('id_notes_2');

        if(this.model.get('notes')){
            this.notesInstance.instanceById('id_notes_2').setContent(this.model.get('notes'));
        }

    },

    onAddSource: function (e) {
        this.editSourceView = new EditSourceView({
            model: new SourceModel(),
            collection: this.model.sources
        });
        this.editSourceView.render();
        this.$('.edit-source-view').html(this.editSourceView.$el);
    },

    setIndividualError: function(element, name, error){
        var textarea = $('.textarea');

        // If not valid
        if( error != ''){

            if(name == 'notes'){
                textarea.addClass('has-error');
                textarea.next('p.has-error').remove();
                textarea.after('<p class="has-error">'+error+'</p>');
            }else{
                element.addClass('has-error');
                element.next('p.has-error').remove();
                element.after('<p class="has-error">'+error+'</p>');
            }

        // If valid
        }else{
            element.removeClass('has-error');
            element.next('p.has-error').remove();

            textarea.removeClass('has-error');
            textarea.next('p.has-error').remove();
        }

    },

    isValid: function () {
        var notes = '';
        var content = this.notesInstance.instanceById('id_notes_2').getContent();

        // When notes initialice empty, nicEdit initialices with <br>
        if (content.length > 0 && content !== '<br>') {
            notes = $.trim( content );
        }

        this.model.set('notes', notes);

        var valid = this.model.isValid(true);
        return valid;
    }
})