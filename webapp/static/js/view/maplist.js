riot.tag('maplist', '<ul class="collection with-header"> <li class="collection-header"><h4>Choose Map</h4></li> <listitem each="{items}" iid="{id}" name="{name}" status="{status}" activated="{parent.isActivated(id)}"></listitem> <li class="collection-item center-align" onclick="{addmap}"> <a href="#"> <i class="fa fa-plus"></i> </a> </li> </ul>', function(opts) {
		this.addmap = function(){
			modalActions.openModal("addMap");
		}
		this.updateMaps = function(new_maps, updatemaps, entermaps, exitmaps){









			this.items = new_maps;
			this.update();
		}
		this.isActivated = function(id){
			return mapActivateStore.isActivated(id);
		}
		this.items = [];
		mapsStore.listen((this.updateMaps).bind(this));
		mapActivateStore.listen((this.update).bind(this));
		mapActions.getMaps();
	
});