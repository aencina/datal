(function ($, Backbone, global, undefined) {

    var ErrorManagerModel = Backbone.Model.extend({
        defaults: {
            "error": "",
            "description": "",
            "status": "",
            "type": "",
            "actions": []
        },
        /**
         * Filter the error source data to match the error model
         * @param  {object}
         */
        assignRaw: function (errorSource) {
            console.log('ErrorManager', 'Error Source Object:', errorSource);

            //Handling Jquery ajax error data source
            if(typeof errorSource['jqXHR'] !== 'undefined'){
                errorSource = errorSource.jqXHR;
            }


            //Get the error message from the ajax response text
            if(typeof errorSource['responseText'] !== 'undefined'){
                errorMessage = errorSource.responseText;
            }

            //Normalize error message data type
            if(typeof errorMessage !== 'object'){
                try {
                    errorMessage = JSON.parse(errorMessage);
                } catch(e){
                    console.error(e); //error in the above string(in this case,yes)!
                }
            }

            //Check if we are handling and old version of the error messages
            if(typeof errorMessage['messages'] !== 'undefined'){
                errorMessage = this.normalizeOldErrorFormat(errorMessage);
            }

            //Validate the format of the error message
            if(typeof errorMessage['description'] !== 'undefined' && typeof errorMessage['error'] !== 'undefined'){
                // changed to fire change every time it is set
                if (errorSource.hasOwnProperty('onClose')) {
                    errorMessage['responseOnClose'] = errorSource.onClose
                }
                this.set(errorMessage, {silent: true}).trigger('change');
            }
            else{
                this.setUnexpectedErrorMessage();
            }
        },
        setUnexpectedErrorMessage: function () {
            console.log('ErrorManager', 'Unexpected Error Message, please report to development team', errorMessage);
            //TODO: Define a better unexpected error message 
            this.set({
                "error": gettext("APP-ERROR-TEXT"),
                "description": gettext("APP-ERROR-TEXT"),
                "status": "",
                "type": "",
                "actions": []
            });
        },
        normalizeOldErrorFormat: function (errorMessage) {
            errorMessage.description = errorMessage.messages;

            if(typeof errorMessage.description === 'array')
                errorMessage.description = errorMessage.description.join('. ');

            if(typeof errorMessage['status'] !== 'undefined')
                errorMessage.error = errorMessage.status.charAt(0).toUpperCase() + errorMessage.status.slice(1);
            else
                errorMessage.error = 'Error';

            return errorMessage;
        }
    });

    global.errorManagerModel = new ErrorManagerModel();
})(jQuery, Backbone, window);