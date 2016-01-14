var PatternView = Backbone.View.extend({
    events: {
        'change select[name=pattern]': 'onChange'
    },

    initialize: function (options) {
        this.template = _.template( $('#pattern_template').html() );
        this.type = options.type;
        this.subtype = options.subtype;
    },

    render: function () {
        this.$el.html(this.template({
            type: this.type,
            subtype: this.subtype
        }));
    },

    onChange: function (e) {
        var value = $(e.currentTarget).val();
        this.trigger('change', value);
    },

    setValue: function (value) {
        this.$('select[name=pattern]').val(value);
    }
})