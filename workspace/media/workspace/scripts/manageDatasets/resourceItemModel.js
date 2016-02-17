var ResourceItemModel = Backbone.Model.extend({
    
    defaults: function() {
        return {
            title: "",
            collect_type: "",
            id: "",
            end_point: "",
            created_at: "",
            modified_at: "",
            category: "",
            author: "",
            status_nice: "",
            type_nice: "",
            type_classname: "",
            filename: "",
            dataset_last_revision_id: "",
            url: "",
            impl_type: ""
        };
    },

    remove: function (options) {
        var opts = _.extend({url: '/datasets/remove/' + this.id}, options || {});

        return Backbone.Model.prototype.destroy.call(this, opts);
    },

    remove_revision: function (options) {
        var opts = _.extend({url: '/datasets/remove/revision/' + this.id}, options || {});

        return Backbone.Model.prototype.destroy.call(this, opts);
    },

});
