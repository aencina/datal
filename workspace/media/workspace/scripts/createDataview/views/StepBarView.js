var StepBarView = Backbone.View.extend({
    events: {
        'click .btn-next': 'onClickNext',
        'click .btn-prev': 'onClickPrev',
        'click .btn-save': 'onClickSave'
    },

    initialize: function () {
        this.template = _.template( $('#step_bar_template').html() );
        this.listenTo(this.model, 'change:step', this.render, this);
    },

    render: function () {
        var step = this.model.get('step');
        this.$el.html(this.template({
            step: step
        }));
        return this;
    },

    onClickNext: function () {
        this.trigger('next');
    },

    onClickPrev: function () {
        this.trigger('prev');
    },

    onClickSave: function () {
        this.trigger('save');
    },

    enable: function (enabled) {
        this.$('.btn-next').toggleClass('disabled', !enabled);
    }
});
