var DisclamerView = Backbone.View.extend({
	initialize: function() {
    this.template = _.template( $('#disclamer_template').html() );
  },
  render: function () {
    this.$el.html(this.template());
  }
});
