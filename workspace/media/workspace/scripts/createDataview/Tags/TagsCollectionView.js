var TagsCollectionView = Backbone.View.extend({
    initialize: function () {
        this.template = _.template( $('#tags_collection_template').html() );
        this.listenTo(this.collection, 'add change remove', this.render, this);
    },

    render: function () {
        this.$el.html(this.template({tags: this.collection.toJSON()}));
    }
});