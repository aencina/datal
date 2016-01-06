var MainView = Backbone.View.extend({

    initialize: function (options) {

        this.stateModel = new StateModel({
            step: 0
        });

        this.stepBarView = new StepBarView({
            el: '.context-menu',
            model: this.stateModel
        });

        this.dataviewModel = options.dataviewModel;
        this.categories = options.categories;

        this.dataviewModel.dataset.fetch();

        this.listenToOnce(this.dataviewModel.dataset, 'change:tables', function () {
            this.render();
            this.listenTo(this.stateModel, 'change:step', this.render, this);
        }, this);
        this.listenTo(this.stepBarView, 'save', this.onClickSave, this);
        this.listenTo(this.stepBarView, 'next', this.onClickNext, this);
        this.listenTo(this.stepBarView, 'prev', this.onClickPrev, this);

        this.setLoadingHeight();

    },

    render: function () {
        var self = this,
            step = this.stateModel.get('step');

        if (this.currentView) {
            this.currentView.remove();
            delete this.currentView;
        }


        if (this.dataviewModel.dataset.get('tables').length === 0) {
            this.stepBarView.$el.addClass('hidden');
            this.currentView = new DisclamerView();
        } else if (step === 0) {
            this.currentView = new SelectDataView({
                datasetModel: this.dataviewModel.dataset,
                dataviewModel: this.dataviewModel,
            });
        } else if (step === 1) {
            this.currentView = new MetadataView({
                model: this.dataviewModel,
                categories: this.categories
            });
            this.listenTo(this.currentView, 'valid', this.enable, this);
        } else if (step === 2) {
            this.currentView = new PreviewView({
                model: this.dataviewModel
            });
        }
        this.$('.current-step').empty();
        this.$('.current-step').append(this.currentView.$el);

        this.currentView.render();
        this.stepBarView.render();
    },

    onClickNext: function () {
        if (this.currentView.isValid()) {
            this.stateModel.next();
        }
    },

    onClickPrev: function () {
        this.stateModel.prev();
    },

    onClickSave: function () {
        this.dataviewModel.save().then(function (response) {
            window.location.replace('/dataviews/' + response.datastream_revision_id);
        }).fail(function (response) {
            this.stateModel.set('step', 2);
        });
    },

    setLoadingHeight: function(){

        $(window).resize(function(){

            var windowHeight = $(window).height(),
                sectionTitleHeight = $('.main-section .section-title').height();

            var sectionContentHeight =
                windowHeight
                - $('.global-navigation').height()
                - sectionTitleHeight;

            $('.loading').css({
                'height': sectionContentHeight+'px',
                'margin-top': -sectionTitleHeight / 2

            });

        }).resize();

    }, 
    
});