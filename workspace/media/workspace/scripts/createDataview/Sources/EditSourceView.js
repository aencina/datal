var EditSourceView = Backbone.Epoxy.View.extend({
  events: {
    'click a.btn-add': 'onAdd'
  },

  bindings: {
    "input.source__name": "value:source__name, events:['keyup']",
    "input.source__url": "value:source__url, events:['keyup']"
  },

  initialize: function (options) {
    this.template = _.template( $('#edit_source_template').html() );
  },

  render: function () {
    var self = this;
    this.$el.html(this.template({}));
    this.applyBindings();

    Backbone.Validation.bind(this, {
      valid: function (view, attr, selector) {
        self.setIndividualError(view.$('[name=' + attr + ']'), attr, '');
      },
      invalid: function (view, attr, error, selector) {
        self.setIndividualError(view.$('[name=' + attr + ']'), attr, error);
      }
    });
  },

  onAdd: function (e) {
    if (this.model.isValid(true)) {
      this.collection.add(this.model);
      this.remove();
    }
  },

  setIndividualError: function(element, name, error){
    // If not valid
    if( error != ''){
      element.addClass('has-error');
      element.next('p.has-error').remove();
      element.after('<p class="has-error">'+error+'</p>');

    // If valid
    }else{
      element.removeClass('has-error');
      element.next('p.has-error').remove();
    }
  },
})