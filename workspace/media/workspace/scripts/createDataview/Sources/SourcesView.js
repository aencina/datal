var SourcesView = Backbone.View.extend({
  events: {
    'click  a.remove': 'onRemove'
  },

  initialize: function () {
    var self = this;
    this.template = _.template( $('#sources_template').html() );
    this.listenTo(this.collection, 'add remove change', this.render, this);
  },

  render: function () {
    this.$el.html(this.template({
      sources: this.collection.toJSON()
    }));
  },

  onRemove: function (e) {
    var index = $(e.currentTarget).data('index');
    this.collection.remove(this.collection.at(index));
  }
})