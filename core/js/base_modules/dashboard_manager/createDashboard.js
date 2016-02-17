var CreateDashboard = Backbone.Model.extend({
    defaults: {
        url: '/dashboards/action_insert/',
        $Container: null,
        $Form: null
    },
    initialize: function(container){
        this.attributes.$Form = this.attributes.$Container.find('#id_dashboard_form');
        this.attributes.$Form.validate({
            rules: {
                'dashboard-title': {
                    'required': true,
                    'maxlength': 80,
                    'regex': /^.*[a-zA-Z0-9]+.*$/
                },
                'dashboard-description': {
                    'required': true,
                    'maxlength': 140
                }
            },
            messages: {
                'dashboard-title': {regex: gettext( "VALIDATE-REGEX" )}
            }
        });

        this.attributes.$Container.find('#id_save_draft').click(_.bind(this.saveDraft, this));
		this.attributes.$Container.find('#id_review').click(_.bind(this.saveReview, this));
		this.attributes.$Container.find('#id_approve').click(_.bind(this.saveApproved, this));
		this.attributes.$Container.find('#id_publish').click(_.bind(this.savePublished, this));
		
        this.attributes.$Container.find('#id_dashboard_tag').tagging({
            tagContainer : '#'+this.attributes.$Container.attr("id") +' #id_tag_container',
            source: '/rest/tags.json/',
            minLength: 3
        });
    },
	save : function(){
		this.attributes.url = '/dashboards/edit_dashboard/';
		this.onSubmit();
	},
	saveDraft : function(){
		this.attributes.url = '/dashboards/save_dashboard_as_draft/';
		this.onSubmit();
	},
	saveReview : function(){
		this.attributes.url = '/dashboards/save_dashboard_as_review/';
		this.onSubmit();
	},
	saveApproved : function(){
		this.attributes.url = '/dashboards/save_dashboard_as_approved/';
		this.onSubmit();
	},
	savePublished : function(){
		this.attributes.url = '/dashboards/save_dashboard_as_published/';
		this.onSubmit();
	},
    onSubmit: function(){
        if (this.attributes.$Form.valid()) {
            var lUrl = this.attributes.url;

            var lTagForm 		= this.serializeTags();
            var lDashboardForm 	= this.serializeForm();
			var lMetaData		= this.serializeMetaData();
            
			var lData = lTagForm + '&' + lDashboardForm +'&'+ lMetaData;
			
            $.ajax({
                url: lUrl,
                type: 'POST',
                data: lData,
                dataType: 'json',
                success: _.bind(this.onSuccess, this),
                error: _.bind(this.onError, this)
            });
        }

        return false;
    },
    onSuccess: function(pResponse){
        if (pResponse.status == "ok") {
			this.resetForm();
			$(this.get("container")).trigger('datatable:refresh:pagination');
			$('#id_create_dashboard_overlay').data("overlay").close();
            if($.inArray('ao-publisher', authManager.get("roles")) != -1 || $.inArray('ao-account-admin', authManager.get("roles")) != -1){
                $.gritter.add({
                    title: gettext("NOTIF-SAVED-TITLE"),
                    text: gettext("NOTIF-SAVED-DESC-4"),
                    image: '/static/core/images/common/im_defaultAvatar_90x90.jpg',
                    sticky: true,
                    time: ''
                });
            }
                            
            return false;
        }else{
			jQuery.TwitterMessage({
                type: 'error',
                message: pResponse.messages.join('. ')
            });
		}
    },
    onError: function(pResponse){
        //on error callback
    },
    serializeForm: function(){
        var lDashboardForm = this.attributes.$Form;

        var lData = {
          'dashboard-title': $('#id_dashboard-title', lDashboardForm).val()
          , 'dashboard-description': $('#id_dashboard-description', lDashboardForm).val()
		  , 'dashboard-category': $('#id_dashboard-category', lDashboardForm).val()
		  , 'csrfmiddlewaretoken': csrfmiddlewaretoken
        }

        return $.param(lData);
    },
    serializeTags: function(){
        var lData = {};
        var lEditTagsContainer = this.attributes.$Container.find('#id_tag_container');
        var $lTags = $('[id*=id_tag_][id$=_name]', lEditTagsContainer);

        $lTags.each(function(i){
            var $lTag = $(this);
            lData['tags-' + i + '-name'] = $.trim($lTag.text());
        });

        lData['tags-TOTAL_FORMS'] = $lTags.length;
        lData['tags-INITIAL_FORMS'] = 0;

        return $.param(lData);
    }, 
	serializeMetaData : function(){
		var lFields = $('[name*=cust-]');
		var lData = {};
		
		for (var i = 0; i < lFields.size(); i++){
			var lField = lFields.eq(i);
			lData[lField.attr('name')] = $.trim(lField.val());
		};
		
		return $.param(lData);
	},
	resetForm : function(){
		this.attributes.$Form.find(':input').val("");
		this.attributes.$Form.find('#id_tag_container').html('');
	}
});

