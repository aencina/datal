var Notes = Backbone.Model.extend({
    defaults: {
        $AddButton: null
        , $Form: null
        , formPrefix: ''
        , niceEditor: null
        , $EditButton: null
        , $ViewMoreButton: null
		, is_datastream : false
    }
    , initialize: function(){
		var att = this.attributes;
        att.$AddButton.click(_.bind(this.displayForm, this));
        att.$EditButton.click(_.bind(this.displayForm, this));

        att.$Form.submit(_.bind(this.validate ,this));

        att.$ViewMoreButton.toggle(_.bind(this.viewMore ,this), _.bind(this.viewLess ,this))
    }
    , displayForm: function(){
        var att = this.attributes;
        var $lToHide = att.$AddButton.add('.notesContainer');
        $lToHide.fadeOut('fast', _.bind(function(){
            var att = this.attributes;
            att.$Form.fadeIn(_.bind(this.initializeEditor, this));
        }, this));
    }
    , hideForm: function(){
        var att = this.attributes;
        att.$Form.fadeOut('fast', _.bind(function(){
            var att = this.attributes;
            var lEditor = this.getEditor();
            $('.notesContainer').html(lEditor.getContent()).fadeIn();
            att.$EditButton.prev().fadeIn();
            att.$EditButton.fadeIn();
            att.$ViewMoreButton.fadeIn();
        }, this));
    }
    , getEditor: function() {
        return nicEditors.findEditor('id_notes');
    }
    , initializeEditor: function() {
        var att = this.attributes;
        if (this.getEditor() == null) {
            // use fullPanel: true for all button or select some buttons: buttonList : ['bold','italic','underline','ul']
            var lEditor = new nicEditor({fullPanel: true, iconsPath: '/js_core/plugins/nicEdit/nicEditorIcons-2014.gif'}).panelInstance('id_notes');
        }
    }
    , validate: function(pEvent){
        pEvent.preventDefault();
        var att = this.attributes;
        var lEditor = this.getEditor();
        var lNotes = lEditor.getContent().replace(/<br>$/, '');
        lEditor.setContent(lNotes);
        lEditor.saveContent();
        this.submitForm(att.$Form.get(0));
    }
    , submitForm: function(pForm){
        var att = this.attributes;
		att.$Form.find('[name*=csrfmiddlewaretoken]').val(csrfmiddlewaretoken);
        var lUrl = att.$Form.attr('action');
        var lData = att.$Form.serialize();
        this.blockForm();

        $.ajax({
            url: lUrl,
            type: 'POST',
            data: lData,
            dataType: 'json',
            success: _.bind(this.onSuccess, this),
            error: _.bind(this.onError, this),
            complete: _.bind(this.onComplete, this)
        });
        return false;
    }
    , onSuccess: function(pResponse){
        if (pResponse.status == 'ok') {
			if(this.attributes.is_datastream){
				if(pResponse.datastream_revision_id != $('#id_datastream-datastream_revision_id').val()){
					window.location.replace('/dataviews/view/?datastream_revision_id=' + pResponse.datastream_revision_id);
					jQuery.TwitterMessage({ 'type': 'success', 'message': pResponse.messages });
				}else{
					
				}
			}else{
				if(pResponse.dashboard_revision_id != fDashboardId){
					fDashboardId = pResponse.dashboard_revision_id;
					jQuery.TwitterMessage({ 'type': 'success', 'message': pResponse.messages });
				}else{
					
				}
			}
            this.hideForm();
        } else {
            this.onError(pResponse);
        }
    }
    , onError: function(pResponse){
        jQuery.TwitterMessage({ 'type': 'error', 'message': pResponse.messages.join('. ') });
    }
    , onComplete: function(){
        this.unblockForm();
    }
    , blockForm: function () {
        this.attributes.$Form.find('input[type=submit]').attr('disabled', 'disabled');
    }
    , unblockForm: function () {
        this.attributes.$Form.find('input[type=submit]').removeAttr('disabled');
    }
    , viewMore: function () {
        $('.notesContainer').css({'max-height': 'none', 'overflow': 'visible'});
        this.attributes.$ViewMoreButton.addClass('expanded');
    }
    , viewLess: function () {
        $('.notesContainer').css({'max-height': '64px', 'overflow': 'hidden'});
        this.attributes.$ViewMoreButton.removeClass('expanded');
    }
});