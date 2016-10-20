var FiltersCollection = Backbone.Collection.extend({
    model: FilterModel,

    comparator: 'column',

    add: function(models, options){
        var l = this.countBy(function (model) {
            return model.get('type');
        }).parameter || 0;

        if (_.isUndefined(models)) {
            // An add event is fired when reset is called. If reset receives no parameters, 
            // the add method does not receive the models parameter
            return;
        }

        if (!_.isArray(models)) {
            models = [models];
        }

        // If added model is of type 'parameter', we add a position attribute to it.
        _.each(models, function (model, i) {
            if (model.get('type') === 'parameter' && _.isUndefined(model.get('position'))) {
                model.set('position', l + i);
            }
        });
        Backbone.Collection.prototype.add.call(this, models, options);
    },

    toSampleFilters: function () {
        var result = {};

        var parameterFilters = this.models.filter(function (model) {
            return model.get('type') === 'parameter';
        });
        _.each(parameterFilters, function (model) {
            result['pArgument' + model.get('position')] = model.get('default');
            result['pParameter' +  model.get('position')] = model.get('name');
        });

        return result;
    },

    toFormSet: function () {
        var payload = this.filter(function (model) {
            return model.get('type') === 'parameter';
        }).map(function (model) {
            return model.pick(['name', 'description', 'default', 'position']);
        });
        return payload;
    }
});