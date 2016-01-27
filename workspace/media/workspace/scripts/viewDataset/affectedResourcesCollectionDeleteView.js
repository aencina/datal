var AffectedResourcesCollectionDeleteItemView = Backbone.View.extend({

    el: '#id_confirmDeleteDataset',

    affectedResourcesHTML: '',

    events: {
        "click #id_deleteRelatedResources": "deleteRelatedResources",
        "click .close, .cancel": "closeOverlay",
    },

    initialize: function(options) {

        this.parentView = options.parentView;
        this.models = options.models;
        this.type = options.type;

        // init Overlay
        this.$el.overlay({
            top: 'center',
            left: 'center',
            mask: {
                color: '#000',
                loadSpeed: 200,
                opacity: 0.5,
                zIndex: 99999
            }
        });

        var total = this.models.length,
            self = this;

        // For each selected model, fetch related resources
        _.each(this.models, function(model, index) {

            self.collection.fetch({
                data: $.param({
                    revision_id: model.get('id'),
                    dataset_id: model.get('dataset_id'),
                    type: self.type
                }),
                success: function(model, response) {
                    
                    if (self.collection.length > 0) {
                        _(self.collection.models).each(function(model) {
                            self.addResource(model);
                        }, self);
                    }

                    // If last model iterated, check if related resources in all model iterations, have been fetched and render, else delete resources without prompting an overlay
                    if (index === total - 1) {
                        if (self.affectedResourcesHTML) {
                            self.render();
                        } else {
                            self.deleteRelatedResources();
                        }
                    }

                }
            });


        });

        this.collection.bind('reset', this.render);
        
    },

    render: function() {
        this.$el.find('#id_affectedResourcesList').html( this.affectedResourcesHTML );

        var self = this;
        setTimeout(function(){
            self.$el.data('overlay').load();
        }, 250);
    },

    addResource: function(model) {
        // Add new affected resource to DOM
        var theView = new affectedResourcesView({
            model: model
        });
        this.affectedResourcesHTML += theView.render().el.outerHTML;
    },

    deleteRelatedResources: function() {
        var self = this;
        _.each(this.models, function(model) {
            resource = model.get('title');
            model.remove({
                
                beforeSend: function(xhr, settings){
                    // Prevent override of global beforeSend
                    $.ajaxSettings.beforeSend(xhr, settings);
                    // Show Loading
                    $("#ajax_loading_overlay").show();
                },

                success: function(response, a) {
                    $.gritter.add({
                        title: gettext('APP-OVERLAY-DELETE-DATASET-CONFIRM-TITLE'),
                        text:  resource + ": "+ gettext('APP-DELETE-DATASET-ACTION-TEXT'),
                        image: '/static/workspace/images/common/ic_validationOk32.png',
                        sticky: false,
                        time: 3500
                    });
                    self.closeOverlay();
                    self.undelegateEvents();

                    var location = window.location.href,
                        splitURL = location.split("/"),
                        cutURL = splitURL.slice(0, -2),
                        joinURL = cutURL.join("/");

                    setTimeout(function () {
                        window.location = joinURL;
                    }, 2000);
                    
                },

                error: function() {
                    $.gritter.add({
                        title: gettext('APP-OVERLAY-DELETE-DATASET-CONFIRM-TITLE'),
                        text: resource + ": "+  gettext('APP-DELETE-DATASET-ACTION-ERROR-TEXT'),
                        image: '/static/workspace/images/common/ic_validationError32.png',
                        sticky: true,
                        time: 2500
                    });
                    self.closeOverlay();
                    self.undelegateEvents();
                }
            });

        });

    },

    closeOverlay: function() {
        $("#ajax_loading_overlay").hide();
        this.$el.data('overlay').close();
    }

});
