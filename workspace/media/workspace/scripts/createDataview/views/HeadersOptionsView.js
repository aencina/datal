var HeadersOptionsView = Backbone.View.extend({
    events: {
        'click a.btn-clear': 'onClickClear',
        'click a.btn-back': 'onClickBack',
        'click button.btn-ok': 'onClickOk'
    },


    initialize: function () {
        this.template = _.template( $('#headers_options_template').html() );
        this.listenTo(this.model, 'change', this.render, this);
    },

    render: function () {
        this.$el.html(this.template({
            state: this.model.toJSON()
        }));
    },

    onClickBack: function () {
        this.collection.removeItemsByMode('header');
        this.model.set('mode', 'data');
    },

    onClickClear: function () {
        this.collection.removeItemsByMode('header');
    },

    onClickOk: function () {
        this.model.set('mode', 'data');
    },

    show: function () {
        this.$el.removeClass('hidden');
    },

    hide: function () {
        this.$el.addClass('hidden');
    },
});
