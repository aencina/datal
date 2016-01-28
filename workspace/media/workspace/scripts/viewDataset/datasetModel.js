var DatasetModel = dataset.extend({
  remove: function (options) {
      var opts = _.extend({url: '/datasets/remove/' + this.id}, options || {});

      return Backbone.Model.prototype.destroy.call(this, opts);
  },

  remove_revision: function (options) {
      var opts = _.extend({url: '/datasets/remove/revision/' + this.id}, options || {});

      return Backbone.Model.prototype.destroy.call(this, opts);
  }

});
