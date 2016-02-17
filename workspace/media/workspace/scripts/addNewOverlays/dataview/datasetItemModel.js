var DatasetItemModel = Backbone.Model.extend({
	defaults: function() {
		return {
			title: "",
			collect_type: "",
			id: "",
			end_point: "",
			created_at: "",
			category: "",
			author: "",
			status_nice: "",
			type_nice: "",
			type_classname: ""
		};
	}
});