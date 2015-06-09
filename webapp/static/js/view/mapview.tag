<mapview>
	<div name="themap" style="height: 300px; width: 100%; position: relative;"/>
	<script>
		var size = $("listview").width()-40;
		this.msize = "height:"+size+"px; width:"+size+"px; position: relative"
		this.init_map = function(){
			//'tiles/'+this.opts.iid+'/{z}/{x}/{y}'
			this.mapL = L.tileLayer('tiles/'+this.opts.iid+'/{z}/{x}/{y}', {
		 		maxZoom: 8,	
		 		continuousWorld : true,
		 		noWrap : true,
		 		attribution: 'YDC'
		 	});
		 	this.utfL =new L.UtfGrid('infos/'+this.opts.iid+'/{z}/{x}/{y}', {
		 		maxZoom: 8,
		 		continuousWorld : true,
		 		noWrap : true,
		 		resolution: 2,
		 		attribution: 'YDC',
		 		useJsonP: false
		 	});
		 	this.opts.syncmaps = this.opts.syncmaps || {};
		 	var maps = this.opts.syncmaps;
		 	// initalise to the same center;
		 	var center, zoom;
		 	for (var otherid in maps){
				if (maps[otherid]){
					zoom = maps[otherid].getZoom();
					center = maps[otherid].getCenter();
				}
			}
		 	this.map = new L.Map(this.themap, {
		 		center: center || [0, 0],
				crs: L.CRS.Simple,
				zoomControl : true,
				attributionControl : false,
				minZoom: 0,
				maxZoom: 8,	
				zoom: zoom || 1
		 	}).addLayer(this.utfL).addLayer(this.mapL);
		 	this.utfL.on('click', function(e){
		 		if (e.data && e.data.color){
		 			$(".toast").hide(function(){$(this).remove});
		 			Materialize.toast("Color: "+e.data.color, 10*1000);
		 		}
		 	});
		}
		this.synchronise = function(){
			this.opts.syncmaps = this.opts.syncmaps || {};
			var maps = this.opts.syncmaps;
			var id = this.opts.iid;
			for (var otherid in maps){
				if (maps[otherid]){
					this.map.sync(maps[otherid]);
					maps[otherid].sync(this.map);
				}
			}
			maps[id] = this.map;
		}
		this.unsynchronise = function(){
			this.opts.syncmaps = this.opts.syncmaps || {};
			var maps = this.opts.syncmaps;
			var id = this.opts.iid;
			maps[id] = undefined;
			for (var otherid in maps){
				if (maps[otherid]){
					maps[otherid].unsync(this.map);
					this.map.unsync(maps[otherid]);
				}
			}
		}
		this.init_map();
		this.synchronise();
		
		mapActivateStore.listen((function(){
			if (!mapActivateStore.isActivated(this.opts.iid)){
				this.unsynchronise();
			}
		}).bind(this));

		this.on('update', (function(){
			// the size has been dynamically adjusted, need to call this function
			// see http://leafletjs.com/reference.html#map-invalidatesize
			console.log("size changed!");
			this.map.invalidateSize();
		}).bind(this));
	</script>
</mapview>