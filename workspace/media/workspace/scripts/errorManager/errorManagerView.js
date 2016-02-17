(function ($, Backbone, global, undefined) {
    var ErrorManagerView = Backbone.View.extend({
        template: null,
        initialize: function () {
            this.model.on("set change", this.render, this);

            datalEvents.on('datal:application-error', this.onApplicationError, this);
        },
        /**
         * Captures an object containing data from an error exception
         * @param  {Object}
         */
        onApplicationError: function (errorSource) {
            this.model.assignRaw(errorSource);
        },
        prepareText: function () {
            return this.template(this.model.toJSON());
        },
        render: function () {
            if(this.template === null)
                this.template = _.template($("#errorManagerView_template").html());
            this.addGritterNotification();
        },
        addGritterNotification: function () {
            var params = {
                title: this.model.get('error'),
                text: this.prepareText(),
                image: '/static/workspace/images/common/ic_validationError32.png',
                sticky: true
            }
            var responseOnClose = this.model.get('responseOnClose')
            if ( responseOnClose ) {
                params['after_close'] = responseOnClose 
            }
            $.gritter.add(params);
        }
    });

    global.errorManagerView = new ErrorManagerView({ model: global.errorManagerModel });
})(jQuery, Backbone, window);