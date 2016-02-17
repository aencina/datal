var ListDatastreamView = Backbone.View.extend({
	el: $("#datastream_list"),

	initialize: function(input){
		// Initialize the model and the filters call for listening.
		this.model = input.datastreamCollection;
		this.rows_views = [];
		this.render();
	}
});