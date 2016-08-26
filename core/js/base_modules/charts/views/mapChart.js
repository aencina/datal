var charts = charts || {
    models: {},
    views: {}
};

charts.views.MapChart = charts.views.Chart.extend({
    mapInstance: null,
    heatMapLayer: null,
    heatMapPoints: [], 
    onHeatMap: false, 
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

        console.log('render');

        this.clearMapOverlays();
        this.clearHeatMapOverlays();
        var points = this.model.data.get('points');
        var clusters = this.model.data.get('clusters');
        var oms = new OverlappingMarkerSpiderfier(this.mapInstance);
        
        var styles = this.model.data.get('mapStyles');
        var styledPoints = this.mergePointsAndStyles(points, styles);

        if(!_.isUndefined(points) && points.length !== 0){
            this.createMapPoints(styledPoints, oms);
        }
        if(!_.isUndefined(clusters) && clusters.length !== 0){
            this.createMapClusters(clusters);
        }

        if (this.onHeatMap) {
            this.heatMapLayer.setData(this.heatMapPoints);
            this.heatMapLayer.setMap(this.mapInstance);
            this.clearMapOverlays();
        }
        else {
            this.heatMapLayer.setMap(null);
            }
        
        return this;
    },

    handleDataUpdated: function () {
        this.render();
    },

    bindEvents: function () {
        this.listenTo(this.model, 'change', this.render, this);
        this.listenTo(this.model, 'change:mapType', this.onChangeMapType, this);
        this.listenTo(this.model, 'data_updated', this.handleDataUpdated, this);
    },

    mergePointsAndStyles: function (points, styles) {
        var self = this,
            result;
        var mapStyles={}
         _.each(styles, function (style) {
            mapStyles[style.id]=style;
         });

        if (_.isUndefined(mapStyles) || mapStyles.length === 0) {
            result = points;
        } else {
            result = _.map(points, function (point, index) {

                // si  no tiene un hash en el hashmap, usa el estilo default
                if ( ! _.isUndefined(mapStyles[point.mapStyle]) ){

                    var mapStyle= mapStyles[point.mapStyle];

                    // si no viene con styles
                    if ( _.isEmpty(mapStyle.styles)){
                        var style={}
                        for (var firstKey in mapStyles[point.mapStyle].pairs) {
                            style[mapStyles[point.mapStyle].pairs[firstKey]]={"style":mapStyles[firstKey].styles};
                        };
                        point.styles = style['normal'].style;

                    // si el mapStyle trae style, usamos ese
                    }else{
                        point.styles = mapStyle.styles;
                    }
                }
    
                return point;
            });
 
       }

        return result;
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

        // TODO: Buscar una solucion a todo esto.

        // Vuelvo atras este cambio, porque hay 342 revisions de visualizaciones que no tienen bounds en el impl_details, entonces eso hace que si quito la linea de idle y uso las otras dos (para evitar los request que hace el idle innecesarios) venga bounds=undefined en los que no lo tienen en el impl_details.

        this.mapInstance.addListener('idle', this.handleBoundChanges.bind(this));
        //this.mapInstance.addListener('dragend', this.handleBoundChanges.bind(this));
        //this.mapInstance.addListener('zoom_changed', this.handleBoundChanges.bind(this));
    },

    /**
     * Creates a new map google map instance
     */
    createGoogleMapInstance: function () {


        var mapInitialOptions = {
            zoom: this.model.get('options').zoom,
            mapTypeId: google.maps.MapTypeId[this.model.get('mapType')],
            backgroundColor:'#FFFFFF',
            zoomControl: true,
        };

        if(this.model.get('options').center){
            mapInitialOptions.center = new google.maps.LatLng(
                    this.model.get('options').center.lat,
                    this.model.get('options').center.long
                    );
        }

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

        // crear instancia del heatmap vacia
        this.heatMapPoints = new google.maps.MVCArray([]);
        this.heatMapLayer = new google.maps.visualization.HeatmapLayer({data: this.heatMapPoints , radius: 20, opacity: 0.8});

        this.infoWindow = new google.maps.InfoWindow({
            disableAutoPan: true,
            maxWidth: 700,
            maxHeight: 400,
            });
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
        
    clearHeatMapOverlays: function() {
        // limpiar el heatmap asociado
        this.heatMapPoints = new google.maps.MVCArray([]);
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
    createMapPoints: function (points, oms) {

        _.each(points, function (point, index) {
            if(point.trace){
                this.createMapTrace(point, index);
            } else {
                this.createMapMarker(point, index, oms);
            }
        }, this);
    },

    /**
     * Crea un trace de puntos dentro del mapa
     * @param  {object} point   Objeto con el trace de los puntos en el mapa
     * @param  {int} index      Indice del trace en el arreglo local de traces
     * @param  {object} styles  Estilos para dibujar el trace
     */
    createMapTrace: function (point, index) {
        var paths = _.map(point.trace, function (tracePoint, index) {
            return {lat: parseFloat(tracePoint.lat), lng: parseFloat(tracePoint.long)};
        });
        var styles = this.parseKmlStyles(point.styles);

        var isPolygon = (paths[0].lat == paths[paths.length-1].lat && paths[0].lng == paths[paths.length-1].lng);
        if(isPolygon){
            var obj = this.createMapPolygon(paths, styles.polyStyle);
        } else {
            var obj = this.createMapPolyline(paths, styles.lineStyle);    
        }
        this.mapTraces.push(obj)

        var self = this;
        if(point.info){
            var clickHandler = google.maps.event.addListener(obj, 'click', (function (marker, info) {
                return function(event) {
                    self.infoWindow.setContent("<div class='junarinfowindow'>" + String(info) + "</div>");
                    self.infoWindow.setPosition(event.latLng);
                    self.infoWindow.open(self.mapInstance, marker);
                }
            })(obj, point.info));
            obj.events = {click: clickHandler};
        }
        
        obj.setMap(this.mapInstance);
    },

    createMapPolygon: function (paths, styles) {
        var poly = new google.maps.Polygon({
            paths: paths,
            strokeColor: styles.strokeColor,
            strokeOpacity: styles.strokeOpacity,
            strokeWeight: styles.strokeWeight,
            fillColor: styles.fillColor,
            fillOpacity: styles.fillOpacity
        });

        poly.weight = 1;
        this.addWeightLocation(poly);

        return poly;
    },

    createMapPolyline: function (path, styles) {
        var line = new google.maps.Polyline({
            path: path,
            strokeColor: styles.strokeColor,
            strokeOpacity: styles.strokeOpacity,
            strokeWeight: styles.strokeWeight
        });
        
        line.weight = 1;
        this.addWeightLocation(line);
        return line;
    },

    /**
     * Crea un marker dentro del mapa
     * @param  {object} point   Objeto con las coordenadas del punto en el mapa
     * @param  {int}    index   Indice del punto en el arreglo local de markers
     * @param  {object} styles  Estilos para dibujar el marker
     */
    createMapMarker: function (point, index, oms) {
        var self = this, markerIcon = this.stylesDefault.marker.icon;

        //agregar al heatmap
        point.weight = 1;
        this.addWeightLocation(point);

        //Obtiene el estilo del marcador
        if(point.styles && point.styles.iconStyle){
            //TODO For now personalized KMLFile-included markers files are not readable for us
            if (undefined !== point.styles.iconStyle.href) {
                //just if it's a external link
                if (point.styles.iconStyle.href.indexOf("http") > -1) {
                    markerIcon = point.styles.iconStyle.href;
                    }
                }
            
        }

        this.mapMarkers[index] = new google.maps.Marker({
            position: new google.maps.LatLng(point.lat, point.long),
            map: this.mapInstance,
            icon: markerIcon,
            info: point.info // ADDED for OMS
        });
        oms.addMarker(this.mapMarkers[index]);

        if(point.info){
            
            /*var clickHandler = google.maps.event.addListener(this.mapMarkers[index], 'click', (function (marker, info) {
                return function() {
                    self.infoWindow.setContent("<div class='junarinfowindow'>" + String(info) + "</div>");
                    self.infoWindow.open(self.mapInstance, marker);
                }
            })(self.mapMarkers[index], point.info));
            this.mapMarkers[index].events = {click: clickHandler};
            */
            oms.addListener('click', function(marker, info) {
                self.infoWindow.setContent("<div class='junarinfowindow'>" + String(marker.info) + "</div>");
                self.infoWindow.open(self.mapInstance, marker);
            });

            oms.addListener('spiderfy', function(markers) {
              self.infoWindow.close();
            });
            
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
        this.mapClusters[index] = new multimarker(cluster, cluster.info, this.mapInstance, true /* joinIntersectedClusters */);
        var hPoint = {lat: parseFloat(cluster.lat), long: parseFloat(cluster.long), weight: parseInt(cluster.info)};
        this.addWeightLocation(hPoint);
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
        var parsedStyles = _.clone(this.stylesDefault);

        if (_.isUndefined(styles)) {
            return parsedStyles;
        }
        if(styles.lineStyle){
            parsedStyles.lineStyle = this.kmlStyleToLine(styles.lineStyle);
        }
        if(styles.polyStyle){
            parsedStyles.polyStyle = this.kmlStyleToPolygon(parsedStyles.lineStyle, styles.polyStyle);
        }

        return parsedStyles;
    },

    /**
     * Prser para los estilos desde un kml a lineas de google maps
     * @param  {object} lineStyle
     * @return {object
     */
    kmlStyleToLine: function(lineStyle) {
        var defaultStyle = _.clone(this.stylesDefault.lineStyle);
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
        var defaultStyle = _.clone(this.stylesDefault.polyStyle);

        return {
            "strokeColor": lineStyle.strokeColor,
            "strokeOpacity": lineStyle.strokeOpacity,
            "strokeWeight": lineStyle.strokeWeight,
            "fillColor": this.getStyleFromKml(polyStyle, 'color', 'color', defaultStyle.fillColor),
            "fillOpacity": this.getStyleFromKml(polyStyle, 'color', 'opacity', defaultStyle.fillOpacity)
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
        if(type == 'color') {
            return '#' + style.substring(2);
        }
        //La opacidad se extrae del color y convierte de hexadecimal a entero
        if(type == 'opacity') {
            return parseInt(style.substring(0, 2), 16) / 256;
        }

        if(type == 'width') {
            var value = parseFloat(style);
            return (value === 0)? 1 : value;
        }

        return style;
    },
    toggleHeatMap: function(){
        // toogle
        this.onHeatMap = !this.heatMapLayer.getMap();
        this.render(); 
    },

    addWeightLocation: function(obj) {
        weight = obj.weight || 1;
        this.heatMapPoints.push({location: new google.maps.LatLng(obj.lat, obj.long), weight: weight});
    }

});
