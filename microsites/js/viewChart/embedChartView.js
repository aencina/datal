var embedChartView = Backbone.View.extend({

    el: '#id_embedContainer',    
    
    template: null,
    
    events:{
        'click #id_embedCode': 'onTextareaClicked',
        'change #id_embedWidth': 'onSizeChanged',
        'change #id_embedHeight': 'onSizeChanged',
    },
    
    $widthInput: null,
    $heightInput: null,
    
    initialize: function() {

        $widthInput     = this.$el.find('#id_embedWidth').val(this.model.get('width'));
        $heightInput    = this.$el.find('#id_embedHeight').val(this.model.get('height'));
        
        _.templateSettings = {
            interpolate : /\{\{(.+?)\}\}/g
        };
    
        var tmpl = '<iframe title="{{title}}" width="{{width}}" height="{{height}}" src="{{url}}" ';
        tmpl += 'frameborder="0" style="border:1px solid #E2E0E0;padding:0;margin:0;"></iframe>';
        tmpl += '<p style="padding:3px 0 15px 0;margin:0;font:11px arial, helvetica, sans-serif;color:#999;">';
        tmpl += gettext( "APP-POWEREDBY-TEXT" );
        tmpl += ' <a href="' + Configuration.APPLICATION_DETAILS.website + '" title="' + gettext( "APP-POWEREDBY-TITLE" ) + '" style="color:#0862A2;">' + Configuration.APPLICATION_DETAILS.name + '</a></p>';
        
        this.template =  _.template(tmpl); 
        
        this.listenTo(this.model, "change", this.render);
        this.listenTo(this.model, "invalid", this.onValidationErrors);
        
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
        
        this.$el.data('overlay').load();
        
        this.render();

    },
    
    render: function() {
        this.$el.find('#id_embedCode').text(this.template(this.model.attributes));
        return this;
    },
    
    onValidationErrors: function(){ 
        var errors      = this.model.validationError;
        
        if(!_.isUndefined(errors.height)){
            $heightInput.val(this.model.get('height'));
        }
        
        if(!_.isUndefined(errors.width)){
            $widthInput.val(this.model.get('width'));
        }
        
    },

    onTextareaClicked: function(event){
        var textarea = event.currentTarget;
        $(textarea).select();
    },
    
    onSizeChanged: function(){
        
        this.model.set({
            'height': $.trim($heightInput.val()), 
            'width': $.trim($widthInput.val())
        },{ 
            validate:true 
        });
        
    }

});