var AffectedResourcesCollection = Backbone.Collection.extend({
    model: affectedResourcesModel,
    url: '/datasets/retrieve_childs/'
});