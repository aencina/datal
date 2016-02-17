var ResourceItemModel = Backbone.Model.extend({

    defaults: function() {
        return {
            title: "",
            id: "",
            dataset__datasetrevision__end_point: "",
            created_at: "",
            category: "",
            author: "",
            status_nice: "",
            dataset_title: "",
            end_point: "",
            datastream_id: "",
            url: ""
        };
    },

    remove: function (options) {
        var opts = _.extend({url: '/dataviews/remove/' + this.id}, options || {});

        return Backbone.Model.prototype.destroy.call(this, opts);
    },

    remove_revision: function (options) {
        var opts = _.extend({url: '/dataviews/remove/revision/' + this.id}, options || {});

        return Backbone.Model.prototype.destroy.call(this, opts);
    },
    
});
