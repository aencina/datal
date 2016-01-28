var ListDatastreams = Backbone.PageableCollection.extend({

	model: DatastreamItemModel,
	url: "/visualizations/filter_datastream/",

	// Any `state` or `queryParam` you override in a subclass will be merged with
	// the defaults in `Backbone.PageableCollection` 's prototype.
	state: {

		// You can use 0-based or 1-based indices, the default is 1-based.
		// You can set to 0-based by setting ``firstPage`` to 0.
		firstPage: 0,

		// Set this to the initial page index if different from `firstPage`. Can
		// also be 0-based or 1-based.

		pageSize:10,

	},

 queryParams: {
		totalPages: null,
		page:null,
		pageSize:null,
	},

 parseState: function (resp, queryParams, state, options) {
		return {totalRecords: resp.total_entries};
	},

parseRecords: function (resp) {
		return resp.items;
	}

});