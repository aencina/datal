var ParamsView = Backbone.View.extend({
    events: {
        'keyup input[type=text]': 'onChangeInput'
    },

    initialize: function () {
        this.template = _.template( $('#params_template').html() );
    },

    render: function () {
        this.$el.html(this.template({
            args: this.collection.toJSON()
        }));
    },

    onChangeInput: function  (e) {
        var $target = $(e.currentTarget),
            field = $target.attr('name'),
            index = $target.data('index'),
            value = $target.val(),
            model = this.collection.at(index);

        model.set(field, value);
    }
});