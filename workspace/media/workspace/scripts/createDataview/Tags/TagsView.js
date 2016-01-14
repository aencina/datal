var TagsView = Backbone.View.extend({
    events: {
        'keyup input.input-tag': 'onKeyUpInputTag',
        'click  a.remove': 'onRemove'
    },

    initialize: function () {
        this.template = _.template( $('#tags_template').html() );
    },

    render: function () {
        this.$el.html(this.template());
        this.$('.input-tag').autocomplete({
            source: '/rest/tags.json',
            minLength: 3,
            select: function (e, ui) {
                e.preventDefault();
                var model = new self.collection.model({
                    tag__name: ui.item.value
                });
                if(model.isValid(true)){
                    self.collection.add(model.toJSON());
                    $(e.target).val('');
                }
            }
        });
        this.tagsCollectionView = new TagsCollectionView({
            el: this.$('.tags-collection-view'),
            collection: this.collection
        });
        this.tagsCollectionView.render();
    },

    onKeyUpInputTag: function(e) {
        var code = e.keyCode,
            $target = $(e.currentTarget),
            tag = $target.val(),
            model;

        if((tag != '') && (code == 188 || code == 13)) { 
            if(code == 188){
                var tag = tag.substring(0, tag.length-1);
            }
            model = new this.collection.model({tag__name: tag});
            if(model.isValid(true)){
                this.collection.add(model.toJSON());
                $target.val('');
            }
        }
    },

    onRemove: function (e) {
        var index = $(e.currentTarget).data('index');
        this.collection.remove(this.collection.at(index));
    }
});