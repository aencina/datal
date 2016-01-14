var SourcesCollection = Backbone.Collection.extend({
  model: SourceModel,

  add: function(models, options){

    // Validate if name is already in collection
    var match = this.where({name: models.name}),
      errorMsg = '';

    if(match.length == 0){
      Backbone.Collection.prototype.add.call(this, models, options);
    }else{
      errorMsg = gettext('VALIDATE-SOURCENAMEINCOLLECTION-TEXT');
    }
    this.trigger('validateAdd', errorMsg );
  }
})