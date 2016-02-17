var ListDatasetView = Backbone.View.extend({
	el: $("#dataset_list"),

	initialize: function(input){
		// Initialize the model and the filters call for listening.
		this.model = input.datasetCollection;
		this.rows_views = [];
		this.render();
	}
});