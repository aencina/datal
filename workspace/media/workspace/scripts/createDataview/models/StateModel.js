var StateModel = Backbone.Model.extend({
    last: 4,

    next: function () {
        this.set('step', this.get('step') + 1);
    },

    prev: function () {
        var step = this.get('step');
        if (step > 0) {
            this.set('step', step - 1);
        }
    }
});
