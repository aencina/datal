var charts = charts || {
    models: {},
    views: {}
};

charts.views.MapChart = charts.views.Chart.extend({
    mapInstance: null,
    mapMarkers: [],
    mapClusters: [],
    mapTraces: [],
    latestDataUpdate: null,
    latestDataRender: null,
    styles: {},
    stylesDefault: {
        'marker': {
            icon : 'https://maps.gstatic.com/mapfiles/ms2/micons/red-pushpin.png'
        },
        'lineStyle': {
            'strokeColor': '#00FFaa',
            'strokeOpacity': 1.0,
            'strokeWeight': 2,
            'fillColor': '#FF0000',
            'fillOpacity': 0.01
        },
        'polyStyle': {
            'strokeColor': '#FF0000',
            'strokeOpacity': 1.0,
            'strokeWeight': 3,
            'fillColor': '#FF0000',
            'fillOpacity': 0.35
        },
    },
    initialize: function(options){
        this.googleMapOptions = options.mapOptions || {};
        this.bindEvents();
        this.createGoogleMapInstance();
    },

    render: function () {
        this.clearMapOverlays();
        if(this.model.data.get('points') && this.model.data.get('points').length){
            this.createMapPoints();
        }
        if(this.model.data.get('clusters') && this.model.data.get('clusters').length){
            this.createMapClusters();
        }
        return this;
    },

    handleDataUpdated: function () {
        this.clearMapOverlays();
        this.render();
    },

    bindEvents: function () {
        this.listenTo(this.model, 'change', this.render, this);
        this.listenTo(this.model, 'change:mapType', this.onChangeMapType, this);
        this.listenTo(this.model, 'data_updated', this.handleDataUpdated, this);
    },

    onChangeMapType: function (model, type) {
        if (this.mapInstance) {
            this.mapInstance.setMapTypeId(google.maps.MapTypeId[type]);
        }
    },

    /**
     * Add event handlers to the map events
     */
    bindMapEvents: function () {
        this.mapInstance.addListener('idle', this.handleBoundChanges.bind(this));
    },

    /**
     * Creates a new map google map instance
     */
    createGoogleMapInstance: function () {


        var mapInitialOptions = {
            zoom: this.model.get('options').zoom,
            mapTypeId: google.maps.MapTypeId[this.model.get('mapType')],
            backgroundColor:'#FFFFFF'
        };

        if(this.model.get('options').center){
            mapInitialOptions.center = new google.maps.LatLng(
                    this.model.get('options').center.lat,
                    this.model.get('options').center.long
                    );
        }
        
        console.log('create_map',this.model.get('options'));

        if(this.model.get('options').bounds){
            var b = this.model.get('options').bounds;
            var southWest = new google.maps.LatLng(parseFloat(b[2]),parseFloat(b[3])),
                northEast = new google.maps.LatLng(parseFloat(b[0]),parseFloat(b[1])),
                bounds = new google.maps.LatLngBounds(southWest,northEast);
                mapInitialOptions.center = bounds.getCenter();
        }

        this.mapInstance = new google.maps.Map(this.el, mapInitialOptions);
        this.mapInstance.setOptions(this.googleMapOptions);
        this.mapInstance.setOptions({minZoom: 1});

        this.infoWindow = new google.maps.InfoWindow();
        this.bindMapEvents();
    },

    /**
     * Remueve los elementos del mapa y elimina cualquier evento asociado a estos
     */
    clearMapOverlays: function () {
        //Markers
        this.mapMarkers = this.clearOverlay(this.mapMarkers);
        //Clusters
        this.mapClusters = this.clearOverlay(this.mapClusters);
        //Traces
        this.mapTraces = this.clearOverlay(this.mapTraces);
    },

    /**
     * Elimina una coleccion especifica de elementos sobre el mapa
     * @param  {array} overlayCollection
     */
    clearOverlay: function (overlayCollection) {
        _.each(overlayCollection, function (overlayElement, index) {
            if (_.isUndefined(overlayElement)) return;
            overlayElement.setMap(null);
            //Elimina los eventos asociados al elemento
            if(overlayElement.events){
                _.each(overlayElement.events, function (event) {
                    google.maps.event.removeListener(event);
                });
            }
        }, this);
        return [];
    },

    /**
     * Crea puntos en el mapa, pueden ser de tipo traces o markers
     */
    createMapPoints: function () {
        var self = this,
            styles = this.parseKmlStyles(this.model.get('styles'));
        _.each(this.model.data.get('points'), function (point, index) {
            if(point.trace){
                this.createMapTrace(point, index, styles);
            } else {
                this.createMapMarker(point, index, styles);
            }
        }, this);
    },

    /**
     * Crea un trace de puntos dentro del mapa
     * @param  {object} point   Objeto con el trace de los puntos en el mapa
     * @param  {int} index      Indice del trace en el arreglo local de traces
     * @param  {object} styles  Estilos para dibujar el trace
     */
    createMapTrace: function (point, index, styles) {
        var paths = _.map(point.trace, function (tracePoint, index) {
            return {lat: parseFloat(tracePoint.lat), lng: parseFloat(tracePoint.long)};
        });

        var isPolygon = (paths[0].lat == paths[paths.length-1].lat && paths[0].lng == paths[paths.length-1].lng);

        if(isPolygon){
            this.mapTraces.push(this.createMapPolygon(paths, styles.polyStyle));
        } else {
            this.mapTraces.push(this.createMapPolyline(paths, styles.lineStyle))
        }
        this.mapTraces[index].setMap(this.mapInstance);
    },

    createMapPolygon: function (paths, styles) {
        return new google.maps.Polygon({
            paths: paths,
            strokeColor: styles.strokeColor,
            strokeOpacity: styles.strokeOpacity,
            strokeWeight: styles.strokeWeight,
            fillColor: styles.fillColor,
            fillOpacity: styles.fillOpacity
        });
    },

    createMapPolyline: function (path, styles) {
        return new google.maps.Polyline({
            path: path,
            strokeColor: styles.strokeColor,
            strokeOpacity: styles.strokeOpacity,
            strokeWeight: styles.strokeWeight
        });
    },

    /**
     * Crea un marker dentro del mapa
     * @param  {object} point   Objeto con las coordenadas del punto en el mapa
     * @param  {int}    index   Indice del punto en el arreglo local de markers
     * @param  {object} styles  Estilos para dibujar el marker
     */
    createMapMarker: function (point, index, styles) {
        var self = this,
            markerIcon = this.stylesDefault.marker.icon;

        //Obtiene el estilo del marcador
        if(styles && styles.iconStyle){
            markerIcon = styles.iconStyle.href;
        }

        this.mapMarkers[index] = new google.maps.Marker({
            position: new google.maps.LatLng(point.lat, point.long),
            map: this.mapInstance,
            icon: markerIcon
        });

        if(point.info){
            var clickHandler = google.maps.event.addListener(this.mapMarkers[index], 'click', (function (marker, info) {
                return function() {
                    self.infoWindow.setContent("<div class='junarinfowindow'>" + String(info) + "</div>");
                    self.infoWindow.open(self.mapInstance, marker);
                }
            })(self.mapMarkers[index], point.info));
            this.mapMarkers[index].events = {click: clickHandler};
        }
    },

    /**
     * Crea clusters de puntos
     */
    createMapClusters: function () {
        var self = this;
        _.each(this.model.data.get('clusters'), this.createMapCluster, this);
    },

    /**
     * Crea un cluster de puntos 
     * @param  {object} cluster
     * @param  {int} index
     */
    createMapCluster: function (cluster, index) {
        cluster.noWrap = true;

        // Se desabilita la funcionalidad de joinIntersectedClusters porque contiene problemas
        this.mapClusters[index] = new multimarker(cluster, cluster.info, this.mapInstance, false /* joinIntersectedClusters */);
    },

    /**
     * Get the boundaries of the current map
     */
    handleBoundChanges: function(){

        if(this.mapInstance){

            var center = this.mapInstance.getCenter(),
                bounds = this.mapInstance.getBounds(),
                zoom = this.mapInstance.getZoom();

            var updatedOptions = {
                zoom: zoom
            };

            if(bounds){
                updatedOptions.bounds = [
                        bounds.getNorthEast().lat(), 
                        bounds.getNorthEast().lng(), 
                        bounds.getSouthWest().lat(), 
                        bounds.getSouthWest().lng()
                    ];
            }

            if(center){
                updatedOptions.center = {
                    lat: center.lat(),
                    long: center.lng(),
                };
            }

            this.model.set('options', updatedOptions);

        }

    },

    /**
     * Convierte estilos de tipo kml al necesario para usar en los mapas
     * @param  {object} styles
     * @return {object}
     */
    parseKmlStyles: function (styles) {
        styles = styles || [];
        var parsedStyles = this.stylesDefault;

        if(styles.length && styles[0].styles){
            //Obtiene el primer estilo encontrado en la data
            styles = styles[0].styles;
            if(styles.lineStyle){
                parsedStyles.lineStyle = this.kmlStyleToLine(styles.lineStyle);
            }
            if(styles.polyStyle){
                parsedStyles.polyStyle = this.kmlStyleToPolygon(parsedStyles.lineStyle, styles.polyStyle);
            }
        }

        return parsedStyles;
    },

    /**
     * Prser para los estilos desde un kml a lineas de google maps
     * @param  {object} lineStyle
     * @return {object
     */
    kmlStyleToLine: function(lineStyle) {
        var defaultStyle = this.get('stylesDefault').lineStyle;
        return {
            "strokeColor": this.getStyleFromKml(lineStyle, 'color', 'color', defaultStyle.strokeColor),
            "strokeOpacity": this.getStyleFromKml(lineStyle, 'color', 'opacity', defaultStyle.strokeOpacity),
            "strokeWeight": this.getStyleFromKml(lineStyle, 'width', 'width', defaultStyle.strokeWeight)
        };
    },

    /**
     * Parser para los estilos de un kml a polygons de google maps
     * @param  {object} lineStyle
     * @param  {object} polyStyle
     * @return {object}
     */
    kmlStyleToPolygon: function (lineStyle, polyStyle) {
        var defaultStyle = this.get('stylesDefault').polyStyle;
        var opacity = this.getStyleFromKml(polyStyle, 'fill', 'opacity', defaultStyle.strokeWeight);
        return {
            "strokeColor": lineStyle.strokeColor,
            "strokeOpacity": lineStyle.strokeOpacity,
            "strokeWeight": lineStyle.strokeWeight,
            "fillColor": this.getStyleFromKml(polyStyle, 'fill', 'color', defaultStyle.strokeWeight),
            "fillOpacity": this.getStyleFromKml(polyStyle, 'fill', 'opacity', defaultStyle.strokeWeight)
        };
    },

    /**
     * Obtiene un estilo de un objeto de estilos Kml para ser usado en google maps
     * @param  {object} kmlStyles
     * @param  {string} attribute
     * @param  {string} type
     * @param  {string} defaultStyle
     * @return {string}
     */
    getStyleFromKml: function (kmlStyles, attribute, type, defaultStyle) {
        var style = kmlStyles[attribute] || null;
        if(style == null) return defaultStyle;

        //Convierte el color de formato ARGB a RGB
        if(type == 'color')
            return '#' + style.substring(2);
        //La opacidad se extrae del color y convierte de hexadecimal a entero
        if(type == 'opacity')
            return parseInt(style.substring(0, 2), 16) / 256;

        return style;
    }


});