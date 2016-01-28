var DeleteItemView = Backbone.View.extend({
	
	el: '#id_deleteVisualization',

	parentView: null,
	
	events: {
		"click #id_deleteResource": "deleteVisualization",
		"click #id_deleteRevision": "deleteRevision"
	},

	initialize: function(options) {

    this.parentView = options.parentView;
    this.itemCollection = options.itemCollection;
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
		
		// Render
		this.render();

	},

	render: function(){
		this.$el.data('overlay').load();
	},

	deleteVisualization: function() {
		
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
                    title: gettext('APP-DELETE-VISUALIZATION-TEXT'),
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
                    title: gettext('APP-DELETE-VISUALIZATION-TEXT'),
                    text: resource + ": "+  gettext('APP-DELETE-VISUALIZATION-ACTION-ERROR-TEXT'),
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

	deleteRevision: function() {
		self = this;
		_.each(this.models, function(model) {

			var resource = model.get('title');

			model.remove_revision({
				
                beforeSend: function(xhr, settings){
                    // Prevent override of global beforeSend
                    $.ajaxSettings.beforeSend(xhr, settings);
                    // Show Loading
                    $("#ajax_loading_overlay").show();
                },

				success: function(response, a) {
					$.gritter.add({
						title: gettext('APP-OVERLAY-DELETE-VISUALIZATION-CONFIRM-TITLE'),
						text: resource + ": " + gettext('APP-DELETE-VISUALIZATION-REV-ACTION-TEXT'),
						image: '/static/workspace/images/common/ic_validationOk32.png',
						sticky: false,
						time: 3500
					});
					self.closeOverlay();
					self.undelegateEvents();

                    var deleteRevisionID = a['revision_id'],
                        location = window.location.href,
                        splitURL = location.split("/"),
                        cutURL = splitURL.slice(0, -2),
                        joinURL = cutURL.join("/");

                    if(deleteRevisionID == -1){
                        setURL = joinURL;
                    }else{
                        setURL = joinURL + "/" + deleteRevisionID;
                    }

                    setTimeout(function () {
                           window.location = setURL;
                    }, 2000);
				},

				error: function() {
					$.gritter.add({
						title: gettext('APP-OVERLAY-DELETE-VISUALIZATION-TITLE'),
						text: resource + ": " + gettext('APP-DELETE-VISUALIZATION-REV-ACTION-ERROR-TEXT'),
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