var UpdateDashboard = CreateDashboard.extend({
    defaults : {
        url : '/dashboards/action_update'
    },
	initialize:  function(){
		CreateDashboard.prototype.initialize.call(this);
		_.defaults(this.attributes, CreateDashboard.prototype.defaults);

        this.attributes.$Container.find('#id_save').click(_.bind(this.save, this));
	},
    onSubmit: function(){
        if (this.attributes.$Form.valid()) {
            var lUrl = this.attributes.url;

            var lTagForm 		= this.serializeTags();
            var lDashboardForm 	= this.serializeForm();
			var lMetaData		= this.serializeMetaData();
            
			var lData = "dashboard-dashboard_revision_id=" + $('#id_dashboard-dashboard_revision_id').val()+  '&'+lTagForm + '&' + lDashboardForm +'&'+ lMetaData;
			
            $.ajax({
                url: lUrl,
                type: 'POST',
                data: lData,
                dataType: 'json',
                success: _.bind(this.onSuccess, this),
                error: _.bind(this.onError, this)
            });
        }

        return false;
    },
    onSuccess: function(pResponse){
        if (pResponse.status == "ok") {
				
				var lName = $("#id_dashboard-title", this.attributes.$Container).val();
				var lDescription = $("#id_dashboard_descriptions", this.attributes.$Container).val();
				var $lTags = this.attributes.$Container.find('[id*=id_tag_][id$=_name]');
				
				if ($lTags.length >= 0) {
					var lDashboardTagsContainer = $("#id_dashboard_tags_container");
					var lDashboardAllTagsContainer = $("#id_dashboard_alltags_container");
					
					$(".tagsContainer").show();
					
					var lHtml = '';
					$lTags.slice(0, 5).each(function(i){
						var $lTag = $(this);
						lHtml = lHtml + '<a href="" title="' + $lTag.text() + '">' + $lTag.text() + '</a>, '
					});
					lHtml = lHtml.substring(0, lHtml.length - 2);
					lDashboardTagsContainer.html(lHtml);
					
					lHtml = '';
					$lTags.each(function(i){
						var $lTag = $(this);
						lHtml = lHtml + '<a href="" title="' + $lTag.text() + '">' + $lTag.text() + '</a>, ';
					});
					lHtml = lHtml.substring(0, lHtml.length - 2);
					lDashboardAllTagsContainer.html(lHtml);
					
				}
				
				$('#id_maximized_dashboard_name').text(lName);
				$('#id_maximized_dashboard_description').text(lDescription);
				
				$("#id_edit_dashboard_container").data("overlay").close();
				
				$('.tab-selected a').eq(0).text(lName)

                if(fDashboardId != pResponse.dashboard_revision_id){
                    $('#id_dashboard-dashboard_revision_id').val(pResponse.dashboard_revision_id);
                    fDashboardId = String(pResponse.dashboard_revision_id);
                    $('#id_dashboard_container').data('dashboard_id',fDashboardId );
                    $('#id_dashboard_container').data('dashboard_status', "0");
                    dashboardStatus.set({'status' : '0'});
                    dashboardStatus.renderButtons();
                }

                jQuery.TwitterMessage({
                    type: 'success',
                    message: pResponse.messages.join(". ")
                });

                return;
		}
        if (pResponse.status == "error") {
            $.TwitterMessage({type: 'error', message: pResponse.messages.join('. ') });
        }
    }
});
