var embedChart = Backbone.Model.extend({
    defaults: {
        'title': "",
        'width': 450,
        'height': 300,
        'url': ""
    },
    initialize: function(){
        
    },
    validate: function(attributes, options){
        var errors  = {};       
        var isValid = this.validateHeight(attributes.height, errors) 
                    && this.validateWidth(attributes.width, errors);
                
        if(!isValid){
            return errors;
        }
    },
    validateHeight: function(height, errors){
        var errorList = [];
        
        if(isNaN(height)){
            errorList.push( gettext('EMBED-HEIGHT-ERROR') );
        }
        errors.height = errorList;
        
        if(_.isEmpty(errorList)){
            return true;
        }
        return false;
    },
    validateWidth: function(width, errors){
        var errorList = [];
        
        if(isNaN(width)){
            errorList.push( gettext('EMBED-WIDTH-ERROR') );
        }
        errors.width = errorList;
        
        if(_.isEmpty(errorList)){
            return true;
        }
        return false;
    },  
});