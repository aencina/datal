var AffectedResourcesCollection = Backbone.Collection.extend({
    model: affectedResourcesModel,
    url: '/dataviews/retrieve_childs/'
});